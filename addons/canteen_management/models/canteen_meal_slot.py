# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class CanteenMealSlot(models.Model):
    _name = "canteen.meal.slot"
    _description = "Canteen Meal Slot"
    _inherit = ["mail.thread"]
    _order = "start_at, id"

    name = fields.Char(
        string="Tên ca ăn",
        required=True,
        size=128,
        index=True,
        tracking=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Món / Suất ăn",
        required=True,
        ondelete="restrict",
        index=True,
        tracking=True,
    )
    start_at = fields.Datetime(
        string="Thời điểm bắt đầu",
        required=True,
        index=True,
        tracking=True,
    )
    end_at = fields.Datetime(
        string="Thời điểm kết thúc",
        required=True,
        index=True,
        tracking=True,
    )
    capacity = fields.Integer(
        string="Sức chứa tối đa",
        required=True,
        default=50,
        tracking=True,
    )
    booked_count = fields.Integer(
        string="Số suất đã đặt",
        compute="_compute_booked_count",
        store=True,
        precompute=True,
        index=True,
        readonly=True,
        copy=False,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Nháp"),
            ("open", "Mở đặt chỗ"),
            ("full", "Đã hết chỗ"),
            ("closed", "Đã kết thúc"),
        ],
        string="Trạng thái",
        required=True,
        default="draft",
        index=True,
        tracking=True,
    )
    active = fields.Boolean(
        string="Hiệu lực",
        required=True,
        default=True,
    )

    _check_time_range = models.Constraint(
        "CHECK(start_at < end_at)",
        "Thời gian bắt đầu ca ăn phải trước thời gian kết thúc!",
    )
    _check_non_negative_capacity = models.Constraint(
        "CHECK(capacity >= 0)",
        "Sức chứa tối đa của ca ăn không được âm!",
    )
    _check_non_negative_booked_count = models.Constraint(
        "CHECK(booked_count >= 0)",
        "Số suất đã đặt không được âm!",
    )
    _check_booked_within_capacity = models.Constraint(
        "CHECK(booked_count <= capacity)",
        "Số suất đã đặt không được vượt quá sức chứa tối đa!",
    )

    def _compute_booked_count(self):
        # shortcut: booking_ids One2many and @api.depends("booking_ids.state", "booking_ids.quantity")
        # are deferred until canteen.meal.booking exists (KAN-161); an unresolved One2many crashes
        # Odoo registry loading.
        if "canteen.meal.booking" not in self.env:
            for slot in self:
                slot.booked_count = 0
            return

        counts = {}
        if self.ids:
            grouped = self.env["canteen.meal.booking"].sudo()._read_group(
                domain=[
                    ("slot_id", "in", self.ids),
                    ("state", "in", ["confirmed", "served"]),
                ],
                groupby=["slot_id"],
                aggregates=["quantity:sum"],
            )
            counts = {slot.id: total or 0 for slot, total in grouped if slot}

        for slot in self:
            slot.booked_count = counts.get(slot.id, 0)

    @api.constrains("start_at", "end_at")
    def _check_time_range_values(self):
        for slot in self:
            if slot.start_at and slot.end_at and slot.start_at >= slot.end_at:
                raise ValidationError(
                    _("Thời gian bắt đầu ca ăn phải trước thời gian kết thúc!")
                )

    @api.constrains("capacity", "booked_count")
    def _check_capacity_values(self):
        for slot in self:
            if slot.capacity < 0:
                raise ValidationError(_("Sức chứa tối đa của ca ăn không được âm!"))
            if slot.booked_count < 0:
                raise ValidationError(_("Số suất đã đặt không được âm!"))
            if slot.booked_count > slot.capacity:
                raise ValidationError(
                    _("Số suất đã đặt không được vượt quá sức chứa tối đa!")
                )

    def _check_manager_access(self):
        if not self.env.su and not self.env.user.has_group(
            "canteen_management.group_canteen_manager"
        ):
            raise AccessError(
                _("Chỉ Quản lý Căn tin mới có quyền mở hoặc đóng ca ăn!")
            )

    def _sync_capacity_state(self):
        for slot in self:
            if slot.state == "open" and slot.booked_count >= slot.capacity:
                slot.state = "full"
            elif slot.state == "full" and slot.booked_count < slot.capacity:
                slot.state = "open"

    def write(self, vals):
        res = super().write(vals)
        if "capacity" in vals and "state" not in vals:
            self._sync_capacity_state()
        return res

    def action_open_slot(self):
        self._check_manager_access()
        for slot in self:
            if slot.state != "draft":
                raise UserError(_("Chỉ có thể mở ca ăn đang ở trạng thái Nháp!"))
            if not slot.active:
                raise UserError(_("Không thể mở ca ăn đã bị vô hiệu hóa!"))
            if slot.capacity <= 0:
                raise UserError(
                    _("Sức chứa ca ăn phải lớn hơn 0 trước khi mở đặt chỗ!")
                )
            slot.state = "full" if slot.booked_count >= slot.capacity else "open"
        return True

    def action_close_slot(self):
        self._check_manager_access()
        for slot in self:
            if slot.state not in ("open", "full"):
                raise UserError(
                    _("Chỉ có thể đóng ca ăn đang ở trạng thái Mở hoặc Đã hết chỗ!")
                )
            slot.state = "closed"
        return True

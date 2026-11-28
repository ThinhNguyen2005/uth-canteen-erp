# -*- coding: utf-8 -*-
import uuid

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CanteenMealBooking(models.Model):
    _name = "canteen.meal.booking"
    _description = "Canteen Meal Booking"
    _inherit = ["mail.thread"]
    _rec_name = "booking_ref"
    _order = "booked_at desc, id desc"

    booking_ref = fields.Char(
        string="Mã phiếu đặt",
        required=True,
        size=64,
        index=True,
        copy=False,
        readonly=True,
        default="/",
    )
    access_token = fields.Char(
        string="Token tra cứu",
        required=True,
        size=64,
        index=True,
        copy=False,
        readonly=True,
        default=lambda self: str(uuid.uuid4()),
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Người đặt suất",
        required=True,
        ondelete="restrict",
        index=True,
        tracking=True,
    )
    slot_id = fields.Many2one(
        comodel_name="canteen.meal.slot",
        string="Ca ăn đăng ký",
        required=True,
        ondelete="restrict",
        index=True,
        tracking=True,
    )
    quantity = fields.Integer(
        string="Số suất đặt",
        required=True,
        default=1,
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Nháp (Nội bộ)"),
            ("confirmed", "Đã xác nhận"),
            ("served", "Đã nhận phần ăn"),
            ("cancelled", "Đã hủy"),
        ],
        string="Trạng thái",
        required=True,
        default="confirmed",
        index=True,
        tracking=True,
    )
    booked_at = fields.Datetime(
        string="Thời điểm đặt",
        required=True,
        default=fields.Datetime.now,
        readonly=True,
    )
    note = fields.Char(
        string="Ghi chú suất ăn",
        size=255,
    )

    _check_quantity_limit = models.Constraint(
        "CHECK(quantity >= 1 AND quantity <= 3)",
        "Mỗi lượt đặt chỉ được phép từ 1 đến 3 suất ăn!",
    )
    _unique_booking_ref = models.Constraint(
        "UNIQUE(booking_ref)",
        "Mã phiếu đặt suất ăn phải là duy nhất!",
    )
    _unique_booking_access_token = models.Constraint(
        "UNIQUE(access_token)",
        "Access token của phiếu đặt suất ăn phải là duy nhất!",
    )
    _unique_active_partner_meal_slot = models.UniqueIndex(
        "(partner_id, slot_id) WHERE state = 'confirmed'",
        "Mỗi người đặt chỉ được có một phiếu đã xác nhận cho cùng một ca ăn!",
    )

    @api.model
    def _validate_slot_accepts_booking(self, slot):
        if not slot.active:
            raise ValidationError(_("Ca ăn đã bị vô hiệu hóa, không thể đặt chỗ!"))
        if slot.state != "open":
            raise ValidationError(_("Ca ăn hiện không mở nhận đặt chỗ!"))

    @api.constrains("quantity")
    def _check_quantity_values(self):
        for booking in self:
            if booking.quantity < 1 or booking.quantity > 3:
                raise ValidationError(
                    _("Mỗi lượt đặt chỉ được phép từ 1 đến 3 suất ăn!")
                )

    @api.constrains("booking_ref", "access_token")
    def _check_identifiers(self):
        for booking in self:
            ref = (booking.booking_ref or "").strip()
            token = (booking.access_token or "").strip()
            if not ref or ref == "/":
                raise ValidationError(_("Mã phiếu đặt suất ăn không hợp lệ!"))
            if not token:
                raise ValidationError(_("Token tra cứu phiếu đặt không hợp lệ!"))

    @api.constrains("partner_id", "slot_id", "state")
    def _check_booking_consistency(self):
        booking_model = self.sudo()
        for booking in self:
            if booking.state in ("draft", "confirmed") and not booking.slot_id.active:
                raise ValidationError(
                    _("Ca ăn đã bị vô hiệu hóa, không thể đặt chỗ!")
                )
            if booking.state == "confirmed":
                duplicate_count = booking_model.search_count([
                    ("id", "!=", booking.id),
                    ("partner_id", "=", booking.partner_id.id),
                    ("slot_id", "=", booking.slot_id.id),
                    ("state", "=", "confirmed"),
                ])
                if duplicate_count:
                    raise ValidationError(
                        _(
                            "Mỗi người đặt chỉ được có một phiếu đã xác nhận cho cùng một ca ăn!"
                        )
                    )

    @api.model_create_multi
    def create(self, vals_list):
        prepared_vals = []
        slot_model = self.env["canteen.meal.slot"].sudo()
        seq_model = self.env["ir.sequence"].sudo()
        for vals in vals_list:
            vals = dict(vals)
            if vals.get("booking_ref") in (None, False, "", "/"):
                vals["booking_ref"] = (
                    seq_model.next_by_code("canteen.meal.booking")
                    or f"BKG-{uuid.uuid4().hex[:12].upper()}"
                )
            if "access_token" not in vals or vals["access_token"] is False:
                vals["access_token"] = str(uuid.uuid4())
            state = vals.get("state", "confirmed")
            slot_id = vals.get("slot_id")
            if slot_id and state == "confirmed":
                slot = slot_model.browse(slot_id)
                if slot.exists():
                    self._validate_slot_accepts_booking(slot)
            prepared_vals.append(vals)

        bookings = super().create(prepared_vals)
        bookings.mapped("slot_id").sudo()._sync_capacity_state()
        return bookings

    def write(self, vals):
        affected_slots = self.mapped("slot_id")
        target_state = vals.get("state")
        target_slot_id = vals.get("slot_id")
        if target_state == "confirmed" or target_slot_id:
            slot_model = self.env["canteen.meal.slot"].sudo()
            for booking in self:
                new_state = target_state or booking.state
                new_slot = (
                    slot_model.browse(target_slot_id)
                    if target_slot_id
                    else booking.slot_id
                )
                is_entering_slot = new_state == "confirmed" and (
                    booking.state != "confirmed"
                    or (target_slot_id and target_slot_id != booking.slot_id.id)
                )
                if is_entering_slot and new_slot.exists():
                    self._validate_slot_accepts_booking(new_slot)

        res = super().write(vals)
        if {"slot_id", "state", "quantity"} & set(vals):
            (affected_slots | self.mapped("slot_id")).sudo()._sync_capacity_state()
        return res

    def unlink(self):
        affected_slots = self.mapped("slot_id")
        res = super().unlink()
        affected_slots.sudo()._sync_capacity_state()
        return res

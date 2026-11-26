# -*- coding: utf-8 -*-
from datetime import timedelta
import uuid

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class CanteenMealBooking(models.Model):
    _name = "canteen.meal.booking"
    _description = "Canteen Meal Booking"
    _inherit = ["mail.thread"]
    _rec_name = "booking_ref"
    _order = "booked_at desc, id desc"

    CANCEL_DEADLINE_MINUTES = 30
    ALLOWED_STATE_TRANSITIONS = {
        "draft": {"confirmed", "cancelled"},
        "confirmed": {"served", "cancelled"},
        "served": set(),
        "cancelled": set(),
    }
    LOCKED_FIELDS_AFTER_DRAFT = frozenset(
        {
            "partner_id",
            "slot_id",
            "quantity",
            "booked_at",
            "booking_ref",
            "access_token",
        }
    )

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
        is_manager = self._is_manager()
        requested_by_slot = {}

        for vals in vals_list:
            vals = dict(vals)
            state = vals.get("state", "confirmed")

            if not is_manager:
                if not self.env.user.has_group("canteen_management.group_canteen_user"):
                    raise AccessError(_("Bạn không có quyền tạo phiếu đặt suất ăn!"))
                if vals.get("partner_id") and vals["partner_id"] != self.env.user.partner_id.id:
                    raise AccessError(
                        _("Bạn không được tạo phiếu đặt suất cho người khác!")
                    )
                if state != "confirmed":
                    raise ValidationError(
                        _("Người đặt chỉ có thể tạo phiếu ở trạng thái Đã xác nhận!")
                    )
            elif not self.env.su and state not in ("draft", "confirmed"):
                raise ValidationError(
                    _("Chỉ có thể tạo phiếu mới ở trạng thái Nháp hoặc Đã xác nhận!")
                )

            if vals.get("booking_ref") in (None, False, "", "/"):
                vals["booking_ref"] = (
                    seq_model.next_by_code("canteen.meal.booking")
                    or f"BKG-{uuid.uuid4().hex[:12].upper()}"
                )
            if "access_token" not in vals or vals["access_token"] is False:
                vals["access_token"] = str(uuid.uuid4())

            qty = vals.get("quantity", 1)
            if isinstance(qty, int) and not isinstance(qty, bool):
                if qty < 1 or qty > 3:
                    raise ValidationError(
                        _("Mỗi lượt đặt chỉ được phép từ 1 đến 3 suất ăn!")
                    )
                slot_id = vals.get("slot_id")
                if slot_id and state == "confirmed":
                    requested_by_slot[slot_id] = requested_by_slot.get(slot_id, 0) + qty

            prepared_vals.append(vals)

        for slot_id, req_qty in requested_by_slot.items():
            slot = slot_model.browse(slot_id)
            if slot.exists():
                self._validate_slot_accepts_booking(slot)
                slot._compute_booked_count()
                if slot.booked_count + req_qty > slot.capacity:
                    remaining = max(slot.capacity - slot.booked_count, 0)
                    raise ValidationError(
                        _("Ca ăn không còn đủ suất trống! Hiện chỉ còn %s suất.")
                        % remaining
                    )

        bookings = super().create(prepared_vals)
        bookings.mapped("slot_id").sudo()._sync_capacity_state()
        return bookings

    def write(self, vals):
        affected_slots = self.mapped("slot_id")
        changed_fields = set(vals)
        target_state = vals.get("state")
        target_slot_id = vals.get("slot_id")

        if "state" in vals:
            allow_direct = self.env.su or self.env.context.get(
                "canteen_allow_state_write"
            )
            for booking in self:
                if target_state == booking.state:
                    continue
                allowed = self.ALLOWED_STATE_TRANSITIONS.get(booking.state, set())
                if target_state not in allowed:
                    raise ValidationError(
                        _("Không thể chuyển trạng thái phiếu từ '%s' sang '%s'!")
                        % (booking.state, target_state)
                    )
                if not allow_direct:
                    raise AccessError(
                        _(
                            "Không được ghi trực tiếp trạng thái phiếu; vui lòng dùng hành động Confirm / Cancel / Serve!"
                        )
                    )

        locked_touched = changed_fields & self.LOCKED_FIELDS_AFTER_DRAFT
        if locked_touched:
            is_manager = self._is_manager()
            for booking in self:
                if booking.state != "draft":
                    raise ValidationError(
                        _(
                            "Không thể chỉnh sửa thông tin đặt suất sau khi phiếu đã xác nhận, phục vụ hoặc hủy!"
                        )
                    )
                if (
                    "partner_id" in locked_touched
                    and not is_manager
                    and vals["partner_id"] != booking.partner_id.id
                ):
                    raise AccessError(_("Bạn không có quyền thay đổi người đặt suất!"))

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
                    new_slot._compute_booked_count()
                    new_qty = vals.get("quantity", booking.quantity)
                    if (
                        isinstance(new_qty, int)
                        and not isinstance(new_qty, bool)
                        and new_slot.booked_count + new_qty > new_slot.capacity
                    ):
                        remaining = max(new_slot.capacity - new_slot.booked_count, 0)
                        raise ValidationError(
                            _("Ca ăn không còn đủ suất trống! Hiện chỉ còn %s suất.")
                            % remaining
                        )

        res = super().write(vals)
        if {"slot_id", "state", "quantity"} & changed_fields:
            (affected_slots | self.mapped("slot_id")).sudo()._sync_capacity_state()
        return res

    def unlink(self):
        if not self.env.su:
            for booking in self:
                if booking.state in ("confirmed", "served"):
                    raise UserError(
                        _(
                            "Không được xóa phiếu đã xác nhận hoặc đã phục vụ; vui lòng dùng thao tác Hủy phiếu!"
                        )
                    )
        affected_slots = self.mapped("slot_id")
        res = super().unlink()
        affected_slots.sudo()._sync_capacity_state()
        return res

    def _is_manager(self):
        return self.env.su or self.env.user.has_group(
            "canteen_management.group_canteen_manager"
        )

    def _is_cashier(self):
        return self.env.su or self.env.user.has_group(
            "canteen_management.group_canteen_cashier"
        )

    def _check_cancel_permission(self, booking):
        if self._is_manager():
            return
        is_owner = (
            self.env.user.has_group("canteen_management.group_canteen_user")
            and booking.partner_id == self.env.user.partner_id
        )
        if not is_owner:
            raise AccessError(
                _("Bạn chỉ được phép hủy phiếu đặt suất của chính mình!")
            )
        if booking.state == "draft":
            raise AccessError(
                _("Chỉ Quản lý Căn tin mới có quyền hủy phiếu nháp nội bộ!")
            )

    def action_confirm_booking(self):
        if not self._is_manager():
            raise AccessError(
                _("Chỉ Quản lý Căn tin mới có quyền xác nhận phiếu nháp!")
            )
        self.check_access("read")
        for booking in self:
            if booking.state == "confirmed":
                raise UserError(_("Phiếu đặt suất đã được xác nhận trước đó!"))
            if booking.state != "draft":
                raise UserError(
                    _("Chỉ có thể xác nhận phiếu đang ở trạng thái Nháp!")
                )

            slot = booking.slot_id.sudo()
            self._validate_slot_accepts_booking(slot)
            slot._compute_booked_count()
            if slot.booked_count + booking.quantity > slot.capacity:
                remaining = max(slot.capacity - slot.booked_count, 0)
                raise UserError(
                    _("Ca ăn không còn đủ suất trống! Hiện chỉ còn %s suất.")
                    % remaining
                )

            booking.with_context(canteen_allow_state_write=True).sudo().write(
                {"state": "confirmed"}
            )
        return True

    def action_cancel_booking(self):
        self.check_access("read")
        now = fields.Datetime.now()
        is_manager = self._is_manager()
        for booking in self:
            self._check_cancel_permission(booking)
            if booking.state == "cancelled":
                raise UserError(_("Phiếu đặt suất đã được hủy trước đó!"))
            if booking.state == "served":
                raise UserError(_("Không thể hủy phiếu đã nhận phần ăn!"))
            if booking.state not in ("draft", "confirmed"):
                raise UserError(_("Trạng thái phiếu hiện tại không thể hủy!"))

            if booking.state == "confirmed" and not is_manager:
                slot = booking.slot_id.sudo()
                if not slot.start_at:
                    raise UserError(
                        _("Ca ăn chưa có thời gian bắt đầu hợp lệ để kiểm tra hạn hủy!")
                    )
                deadline = slot.start_at - timedelta(
                    minutes=self.CANCEL_DEADLINE_MINUTES
                )
                if now > deadline:
                    raise UserError(
                        _("Chỉ được hủy phiếu trước giờ bắt đầu ca ít nhất 30 phút!")
                    )

            booking.with_context(canteen_allow_state_write=True).sudo().write(
                {"state": "cancelled"}
            )
        return True

    def action_mark_booking_served(self):
        if not self._is_cashier():
            raise AccessError(
                _(
                    "Chỉ Thu ngân / Phục vụ hoặc Quản lý mới có quyền check-in giao suất!"
                )
            )
        self.check_access("read")
        for booking in self:
            if booking.state == "served":
                raise UserError(
                    _(
                        "Phiếu đặt suất đã được phục vụ trước đó, không thể nhận lần hai!"
                    )
                )
            if booking.state == "cancelled":
                raise UserError(_("Không thể phục vụ phiếu đã bị hủy!"))
            if booking.state != "confirmed":
                raise UserError(
                    _("Chỉ có thể phục vụ phiếu đang ở trạng thái Đã xác nhận!")
                )

            slot = booking.slot_id.sudo()
            if not slot.active or slot.state not in ("open", "full"):
                raise UserError(_("Ca ăn hiện không ở trạng thái sẵn sàng phục vụ!"))

            booking.with_context(canteen_allow_state_write=True).sudo().write(
                {"state": "served"}
            )
        return True

    # Aliases matching Jira ERP-41 names; canonical contract names (KAN-158) are above.
    def action_confirm(self):
        return self.action_confirm_booking()

    def action_cancel(self):
        return self.action_cancel_booking()

    def action_serve(self):
        return self.action_mark_booking_served()

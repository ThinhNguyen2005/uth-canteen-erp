# -*- coding: utf-8 -*-
from datetime import timedelta
import logging
import uuid

import psycopg2

from odoo import _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

_logger = logging.getLogger(__name__)


class CanteenMealBooking(models.Model):
    _name = "canteen.meal.booking"
    _description = "Canteen Meal Booking"
    _inherit = ["mail.thread"]
    _rec_name = "booking_ref"
    _order = "booked_at desc, id desc"

    CANCEL_DEADLINE_MINUTES = 30
    SLOT_LOCK_TIMEOUT = "3000ms"
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
    def _validate_locked_slot_capacity(
        self, slot_data, requested_qty, exc_cls=ValidationError
    ):
        if not slot_data["active"]:
            raise exc_cls(_("Ca ăn đã bị vô hiệu hóa, không thể đặt chỗ!"))
        if slot_data["state"] == "full":
            raise exc_cls(_("Ca ăn không còn đủ suất trống! Hiện chỉ còn 0 suất."))
        if slot_data["state"] != "open":
            raise exc_cls(_("Ca ăn hiện không mở nhận đặt chỗ!"))
        if slot_data["booked_count"] + requested_qty > slot_data["capacity"]:
            remaining = max(slot_data["capacity"] - slot_data["booked_count"], 0)
            raise exc_cls(
                _("Ca ăn không còn đủ suất trống! Hiện chỉ còn %s suất.") % remaining
            )

    @api.model
    def _lock_slots_for_update(self, slot_ids, nowait=False):
        ordered_ids = sorted(
            {
                sid
                for sid in slot_ids
                if isinstance(sid, int) and not isinstance(sid, bool) and sid > 0
            }
        )
        if not ordered_ids:
            return {}

        slot_model = self.env["canteen.meal.slot"].sudo()
        booking_model = self.env["canteen.meal.booking"].sudo()
        slot_model.flush_model(["capacity", "booked_count", "state", "active"])
        booking_model.flush_model(["slot_id", "state", "quantity"])

        already_locked = frozenset(self.env.context.get("canteen_slot_locked_ids", ()))
        ids_to_lock = [sid for sid in ordered_ids if sid not in already_locked]
        cr = self.env.cr
        locked_rows = []

        if ids_to_lock:
            lock_clause = "FOR UPDATE NOWAIT" if nowait else "FOR UPDATE"
            query = (
                "SELECT id, capacity, booked_count, state, active "
                "FROM canteen_meal_slot "
                "WHERE id IN %s "
                "ORDER BY id ASC "
                f"{lock_clause}"
            )
            try:
                with cr.savepoint():
                    prev_timeout = None
                    if not nowait:
                        cr.execute("SELECT current_setting('lock_timeout')")
                        row = cr.fetchone()
                        prev_timeout = row[0] if row else None
                        cr.execute(
                            "SELECT set_config('lock_timeout', %s, true)",
                            (self.SLOT_LOCK_TIMEOUT,),
                        )
                    cr.execute(query, (tuple(ids_to_lock),))
                    locked_rows.extend(cr.dictfetchall())
                    if prev_timeout is not None:
                        cr.execute(
                            "SELECT set_config('lock_timeout', %s, true)",
                            (prev_timeout,),
                        )
            except psycopg2.OperationalError as err:
                pgcode = getattr(err, "pgcode", None)
                if pgcode == "55P03":
                    _logger.warning(
                        "Lock contention on canteen.meal.slot ids %s: %s",
                        ids_to_lock,
                        err,
                    )
                    raise UserError(
                        _(
                            "Hệ thống đang bận xử lý lượt đặt khác cho ca ăn này, vui lòng thử lại sau giây lát!"
                        )
                    ) from err
                if pgcode in ("40001", "40P01"):
                    _logger.warning(
                        "Transaction contention (%s) on canteen.meal.slot ids %s; propagating for transaction retry: %s",
                        pgcode,
                        ids_to_lock,
                        err,
                    )
                raise

        reused_ids = [sid for sid in ordered_ids if sid in already_locked]
        if reused_ids:
            cr.execute(
                "SELECT id, capacity, booked_count, state, active "
                "FROM canteen_meal_slot "
                "WHERE id IN %s "
                "ORDER BY id ASC",
                (tuple(reused_ids),),
            )
            locked_rows.extend(cr.dictfetchall())

        if not locked_rows:
            return {}

        locked_ids = sorted(row["id"] for row in locked_rows)
        cr.execute(
            "SELECT slot_id, COALESCE(SUM(quantity), 0) AS booked_count "
            "FROM canteen_meal_booking "
            "WHERE slot_id IN %s AND state IN ('confirmed', 'served') "
            "GROUP BY slot_id",
            (tuple(locked_ids),),
        )
        fresh_counts = {
            row["slot_id"]: int(row["booked_count"] or 0)
            for row in cr.dictfetchall()
        }

        slot_model.browse(locked_ids).invalidate_recordset(
            ["capacity", "booked_count", "state", "active"]
        )

        result = {}
        for row in locked_rows:
            row_data = dict(row)
            row_data["booked_count"] = fresh_counts.get(row["id"], 0)
            result[row["id"]] = row_data
        return result

    def _check_create_permission(self, partner_id, state, is_manager):
        if not is_manager:
            if not self.env.user.has_group("canteen_management.group_canteen_user"):
                raise AccessError(_("Bạn không có quyền tạo phiếu đặt suất ăn!"))
            if partner_id and partner_id != self.env.user.partner_id.id:
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

    @api.model
    def create_booking_safe(
        self, partner_id, slot_id, quantity=1, note=False, nowait=False
    ):
        partner_id = partner_id.id if hasattr(partner_id, "id") else partner_id
        slot_id = slot_id.id if hasattr(slot_id, "id") else slot_id
        if (
            not isinstance(partner_id, int)
            or isinstance(partner_id, bool)
            or partner_id <= 0
        ):
            raise ValidationError(_("Người đặt suất không hợp lệ!"))
        if not isinstance(slot_id, int) or isinstance(slot_id, bool) or slot_id <= 0:
            raise ValidationError(_("Ca ăn không hợp lệ!"))
        if (
            not isinstance(quantity, int)
            or isinstance(quantity, bool)
            or quantity < 1
            or quantity > 3
        ):
            raise ValidationError(_("Mỗi lượt đặt chỉ được phép từ 1 đến 3 suất ăn!"))

        self._check_create_permission(partner_id, "confirmed", self._is_manager())

        locked_slots = self._lock_slots_for_update([slot_id], nowait=nowait)
        slot_data = locked_slots.get(slot_id)
        if not slot_data:
            raise UserError(_("Ca ăn không tồn tại trong hệ thống!"))

        self._validate_locked_slot_capacity(slot_data, quantity, exc_cls=UserError)

        locked_ctx = frozenset(self.env.context.get("canteen_slot_locked_ids", ())) | {
            slot_id
        }
        return self.with_context(canteen_slot_locked_ids=locked_ctx).create(
            [
                {
                    "partner_id": partner_id,
                    "slot_id": slot_id,
                    "quantity": quantity,
                    "note": note,
                    "state": "confirmed",
                }
            ]
        )

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
        seq_model = self.env["ir.sequence"].sudo()
        is_manager = self._is_manager()
        requested_by_slot = {}

        for vals in vals_list:
            vals = dict(vals)
            state = vals.get("state", "confirmed")
            self._check_create_permission(vals.get("partner_id"), state, is_manager)

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

        if requested_by_slot:
            locked_slots = self._lock_slots_for_update(requested_by_slot.keys())
            for slot_id in sorted(requested_by_slot):
                slot_data = locked_slots.get(slot_id)
                if slot_data:
                    self._validate_locked_slot_capacity(
                        slot_data,
                        requested_by_slot[slot_id],
                        exc_cls=ValidationError,
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

        locked_slots = {}
        if self and ({"slot_id", "state", "quantity"} & changed_fields):
            slot_ids = list(affected_slots.ids)
            if target_slot_id:
                slot_ids.append(target_slot_id)
            locked_slots = self._lock_slots_for_update(slot_ids)

        if target_state == "confirmed" or target_slot_id:
            entering_by_slot = {}
            for booking in self:
                new_state = target_state or booking.state
                new_slot_id = target_slot_id or booking.slot_id.id
                is_entering_slot = new_state == "confirmed" and (
                    booking.state != "confirmed"
                    or (target_slot_id and target_slot_id != booking.slot_id.id)
                )
                if is_entering_slot and new_slot_id in locked_slots:
                    new_qty = vals.get("quantity", booking.quantity)
                    if isinstance(new_qty, int) and not isinstance(new_qty, bool):
                        entering_by_slot[new_slot_id] = (
                            entering_by_slot.get(new_slot_id, 0) + new_qty
                        )
            for slot_id in sorted(entering_by_slot):
                self._validate_locked_slot_capacity(
                    locked_slots[slot_id],
                    entering_by_slot[slot_id],
                    exc_cls=ValidationError,
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
        if affected_slots:
            self._lock_slots_for_update(affected_slots.ids)
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
        if not self:
            return True

        locked_slots = self._lock_slots_for_update(self.sudo().mapped("slot_id").ids)
        self.invalidate_recordset(["state", "quantity", "slot_id", "partner_id"])

        current_slot_ids = self.sudo().mapped("slot_id").ids
        if set(current_slot_ids) - set(locked_slots):
            locked_slots.update(
                self.with_context(
                    canteen_slot_locked_ids=frozenset(locked_slots)
                )._lock_slots_for_update(current_slot_ids)
            )

        reserved_by_slot = {}
        for booking in self:
            if booking.state == "confirmed":
                raise UserError(_("Phiếu đặt suất đã được xác nhận trước đó!"))
            if booking.state != "draft":
                raise UserError(
                    _("Chỉ có thể xác nhận phiếu đang ở trạng thái Nháp!")
                )

            slot_id = booking.slot_id.id
            slot_data = locked_slots.get(slot_id)
            if not slot_data:
                raise UserError(_("Ca ăn không tồn tại trong hệ thống!"))

            projected = dict(slot_data)
            projected["booked_count"] = slot_data["booked_count"] + reserved_by_slot.get(
                slot_id, 0
            )
            self._validate_locked_slot_capacity(
                projected, booking.quantity, exc_cls=UserError
            )
            reserved_by_slot[slot_id] = (
                reserved_by_slot.get(slot_id, 0) + booking.quantity
            )

        locked_ctx = frozenset(self.env.context.get("canteen_slot_locked_ids", ())) | frozenset(
            locked_slots
        )
        for booking in self:
            booking.with_context(
                canteen_allow_state_write=True,
                canteen_slot_locked_ids=locked_ctx,
            ).sudo().write({"state": "confirmed"})
        return True

    def action_cancel_booking(self):
        if not self:
            return True
        for booking in self:
            self._check_cancel_permission(booking)

        now = fields.Datetime.now()
        is_manager = self._is_manager()
        locked_slots = self._lock_slots_for_update(self.sudo().mapped("slot_id").ids)
        self.invalidate_recordset(["state", "quantity", "slot_id", "partner_id"])

        for booking in self:
            self._check_cancel_permission(booking)
            if booking.state == "cancelled":
                raise UserError(_("Phiếu đặt suất đã được hủy trước đó!"))
            if booking.state == "served":
                raise UserError(_("Không thể hủy phiếu đã nhận phần ăn!"))
            if booking.state not in ("draft", "confirmed"):
                raise UserError(_("Trạng thái phiếu hiện tại không thể hủy!"))

            if booking.state == "confirmed" and not is_manager:
                deadline = booking.slot_id.start_at - timedelta(
                    minutes=self.CANCEL_DEADLINE_MINUTES
                )
                if now > deadline:
                    raise UserError(
                        _("Chỉ được hủy phiếu trước giờ bắt đầu ca ít nhất 30 phút!")
                    )

        locked_ctx = frozenset(self.env.context.get("canteen_slot_locked_ids", ())) | frozenset(
            locked_slots
        )
        for booking in self:
            booking.with_context(
                canteen_allow_state_write=True,
                canteen_slot_locked_ids=locked_ctx,
            ).sudo().write({"state": "cancelled"})
        return True

    def action_mark_booking_served(self):
        if not self._is_cashier():
            raise AccessError(
                _(
                    "Chỉ Thu ngân / Phục vụ hoặc Quản lý mới có quyền check-in giao suất!"
                )
            )
        if not self:
            return True

        locked_slots = self._lock_slots_for_update(self.sudo().mapped("slot_id").ids)
        self.invalidate_recordset(["state", "quantity", "slot_id", "partner_id"])

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

            slot_data = locked_slots.get(booking.slot_id.id)
            if (
                not slot_data
                or not slot_data["active"]
                or slot_data["state"] not in ("open", "full")
            ):
                raise UserError(_("Ca ăn hiện không ở trạng thái sẵn sàng phục vụ!"))

        locked_ctx = frozenset(self.env.context.get("canteen_slot_locked_ids", ())) | frozenset(
            locked_slots
        )
        for booking in self:
            booking.with_context(
                canteen_allow_state_write=True,
                canteen_slot_locked_ids=locked_ctx,
            ).sudo().write({"state": "served"})
        return True

    # Aliases matching Jira ERP-41 names; canonical contract names (KAN-158) are above.
    def action_confirm(self):
        return self.action_confirm_booking()

    def action_cancel(self):
        return self.action_cancel_booking()

    def action_serve(self):
        return self.action_mark_booking_served()

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase
from psycopg2 import IntegrityError


class TestBookingContract(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        product = cls.env["product.product"].create({"name": "Booking meal"})
        cls.partner = cls.env["res.partner"].create({"name": "Booking test partner"})
        cls.slot = cls.env["canteen.meal.slot"].create({
            "name": "Booking slot",
            "product_id": product.id,
            "start_at": "2026-12-01 11:00:00",
            "end_at": "2026-12-01 12:00:00",
            "capacity": 3,
        })
        cls.slot.action_open_slot()

    def _booking(self, **values):
        return self.env["canteen.meal.booking"].create(dict(
            {"partner_id": self.partner.id, "slot_id": self.slot.id}, **values
        ))

    def test_draft_confirm_serve_and_repeated_actions(self):
        booking = self._booking(state="draft")
        self.assertEqual(self.slot.booked_count, 0)
        booking.action_confirm_booking()
        self.assertEqual(booking.state, "confirmed")
        self.assertEqual(self.slot.booked_count, 1)
        with self.assertRaises(UserError):
            booking.action_confirm_booking()
        self.assertEqual(booking.state, "confirmed")
        self.assertEqual(self.slot.booked_count, 1)
        booking.action_mark_booking_served()
        with self.assertRaises(UserError):
            booking.action_mark_booking_served()
        self.assertEqual(booking.state, "served")
        self.assertEqual(self.slot.booked_count, 1)

    def test_quantity_duplicate_cancel_and_rebook(self):
        for quantity in (0, 4, True, "1", 1.5):
            with self.subTest(quantity=quantity):
                with self.assertRaises((ValidationError, IntegrityError)), self.env.cr.savepoint():
                    self._booking(quantity=quantity)
        booking = self._booking(quantity=1)
        self.assertEqual(booking.state, "confirmed")
        with self.assertRaises((ValidationError, IntegrityError)), self.env.cr.savepoint():
            self._booking(quantity=1)
        self.assertEqual(self.slot.booked_count, 1)
        booking.action_cancel_booking()
        with self.assertRaises(UserError):
            booking.action_cancel_booking()
        self.assertEqual(booking.state, "cancelled")
        self.assertEqual(self.slot.booked_count, 0)
        self._booking(quantity=3)
        self.assertEqual(self.slot.booked_count, 3)
        self.assertEqual(self.slot.state, "full")

    def test_safe_booking_capacity_and_rollback(self):
        booking_model = self.env["canteen.meal.booking"]
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            booking_model.create_booking_safe(self.partner.id, self.slot.id, quantity=4)

        rollback = RuntimeError("Roll back the test reservation")
        with self.assertRaisesRegex(RuntimeError, str(rollback)), self.env.cr.savepoint():
            booking_model.create_booking_safe(self.partner.id, self.slot.id, quantity=3)
            self.assertEqual(self.slot.booked_count, 3)
            self.assertEqual(self.slot.state, "full")
            raise rollback

        self.assertEqual(self.slot.booked_count, 0)
        self.assertEqual(self.slot.state, "open")
        self.assertFalse(booking_model.search_count([("slot_id", "=", self.slot.id)]))
        booking = booking_model.create_booking_safe(self.partner.id, self.slot.id, quantity=3)
        self.assertEqual(booking.state, "confirmed")
        self.assertEqual(self.slot.booked_count, 3)
        self.assertEqual(self.slot.state, "full")

    def test_confirmed_booking_fields_remain_unchanged(self):
        booking = self._booking(quantity=1)
        other_partner = self.env["res.partner"].create({"name": "Another booking partner"})
        other_slot = self.slot.copy({"name": "Another booking slot"})
        for field, value in (
            ("quantity", 2),
            ("partner_id", other_partner.id),
            ("slot_id", other_slot.id),
        ):
            with self.subTest(field=field):
                with self.assertRaises(ValidationError), self.env.cr.savepoint():
                    booking.write({field: value})
        self.assertEqual(booking.state, "confirmed")
        self.assertEqual(booking.quantity, 1)
        self.assertEqual(booking.partner_id, self.partner)
        self.assertEqual(booking.slot_id, self.slot)
        self.assertEqual(self.slot.booked_count, 1)
        self.assertEqual(other_slot.booked_count, 0)

    def test_duplicate_batch_preserves_booking_and_capacity(self):
        model = self.env["canteen.meal.booking"]
        values = {"partner_id": self.partner.id, "slot_id": self.slot.id, "quantity": 1}
        with self.assertRaises(ValidationError), self.env.cr.savepoint():
            model.create([values, values])
        self.assertFalse(model.search_count([("slot_id", "=", self.slot.id)]))
        drafts = model.create([dict(values, state="draft"), dict(values, state="draft")])
        with self.assertRaises(UserError), self.env.cr.savepoint():
            drafts.action_confirm_booking()
        self.assertEqual(drafts.mapped("state"), ["draft", "draft"])
        self.assertEqual(self.slot.booked_count, 0)
        self.assertEqual(self.slot.state, "open")

    def test_cancelled_booking_copy_has_new_identity(self):
        booking = self._booking(access_token="  ")
        self.assertTrue(booking.access_token.strip())
        with self.assertRaises(UserError), self.env.cr.savepoint():
            self.slot.write({"active": False})
        self.assertTrue(self.slot.active)
        self.assertEqual(self.slot.booked_count, 1)
        booking.action_cancel_booking()
        duplicate = booking.copy()
        self.assertEqual(booking.state, "cancelled")
        self.assertEqual(duplicate.state, "confirmed")
        self.assertNotEqual(duplicate.booking_ref, booking.booking_ref)
        self.assertNotEqual(duplicate.access_token, booking.access_token)
        self.assertEqual(self.slot.booked_count, 1)

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
        for quantity in (0, 4):
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

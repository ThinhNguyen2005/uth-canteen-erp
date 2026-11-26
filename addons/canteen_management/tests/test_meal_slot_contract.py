from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase
from psycopg2 import IntegrityError


class TestMealSlotContract(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        product = cls.env["product.product"].create({"name": "Test meal"})
        cls.slot_vals = {
            "name": "Test slot",
            "product_id": product.id,
            "start_at": "2026-12-01 11:00:00",
            "end_at": "2026-12-01 12:00:00",
        }

    def _slot(self, **values):
        return self.env["canteen.meal.slot"].create(dict(self.slot_vals, **values))

    def test_zero_capacity_draft_cannot_be_open(self):
        slot = self._slot(capacity=0)
        self.assertEqual(slot.state, "draft")
        with self.assertRaises((ValidationError, IntegrityError)), self.env.cr.savepoint():
            self._slot(capacity=0, state="open")
        with self.assertRaises((ValidationError, IntegrityError)), self.env.cr.savepoint():
            slot.write({"state": "open"})
        self.assertEqual(slot.state, "draft")

    def test_open_close_and_capacity(self):
        slot = self._slot(capacity=1)
        slot.action_open_slot()
        self.assertEqual(slot.state, "open")
        with self.assertRaises((ValidationError, IntegrityError)), self.env.cr.savepoint():
            slot.write({"capacity": 0})
        self.assertEqual(slot.capacity, 1)
        slot.action_close_slot()
        self.assertEqual(slot.state, "closed")
        with self.assertRaises(UserError):
            slot.action_open_slot()

    def test_inactive_slot_cannot_open(self):
        slot = self._slot(capacity=1, active=False)
        with self.assertRaises(UserError):
            slot.action_open_slot()
        self.assertEqual(slot.state, "draft")

    def test_invalid_capacity_and_time(self):
        for values in ({"capacity": -1}, {"end_at": self.slot_vals["start_at"]}):
            with self.subTest(values=values):
                with self.assertRaises((ValidationError, IntegrityError)), self.env.cr.savepoint():
                    self._slot(**values)

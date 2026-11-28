from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestBookingRoleScope(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.booking_model = cls.env["canteen.meal.booking"]
        cls.product = cls.env["product.product"].create({"name": "Role scope test meal"})
        cls.manager = cls._user("manager")
        cls.cashier = cls._user("cashier")
        cls.owner = cls._user("user")
        cls.slot = cls.env["canteen.meal.slot"].create({
            "name": "Role scope test slot",
            "product_id": cls.product.id,
            "start_at": "2099-12-01 11:00:00",
            "end_at": "2099-12-01 12:00:00",
            "capacity": 3,
        })
        cls.slot.action_open_slot()
        values = {"partner_id": cls.owner.partner_id.id, "slot_id": cls.slot.id, "state": "draft"}
        cls.allowed, cls.excluded = cls.booking_model.create([values, values])

    @classmethod
    def _user(cls, role):
        group = cls.env.ref(f"canteen_management.group_canteen_{role}")
        return cls.env["res.users"].create({
            "name": f"Booking scope {role}",
            "login": f"test_canteen_booking_scope_{role}",
            "group_ids": [(6, 0, [cls.env.ref("base.group_user").id, group.id])],
        })

    def _grant_read(self, user, scope):
        group = self.env["res.groups"].create({"name": f"Fixture Read for {user.name}"})
        user.write({"group_ids": [(4, group.id)]})
        self.env["ir.access"].create({
            "name": "Fixture Booking Read",
            "model_id": self.env["ir.model"]._get(self.booking_model._name).id,
            "group_id": group.id,
            "operation": "r",
            "domain": repr(scope),
        })

    def test_confirm_batch_preserves_out_of_scope_records(self):
        self._grant_read(self.manager, [("id", "=", self.allowed.id)])
        batch = (self.allowed | self.excluded).with_user(self.manager)
        self.assertFalse(batch.env.su)
        with self.assertRaises(AccessError), self.env.cr.savepoint():
            batch.action_confirm_booking()
        self.assertEqual((self.allowed | self.excluded).mapped("state"), ["draft", "draft"])
        self.assertEqual(self.slot.booked_count, 0)
        self.allowed.with_user(self.manager).action_confirm_booking()
        self.assertEqual(self.allowed.state, "confirmed")
        self.assertEqual(self.slot.booked_count, 1)

    def test_read_alone_does_not_authorize_workflow(self):
        self._grant_read(self.manager, [("id", "=", self.allowed.id)])
        self._grant_read(self.cashier, [("id", "=", self.allowed.id)])
        self._grant_read(self.owner, [("partner_id", "=", self.owner.partner_id.id)])
        record = self.allowed
        for user in (self.cashier, self.owner):
            user_record = record.with_user(user)
            self.assertFalse(user_record.env.su)
            self.assertTrue(user_record.has_access("read"))
            with self.assertRaises(AccessError), self.env.cr.savepoint():
                user_record.action_confirm_booking()
        record.with_user(self.manager).action_confirm_booking()
        with self.assertRaises(AccessError), self.env.cr.savepoint():
            record.with_user(self.owner).action_mark_booking_served()
        self.assertEqual(record.state, "confirmed")
        self.assertEqual(self.slot.booked_count, 1)
        record.with_user(self.cashier).action_mark_booking_served()
        self.assertEqual(record.state, "served")
        self.assertEqual(self.slot.booked_count, 1)

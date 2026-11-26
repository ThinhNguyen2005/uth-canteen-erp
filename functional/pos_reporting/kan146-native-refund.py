"""Exercise a synthetic cash refund in a fresh session on the test database."""
from decimal import Decimal

assert env.cr.dbname == "uth_kan151_152_test_20261126"
original = env["pos.order"].browse(9).exists()
assert original and original.state == "done" and original.currency_id.name == "USD"
assert not original.lines.filtered(lambda line: line.refunded_qty)
config = original.session_id.config_id
assert not config.current_session_id
config.with_user(env.ref("base.user_admin")).open_ui()
session = config.current_session_id
session.set_opening_control(100000, "KAN146 refund test")
refund = env["pos.order"].browse(original.refund()["res_id"])
assert refund.session_id == session and Decimal(str(refund.amount_total)) == Decimal("-40000")
cash = config.payment_method_ids.filtered(lambda item: item.type == "cash")
assert len(cash) == 1
ctx = {"active_ids": refund.ids, "active_id": refund.id}
payment = env["pos.make.payment"].with_context(**ctx).create({"amount": -40000, "payment_method_id": cash.id})
payment.with_context(**ctx).check()
assert refund.state == "paid" and Decimal(str(refund.amount_paid)) == Decimal("-40000")
env.cr.commit()
print("KAN146_REFUND_OK original", original.id, "refund", refund.id, "session", session.id, "total", refund.amount_total, "state", refund.state)

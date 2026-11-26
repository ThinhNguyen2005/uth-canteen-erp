"""Read-only checks for five synthetic sales in the isolated Odoo database."""
from decimal import Decimal

assert env.cr.dbname == "uth_kan151_152_test_20261126"
cases = [(9, 1, "cash", 40000), (10, 2, "cash", 55000),
         (1, 1, "bank", 40000), (2, 2, "bank", 55000), (31, 1, "bank", 36000)]
for order_id, lines, kind, total in cases:
    order = env["pos.order"].browse(order_id).exists()
    assert order and order.state == "done" and order.session_id.state == "closed"
    assert len(order.lines) == lines and len(order.payment_ids) == 1
    assert order.payment_ids.payment_method_id.type == kind
    assert Decimal(str(order.amount_total)) == Decimal(total)
    assert Decimal(str(order.amount_paid)) == Decimal(total)
    assert order.currency_id.name == "USD"
cancelled = env["pos.order"].browse(32).exists()
assert cancelled and cancelled.state == "cancel" and not cancelled.payment_ids
refund = env["pos.order"].browse(33).exists()
assert refund and refund.state == "done" and refund.amount_total == -40000 and refund.amount_paid == -40000
assert refund.session_id.state == "closed" and refund.payment_ids.payment_method_id.type == "cash"
print("KAN146_ORM_OK five sales, cancelled draft and cash refund; USD synthetic test")

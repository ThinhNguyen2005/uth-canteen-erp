"""Read-only regression against committed synthetic POS orders and pricelist."""
from decimal import Decimal

assert env.cr.dbname == "uth_kan151_152_test_20261126"
session = env["pos.session"].browse(1).exists()
orders = env["pos.order"].search([("session_id", "=", session.id)], order="id")
assert len(orders) == 30 and all(o.state == "paid" for o in orders)
assert sum(Decimal(str(o.amount_total)) for o in orders) == Decimal("1425000")
assert sum(Decimal(str(o.amount_paid)) for o in orders) == Decimal("1425000")
payments = env["pos.payment"].search([("pos_order_id", "in", orders.ids)])
assert len(payments) == 30
assert len(payments.filtered(lambda p: p.payment_method_id.name == "KAN151 Cash Test")) == 22
assert len(payments.filtered(lambda p: p.payment_method_id.name == "KAN151 Transfer Simulation")) == 8
pricelist = env["product.pricelist"].search([("name", "=", "KAN152 Student Test")], limit=1)
a = env["product.product"].search([("default_code", "=", "KAN151-A")], limit=1)
b = env["product.product"].search([("default_code", "=", "KAN151-B")], limit=1)
assert [pricelist._get_product_price(a, 1), pricelist._get_product_price(a, 2), pricelist._get_product_price(b, 2)] == [20000, 18000, 35000]
discounted = env["pos.order"].browse(31).exists()
assert discounted and discounted.state == "paid" and discounted.amount_total == 36000 and discounted.amount_paid == 36000
assert discounted.pricelist_id == pricelist and len(discounted.lines) == 1 and discounted.lines.qty == 2 and discounted.lines.price_unit == 18000
cancelled = env["pos.order"].browse(32).exists()
assert cancelled and cancelled.state == "cancel" and not cancelled.payment_ids
assert len(cancelled.lines) == 1 and cancelled.lines.qty == 2 and cancelled.amount_total == 40000
print("REGRESSION_ORM_OK: 30 paid orders, totals, pricelist, discounted sale and edited cancelled draft")

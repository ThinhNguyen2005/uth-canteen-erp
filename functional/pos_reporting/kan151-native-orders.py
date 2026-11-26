"""Generate and reconcile thirty synthetic POS orders through Odoo ORM."""
from decimal import Decimal
from odoo import Command

assert env.cr.dbname == "uth_kan151_152_test_20261126"
pos = env["pos.config"].search([("name", "=", "KAN151 Test POS")], limit=1)
session = pos.current_session_id
assert session and session.state == "opened"
assert not env["pos.order"].search_count([("session_id", "=", session.id)])
products = env["product.product"].search([("default_code", "in", ["KAN151-A", "KAN151-B"])], order="default_code")
assert len(products) == 2
cash = env["pos.payment.method"].search([("name", "=", "KAN151 Cash Test")], limit=1)
bank = env["pos.payment.method"].search([("name", "=", "KAN151 Transfer Simulation")], limit=1)
assert cash and bank
expected_sum = Decimal("0")
ids = []
for n in range(1, 31):
    items = [(products[0], 1 + n % 2)]
    if n % 2 == 0:
        items.append((products[1], 1))
    expected = sum(Decimal(str(p.lst_price)) * q for p, q in items)
    order = env["pos.order"].create({
        "company_id": pos.company_id.id, "session_id": session.id,
        "amount_paid": 0, "amount_total": float(expected), "amount_tax": 0, "amount_return": 0,
        "lines": [Command.create({"product_id": p.id, "qty": q, "price_unit": p.lst_price, "price_subtotal": p.lst_price * q, "price_subtotal_incl": p.lst_price * q, "tax_ids": [Command.clear()]}) for p, q in items],
    })
    order.lines._onchange_amount_line_all()
    order._compute_prices()
    assert Decimal(str(order.amount_total)) == expected, (n, order.amount_total, expected)
    ctx = {"active_ids": order.ids, "active_id": order.id}
    pay = env["pos.make.payment"].with_context(**ctx).create({"amount": float(expected), "payment_method_id": (bank if n <= 8 else cash).id})
    pay.with_context(**ctx).check()
    assert order.state in ("paid", "done") and Decimal(str(order.amount_paid)) == expected
    ids.append(order.id)
    expected_sum += expected
assert len(ids) == len(set(ids)) == 30
env.cr.commit()
print("KAN151_ORM_ORDERS", ids, "EXPECTED_TOTAL", str(expected_sum), "CASH_COUNT", 22, "SIMULATED_BANK_COUNT", 8)

"""Test editing and cancelling a new synthetic draft in the test database."""
from odoo import Command

assert env.cr.dbname == "uth_kan151_152_test_20261126"
session = env["pos.session"].browse(2).exists()
product = env["product.product"].search([("default_code", "=", "KAN151-A")], limit=1)
assert session and session.state == "opened" and product
order = env["pos.order"].create({"company_id": session.company_id.id, "session_id": session.id, "amount_paid": 0, "amount_total": 20000, "amount_tax": 0, "amount_return": 0, "lines": [Command.create({"product_id": product.id, "qty": 1, "price_unit": 20000, "price_subtotal": 20000, "price_subtotal_incl": 20000, "tax_ids": [Command.clear()]})]})
assert order.state == "draft"
order.lines.write({"qty": 2})
order.lines._onchange_amount_line_all()
order._compute_prices()
assert order.amount_total == 40000
order.with_context(active_ids=order.ids).action_pos_order_cancel()
assert order.state == "cancel" and not order.payment_ids
env.cr.commit()
print("DRAFT_EDIT_CANCEL_OK order", order.id, "state", order.state, "payments", len(order.payment_ids))

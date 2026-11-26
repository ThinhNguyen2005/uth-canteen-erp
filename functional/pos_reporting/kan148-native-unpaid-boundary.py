"""Verify an unpaid synthetic order cannot be marked paid."""
from odoo import Command
from odoo.exceptions import UserError

assert env.cr.dbname == "uth_kan151_152_test_20261126"
session = env["pos.session"].browse(7).exists()
assert session and session.state == "opened" and session.config_id.name == "KAN147 Test VND POS"
company = session.config_id.company_id
product = env["product.product"].with_company(company).search([("default_code", "=", "UTH-RICE-01"), ("company_id", "=", company.id)])
assert len(product) == 1
order = env["pos.order"].with_company(company).create({"company_id": company.id, "session_id": session.id, "amount_paid": 0, "amount_total": 35000, "amount_tax": 0, "amount_return": 0, "lines": [Command.create({"product_id": product.id, "qty": 1, "price_unit": 35000, "price_subtotal": 35000, "price_subtotal_incl": 35000, "tax_ids": [Command.clear()]})]})
try:
    order.action_pos_order_paid()
except UserError:
    pass
else:
    raise AssertionError("Unpaid order was unexpectedly marked paid")
assert order.state == "draft" and not order.payment_ids
order.with_context(active_ids=order.ids).action_pos_order_cancel()
assert order.state == "cancel"
env.cr.commit()
print("KAN148_UNPAID_BLOCKED order", order.id, "cancelled_after_check")

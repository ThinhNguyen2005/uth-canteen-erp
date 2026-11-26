"""Exercise a manually selected synthetic pricelist in a separate test POS."""
from odoo import Command

assert env.cr.dbname == "uth_kan151_152_test_20261126"
assert not env["pos.config"].search_count([("name", "=", "KAN152 Student Test POS")])
pricelist = env["product.pricelist"].search([("name", "=", "KAN152 Student Test")], limit=1)
product = env["product.product"].search([("default_code", "=", "KAN151-A")], limit=1)
bank = env["pos.payment.method"].search([("name", "=", "KAN151 Transfer Simulation")], limit=1)
assert pricelist and product and bank
pos = env["pos.config"].create({"name": "KAN152 Student Test POS", "company_id": env.company.id, "use_pricelist": True, "pricelist_id": pricelist.id, "available_pricelist_ids": [Command.set(pricelist.ids)], "payment_method_ids": [Command.set(bank.ids)]})
pos.with_user(env.ref("base.user_admin")).open_ui()
session = pos.current_session_id
session.set_opening_control(0, "KAN152 simulated payment")
price = pricelist._get_product_price(product, 2)
assert price == 18000
order = env["pos.order"].create({"company_id": pos.company_id.id, "session_id": session.id, "pricelist_id": pricelist.id, "amount_paid": 0, "amount_total": 36000, "amount_tax": 0, "amount_return": 0, "lines": [Command.create({"product_id": product.id, "qty": 2, "price_unit": price, "price_subtotal": 36000, "price_subtotal_incl": 36000, "tax_ids": [Command.clear()]})]})
order.lines._onchange_amount_line_all()
order._compute_prices()
assert order.amount_total == 36000
ctx = {"active_ids": order.ids, "active_id": order.id}
payment = env["pos.make.payment"].with_context(**ctx).create({"amount": 36000, "payment_method_id": bank.id})
payment.with_context(**ctx).check()
assert order.state == "paid" and order.amount_paid == 36000
env.cr.commit()
print("KAN152_POS_ORDER", order.id, "session", session.id, "total", order.amount_total, "state", order.state)

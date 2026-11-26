"""Sell one reference SKU in a separate synthetic VND company via Odoo ORM."""
import csv
import os
from decimal import Decimal
from odoo import Command

assert env.cr.dbname == "uth_kan151_152_test_20261126"
company = env["res.company"].search([("name", "=", "KAN147 Test VND")])
assert len(company) == 1 and company.currency_id.name == "VND"
assert not env["pos.config"].search_count([("name", "=", "KAN147 Test VND POS")])
with open(os.environ["KAN147_PRICE_CSV"], encoding="utf-8-sig", newline="") as f:
    row = next(csv.DictReader(f))
product = env["product.product"].with_company(company).search([("company_id", "=", company.id), ("default_code", "=", row["sku"])])
assert len(product) == 1 and Decimal(str(product.list_price)) == Decimal(row["gia_tham_khao_vnd"])
journal = env["account.journal"].with_company(company).search([("company_id", "=", company.id), ("type", "=", "cash")], limit=1)
assert journal
cash = env["pos.payment.method"].with_company(company).create({"name": "KAN147 Test VND Cash", "company_id": company.id, "type": "cash", "journal_id": journal.id})
pos = env["pos.config"].with_company(company).create({"name": "KAN147 Test VND POS", "company_id": company.id, "payment_method_ids": [Command.set(cash.ids)]})
pos.with_user(env.ref("base.user_admin")).sudo().with_company(company).open_ui()
session = pos.current_session_id
session.set_opening_control(0, "KAN147 synthetic test")
price = product.list_price
order = env["pos.order"].with_company(company).create({"company_id": company.id, "session_id": session.id, "amount_paid": 0, "amount_total": price, "amount_tax": 0, "amount_return": 0, "lines": [Command.create({"product_id": product.id, "qty": 1, "price_unit": price, "price_subtotal": price, "price_subtotal_incl": price, "tax_ids": [Command.clear()]})]})
order.lines._onchange_amount_line_all()
order._compute_prices()
assert Decimal(str(order.amount_total)) == Decimal(row["gia_tham_khao_vnd"])
ctx = {"active_ids": order.ids, "active_id": order.id}
payment = env["pos.make.payment"].with_company(company).with_context(**ctx).create({"amount": price, "payment_method_id": cash.id})
payment.with_context(**ctx).check()
assert order.state == "paid" and order.amount_paid == price and order.currency_id.name == "VND"
env.cr.commit()
print("KAN147_VND_SALE_OK", "order", order.id, "sku", row["sku"], "price", price, "state", order.state)

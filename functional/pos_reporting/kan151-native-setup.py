"""Create POS fixtures only in the explicitly designated isolated database."""
from odoo import Command

assert env.cr.dbname == "uth_kan151_152_test_20261126"
assert not env["pos.config"].search_count([("name", "=", "KAN151 Test POS")])
company = env.company
cash_journal = env["account.journal"].create({"name": "KAN151 Test Cash", "code": "K151C", "type": "cash", "company_id": company.id})
bank_journal = env["account.journal"].search([("company_id", "=", company.id), ("type", "=", "bank")], limit=1)
assert bank_journal
cash = env["pos.payment.method"].create({"name": "KAN151 Cash Test", "type": "cash", "journal_id": cash_journal.id})
bank = env["pos.payment.method"].create({"name": "KAN151 Transfer Simulation", "type": "bank", "journal_id": bank_journal.id})
pos = env["pos.config"].create({"name": "KAN151 Test POS", "company_id": company.id, "payment_method_ids": [Command.set([cash.id, bank.id])]})
products = env["product.product"].create([
    {"name": "KAN151 Test Item A", "default_code": "KAN151-A", "list_price": 20000, "available_in_pos": True, "taxes_id": [Command.clear()]},
    {"name": "KAN151 Test Item B", "default_code": "KAN151-B", "list_price": 35000, "available_in_pos": True, "taxes_id": [Command.clear()]},
])
pos.with_user(env.ref("base.user_admin")).open_ui()
session = pos.current_session_id
session.set_opening_control(100000, "KAN151 synthetic test")
assert session.state == "opened"
env.cr.commit()
print("SETUP", "pos", pos.id, "session", session.id, "cash", cash.id, "transfer", bank.id, "products", products.ids)

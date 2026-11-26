"""Check draft-order blocking and close the synthetic refund session."""
from odoo import Command

assert env.cr.dbname == "uth_kan151_152_test_20261126"
session = env["pos.session"].browse(6).exists()
assert session and session.state == "opened" and session.config_id.name == "KAN151 Test POS"
refund = env["pos.order"].browse(33).exists()
assert refund and refund.state == "paid" and refund.amount_total == -40000
product = env["product.product"].search([("default_code", "=", "KAN151-A")], limit=1)
draft = env["pos.order"].create({"company_id": session.company_id.id, "session_id": session.id, "amount_paid": 0, "amount_total": 20000, "amount_tax": 0, "amount_return": 0, "lines": [Command.create({"product_id": product.id, "qty": 1, "price_unit": 20000, "price_subtotal": 20000, "price_subtotal_incl": 20000, "tax_ids": [Command.clear()]})]})
cash = session.payment_method_ids.filtered(lambda p: p.type == "cash")
bank = session.payment_method_ids.filtered(lambda p: p.type == "bank")
blocked = session.close_session_from_ui({cash.id: 60000, bank.id: 0})
assert blocked.get("status") is False and blocked.get("type") == "draft_orders"
assert session.state == "opened" and draft.state == "draft"
draft.with_context(active_ids=draft.ids).action_pos_order_cancel()
assert draft.state == "cancel" and not draft.payment_ids
assert session.close_session_from_ui({cash.id: 60000, bank.id: 0}).get("status") is True
assert session.state == "closed" and refund.state == "done" and draft.state == "cancel"
env.cr.commit()
print("KAN148_DRAFT_BLOCK_AND_REFUND_CLOSE_OK", "session", session.id, "refund", refund.id, "cancelled", draft.id)

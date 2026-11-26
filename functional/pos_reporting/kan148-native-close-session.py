"""Close the isolated synthetic bank-payment session and verify its state."""
assert env.cr.dbname == "uth_kan151_152_test_20261126"
session = env["pos.session"].browse(2).exists()
assert session and session.state == "opened"
assert session.config_id.name == "KAN152 Student Test POS"
paid = session.order_ids.filtered(lambda order: order.state == "paid")
cancelled = session.order_ids.filtered(lambda order: order.state == "cancel")
assert len(paid) == 1 and paid.amount_total == 36000 and len(cancelled) == 1
method = session.payment_method_ids.filtered(lambda item: item.type == "bank")
assert len(method) == 1
result = session.close_session_from_ui({method.id: 36000})
assert result.get("status") is True and session.state == "closed"
assert paid.state == "done" and cancelled.state == "cancel"
second = session.close_session_from_ui({method.id: 36000})
assert second.get("status") is False and second.get("type") == "session_already_closed"
env.cr.commit()
print("KAN148_CLOSED session=2 paid=36000 cancelled=1 duplicate_close=blocked")

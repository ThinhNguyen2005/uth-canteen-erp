"""Exercise isolated test-session closing and three cash-count variances."""
assert env.cr.dbname == "uth_kan151_152_test_20261126"
session = env["pos.session"].browse(1).exists()
assert session and session.state == "opened" and session.config_id.name == "KAN151 Test POS"
assert len(session.order_ids.filtered(lambda x: x.state == "paid")) == 30
cash = session.payment_method_ids.filtered(lambda x: x.type == "cash")
bank = session.payment_method_ids.filtered(lambda x: x.type == "bank")
assert len(cash) == len(bank) == 1
assert session.close_session_from_ui({cash.id: 1145000, bank.id: 380000}).get("status") is True
assert session.state == "closed"
assert len(session.order_ids.filtered(lambda x: x.state == "done")) == 30
config = session.config_id
results = []
for counted in (99000, 101000, 90000):
    config.with_user(env.ref("base.user_admin")).open_ui()
    s = config.current_session_id
    s.set_opening_control(100000, "KAN148 variance test")
    assert s.state == "opened"
    assert s.close_session_from_ui({cash.id: counted, bank.id: 0}).get("status") is True
    assert s.state == "closed"
    results.append((s.id, counted, counted - 100000))
env.cr.commit()
print("KAN148_CASH_VARIANCE", results, "original_session_closed", session.id)

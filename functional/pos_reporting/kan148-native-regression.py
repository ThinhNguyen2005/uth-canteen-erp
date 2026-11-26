"""Read-only verification of closed synthetic sessions and adjustments."""
from decimal import Decimal

assert env.cr.dbname == "uth_kan151_152_test_20261126"
sessions = env["pos.session"].browse([1, 2, 3, 4, 5]).exists()
assert len(sessions) == 5 and all(s.state == "closed" for s in sessions)
orders = env["pos.order"].search([("session_id", "=", 1)])
assert len(orders) == 30 and all(order.state == "done" for order in orders)
assert sum(Decimal(str(order.amount_total)) for order in orders) == Decimal("1425000")
assert env["pos.order"].browse(31).state == "done" and env["pos.order"].browse(32).state == "cancel"
for session_id, adjustment, counted in [(3, -1000, 99000), (4, 1000, 101000), (5, -10000, 90000)]:
    s = env["pos.session"].browse(session_id)
    statement = s.bank_statement_id
    assert statement and Decimal(str(statement.balance_end_real)) == Decimal(counted)
    assert any(Decimal(str(line.amount)) == Decimal(adjustment) for line in statement.line_ids)
print("KAN148_REGRESSION_OK 5 closed sessions, 30 completed orders and 3 recorded cash adjustments")

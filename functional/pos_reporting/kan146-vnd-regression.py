"""Read-only regression check for KAN-146 POS-01..POS-05 in VND on Odoo 20."""
from decimal import Decimal

assert env.cr.dbname == "uth_kan151_152_test_20261126"

# POS-01: Session 9, Order 38 (40,000 VND cash, closed cleanly at 140,000)
s9 = env["pos.session"].browse(9).exists()
o38 = env["pos.order"].browse(38).exists()
assert s9 and s9.state == "closed" and s9.currency_id.name == "VND"
assert o38 and o38.state == "done" and Decimal(str(o38.amount_total)) == Decimal("40000")
assert Decimal(str(s9.bank_statement_id.balance_end_real)) == Decimal("140000")

# POS-02: Session 10, Order 39 (edited to 20,000 VND then cancelled, 0 payments)
s10 = env["pos.session"].browse(10).exists()
o39 = env["pos.order"].browse(39).exists()
assert s10 and s10.state == "closed"
assert o39 and o39.state == "cancel" and not o39.payment_ids and Decimal(str(o39.amount_total)) == Decimal("20000")

# POS-03: Session 11, Order 40 (30,000 VND simulated bank transfer, exactly 1 payment)
s11 = env["pos.session"].browse(11).exists()
o40 = env["pos.order"].browse(40).exists()
assert s11 and s11.state == "closed"
assert o40 and o40.state == "done" and len(o40.payment_ids) == 1
assert o40.payment_ids.payment_method_id.type == "bank" and Decimal(str(o40.amount_total)) == Decimal("30000")

# POS-04: Session 12, Order 41 (40,000) + partial Refund 42 (-20,000) linked to original line
s12 = env["pos.session"].browse(12).exists()
o41 = env["pos.order"].browse(41).exists()
o42 = env["pos.order"].browse(42).exists()
assert s12 and s12.state == "closed"
assert o41 and o41.state == "done" and Decimal(str(o41.amount_total)) == Decimal("40000")
assert o42 and o42.state == "done" and Decimal(str(o42.amount_total)) == Decimal("-20000")
assert o42.lines.refunded_orderline_id == o41.lines[0]
assert Decimal(str(s12.bank_statement_id.balance_end_real)) == Decimal("120000")

# POS-05: Session 13, Order 43 (40,000 cash, 1 payment) + closing variance -1,000 VND
s13 = env["pos.session"].browse(13).exists()
o43 = env["pos.order"].browse(43).exists()
assert s13 and s13.state == "closed"
assert o43 and o43.state == "done" and len(o43.payment_ids) == 1
assert Decimal(str(s13.bank_statement_id.balance_end_real)) == Decimal("139000")
assert any(Decimal(str(l.amount)) == Decimal("-1000") for l in s13.bank_statement_id.line_ids)

print("KAN146_VND_REGRESSION_OK POS-01..POS-05 verified on Odoo 20 (VND)")

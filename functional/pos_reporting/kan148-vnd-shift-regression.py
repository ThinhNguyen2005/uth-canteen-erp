"""Read-only regression check for KAN-148 CL-01..CL-04 cash shifts in VND."""
from decimal import Decimal

assert env.cr.dbname == "uth_kan151_152_test_20261126"

expected = [
    ("CL-01", 15, 46, 140000, 0),
    ("CL-02", 16, 47, 139000, -1000),
    ("CL-03", 17, 48, 141000, 1000),
    ("CL-04", 18, 49, 130000, -10000),
]
for cl_id, sid, oid, counted, diff in expected:
    s = env["pos.session"].browse(sid).exists()
    o = env["pos.order"].browse(oid).exists()
    assert s and s.state == "closed" and s.currency_id.name == "VND", cl_id
    assert o and o.state == "done" and Decimal(str(o.amount_total)) == Decimal("40000"), cl_id
    stmt = s.bank_statement_id
    assert stmt and Decimal(str(stmt.balance_end_real)) == Decimal(str(counted)), cl_id
    if diff != 0:
        assert any(Decimal(str(l.amount)) == Decimal(str(diff)) for l in stmt.line_ids), cl_id

print("KAN148_VND_SHIFT_REGRESSION_OK CL-01..CL-04 verified on Odoo 20 (VND)")

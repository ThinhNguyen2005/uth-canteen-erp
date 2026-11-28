"""Read-only regression check for KAN-147 20-SKU VND catalog and POS sales."""
import csv
import os
from decimal import Decimal

assert env.cr.dbname == "uth_kan151_152_test_20261126"
company = env["res.company"].search([("name", "=", "KAN147 Test VND")], limit=1)
assert company and company.currency_id.name == "VND"

with open(os.environ["KAN147_PRICE_CSV"], encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 20

for row in rows:
    p = env["product.product"].with_company(company).search(
        [("company_id", "=", company.id), ("default_code", "=", row["sku"])]
    )
    assert len(p) == 1
    assert p.name == row["ten_san_pham"]
    assert p.uom_id == env.ref(row["don_vi_nguon"])
    assert p.available_in_pos and Decimal(str(p.list_price)) == Decimal(row["gia_tham_khao_vnd"])

s14 = env["pos.session"].browse(14).exists()
o44 = env["pos.order"].browse(44).exists()
o45 = env["pos.order"].browse(45).exists()
assert s14 and s14.state == "closed" and Decimal(str(s14.bank_statement_id.balance_end_real)) == Decimal("440000")
assert o44 and o44.state == "done" and len(o44.lines) == 13 and Decimal(str(o44.amount_total)) == Decimal("340000")
assert o45 and o45.state == "done" and len(o45.lines) == 7 and Decimal(str(o45.amount_total)) == Decimal("191000")
assert set(o44.lines.mapped("product_id.default_code")) | set(o45.lines.mapped("product_id.default_code")) == {r["sku"] for r in rows}

print("KAN147_VND_20SKU_REGRESSION_OK 20 SKUs, Order #44 (340000 VND) and Order #45 (191000 VND) verified")

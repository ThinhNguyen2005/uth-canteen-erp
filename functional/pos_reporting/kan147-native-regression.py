"""Read-only catalog comparison in the isolated test company."""
import csv
import os
from decimal import Decimal

assert env.cr.dbname == "uth_kan151_152_test_20261126"
with open(os.environ["KAN147_PRICE_CSV"], encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))
company = env["res.company"].search([("name", "=", "KAN147 Test VND")])
assert len(company) == 1 and company.currency_id.name == "VND" and len(rows) == 20
for row in rows:
    products = env["product.product"].with_company(company).search([("default_code", "=", row["sku"]), ("company_id", "=", company.id)])
    assert len(products) == 1
    p = products[0]
    assert p.name == row["ten_san_pham"] and p.uom_id == env.ref(row["don_vi_nguon"])
    assert p.available_in_pos and Decimal(str(p.list_price)) == Decimal(row["gia_tham_khao_vnd"])
print("KAN147_REGRESSION_OK 20 unique SKU, names, UoM, POS flag and reference prices")

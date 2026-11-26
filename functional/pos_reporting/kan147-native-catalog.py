"""Load and validate the TV2 reference snapshot in a separate test company."""
import csv
import os
from decimal import Decimal
from odoo import Command

assert env.cr.dbname == "uth_kan151_152_test_20261126"
with open(os.environ["KAN147_PRICE_CSV"], encoding="utf-8-sig", newline="") as stream:
    rows = list(csv.DictReader(stream))
assert len(rows) == 20 and len({r["sku"] for r in rows}) == 20
assert not env["res.company"].search_count([("name", "=", "KAN147 Test VND")])
for row in rows:
    assert row["external_id"] and row["sku"] and Decimal(row["gia_tham_khao_vnd"]) > 0
    assert env.ref(row["don_vi_nguon"])
    assert not env["product.product"].search_count([("default_code", "=", row["sku"])])
company = env["res.company"].create({"name": "KAN147 Test VND", "currency_id": env.ref("base.VND").id, "country_id": env.ref("base.vn").id})
model = env["product.product"].with_company(company)
created = model.create([{
    "name": row["ten_san_pham"], "default_code": row["sku"],
    "company_id": company.id, "uom_id": env.ref(row["don_vi_nguon"]).id,
    "list_price": float(Decimal(row["gia_tham_khao_vnd"])),
    "available_in_pos": True, "taxes_id": [Command.clear()],
} for row in rows])
by_sku = {p.default_code: p for p in created}
assert company.currency_id == env.ref("base.VND") and len(by_sku) == 20
for row in rows:
    p = by_sku[row["sku"]]
    assert p.name == row["ten_san_pham"] and p.uom_id == env.ref(row["don_vi_nguon"])
    assert Decimal(str(p.list_price)) == Decimal(row["gia_tham_khao_vnd"]) and p.available_in_pos
env.cr.commit()
print("KAN147_CATALOG_TEST company", company.id, "currency", company.currency_id.name, "products", len(created), "sku_and_price_matches", len(rows))

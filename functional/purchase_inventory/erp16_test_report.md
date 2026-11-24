# ERP-16 – CSV Import Test Report

## 1. Test information

- Jira Task: ERP-16
- Responsible: TV2 – Purchase & Inventory
- Database used for the earlier import: `uth_canteen_erp13_test`
- Earlier execution date: 2026-11-23
- Current status: **Pending re-test after TV1 Request Changes**

## 2. Earlier test results (before review fixes)

The earlier test run imported the original `products.csv` into `product.template` and verified 20 products, unique SKUs and POS availability. Those results are retained as historical evidence only.

They do **not** validate the corrected External IDs, the `product.product` target model, or the two canteen-specific fields. The earlier PASS results must not be treated as acceptance of this revised CSV.

## 3. Required re-test

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| Import products.csv into `product.product` | 20 product variants resolve/import | Not yet executed | PENDING |
| Resolve 13 canonical product External IDs | Existing XML variants are updated; no duplicate variants | Not yet executed | PENDING |
| Verify product fields | 20 rows have `canteen_published=True` and valid `canteen_category` | Not yet executed | PENDING |
| Unique SKU validation | 20 unique SKUs | Not yet executed | PENDING |
| Re-import products.csv | No additional product variants | Not yet executed | PENDING |
| Import suppliers.csv | Five contacts resolve using the same IDs as `demo_suppliers.csv` | Not yet executed | PENDING |
| Re-import suppliers.csv | No duplicate supplier contacts | Not yet executed | PENDING |

## 4. Evidence required

Capture updated Odoo evidence after re-testing:

- Product Variant import preview showing the target model and External ID mapping.
- Import result showing the 13 canonical IDs were matched to existing variants.
- Product list or SQL evidence showing 20 unique SKUs and both canteen fields.
- Before/after counts proving product re-import does not create duplicates.
- Supplier import preview/result and before/after counts proving the five canonical supplier IDs resolve without duplicates.

## 5. Limitations

- Supplier details are fictional test data.
- Product list prices are POS selling prices, not supplier purchase prices.
- Product costs and recipe costing are outside this task's import scope.
- The revised import has not yet been executed; no new PASS result is claimed.

## 6. Conclusion

The four review corrections have been applied to the CSV files and import documentation. ERP-16 remains **Pending re-test and TV1 re-review** until the required Odoo checks and evidence are completed.

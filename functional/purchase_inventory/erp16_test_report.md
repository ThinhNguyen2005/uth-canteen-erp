# ERP-16 – CSV Import Test Report

## 1. Test information

- Jira Task: ERP-16
- Responsible: TV2 – Purchase & Inventory
- Database: `uth_canteen_erp13_test`
- Verification date: 2026-11-24
- Current status: **Pending corrected CSV import and evidence**

## 2. Database inspection

Read-only SQL inspection of the current database established:

- There are 20 UTH product templates and 20 distinct SKUs.
- All 20 product External IDs are in module `__import__` and point to model `product.template`.
- The 13 IDs previously changed to `canteen_management.*` are not present in `ir_model_data` in this database.
- `available_in_pos` exists on `product.template`.
- `canteen_published` and `canteen_category` are not registered fields on either `product.template` or `product.product`.

The corrected CSV and guide therefore retain the existing `__import__.*` identifiers, target `product.template`, and omit the two unsupported canteen fields.

## 3. Required import re-test

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| Test products.csv against `product.template` | All 20 External IDs resolve to existing templates | Not yet executed | PENDING |
| Import products.csv | Existing 20 templates updated; no new products | Not yet executed | PENDING |
| Unique SKU validation | 20 unique SKUs | 20 unique SKUs observed before import | PARTIAL |
| POS availability | `available_in_pos` field exists on product.template | Field existence confirmed; CSV import not tested | PARTIAL |
| Re-import products.csv | No additional product templates | Not yet executed | PENDING |
| Test/import suppliers.csv | Five existing supplier contacts resolve and update | Not yet executed | PENDING |
| Re-import suppliers.csv | No duplicate supplier contacts | Not yet executed | PENDING |

## 4. Evidence required

Capture updated Odoo evidence after the corrected import:

- Product import preview showing target model `product.template` and External ID mapping.
- Import result showing the 20 existing External IDs resolve.
- Product list or SQL evidence showing 20 unique SKUs after import.
- Before/after counts proving product import and re-import do not create duplicates.
- Supplier import preview/result and before/after counts proving the five supplier IDs resolve without duplicates.

## 5. Limitations

- Supplier details are fictional test data.
- Product list prices are POS selling prices, not supplier purchase prices.
- Product costs and recipe costing are outside this task's import scope.
- Database inspection is not a substitute for executing the corrected CSV import. No new import PASS is claimed.

## 6. Conclusion

The CSV contract and guide have been corrected to match the observed database model and External IDs. ERP-16 remains **Pending corrected import re-test, evidence capture and TV1 re-review**.

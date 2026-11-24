# ERP-16 – CSV Import Test Report

## 1. Test information

- Jira Task: ERP-16
- Responsible: TV2 – Purchase & Inventory
- Database: `uth_canteen_erp13_test`
- Verification date: 2026-11-24
- Current status: **Import tests PASS; evidence capture, re-import test and TV1 re-review pending**

## 2. Database inspection and CSV validation

Read-only inspection and local CSV validation established:

- `products.csv` contains 20 products, 20 unique SKUs and 20 unique External IDs.
- All 20 product External IDs are in module `__import__` and point to model `product.template`.
- The 13 IDs previously changed to `canteen_management.*` are not present in `ir_model_data` in this database.
- `available_in_pos` exists on `product.template`.
- `canteen_published` and `canteen_category` are not registered fields on either `product.template` or `product.product`.
- `suppliers.csv` contains five suppliers and five unique External IDs.
- All five supplier External IDs already resolve to `res.partner` records in the `__import__` namespace.

The corrected CSV and guide retain the existing External IDs, target `product.template` for products, and omit the two unsupported canteen fields.

## 3. Import test results

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| Local products.csv validation | 20 rows, unique SKUs and External IDs | 20 rows; 20 unique SKUs; 20 unique External IDs | PASS |
| Odoo Test products.csv | All 20 External IDs resolve without validation errors | Odoo displayed “Everything seems valid.”; mappings resolved to Product fields | PASS |
| Import products.csv | Existing 20 templates updated; no additional UTH products | Post-import SQL: 20 UTH templates and 20 unique SKUs | PASS |
| Product External ID integrity | 20 IDs link to 20 distinct product templates | 20 linked External IDs, 20 linked products, 20 unique SKUs | PASS |
| Local suppliers.csv validation | Five rows and five unique External IDs | Five suppliers and five unique External IDs | PASS |
| Odoo Test suppliers.csv | All five External IDs resolve without validation errors | Odoo displayed “Everything seems valid.”; all nine columns mapped | PASS |
| Import suppliers.csv | Existing five supplier contacts updated | Post-import SQL: 5 linked suppliers, 5 distinct partners, 5 with supplier_rank > 0 | PASS |
| Supplier field verification | Supplier rank, customer rank and contact fields match CSV | All five rows show supplier_rank=1, customer_rank=0; email, phone, street, city and VAT match the CSV | PASS |
| Re-import products.csv | No additional product templates | Not yet executed as a separate second import | PENDING |
| Re-import suppliers.csv | No duplicate supplier contacts | Not yet executed as a separate second import | PENDING |

## 4. Evidence required

Capture and commit updated Odoo evidence:

- Product import preview showing Product model and External ID mapping.
- Product Test Import success message.
- Product import completion result.
- SQL evidence showing 20 UTH templates, 20 unique SKUs and 20 External IDs linked to 20 product templates.
- Supplier import preview showing all nine mappings.
- Supplier Test Import success message and import completion result.
- SQL evidence showing five linked suppliers and the imported contact fields.
- If re-import tests are executed, capture before/after counts proving no duplicates.

## 5. Limitations

- Supplier details are fictional test data.
- Product list prices are POS selling prices, not supplier purchase prices.
- Product costs and recipe costing are outside this task's import scope.
- A separate second import/re-import test has not yet been performed.
- Import success and SQL verification do not replace evidence capture or TV1 review.

## 6. Conclusion

The corrected product and supplier CSV files both passed Odoo Test Import and were imported successfully into the test database. SQL verification confirms 20 product templates remain linked to 20 product External IDs and five supplier contacts remain linked to five supplier External IDs, with the supplier fields matching the CSV.

ERP-16 is **Pending evidence capture, separate re-import checks and TV1 re-review**. Do not mark the task Done or the PR accepted until the remaining acceptance steps are completed.

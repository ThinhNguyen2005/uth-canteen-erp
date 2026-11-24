# ERP-16 – CSV Import Test Report

## 1. Test information

- Jira Task: ERP-16
- Responsible: TV2 – Purchase & Inventory
- Database: `uth_canteen_erp13_test`
- Verification date: 2026-11-24
- Current status: **Import tests PASS; four screenshots captured; TV1 re-review pending**

## 2. Database inspection and CSV validation

Read-only inspection and local CSV validation established:

- `products.csv` contains 20 products, 20 unique SKUs and 20 unique External IDs.
- All 20 product External IDs are in module `__import__` and point to model `product.template`.
- The 13 IDs previously changed to `canteen_management.*` are not present in `ir_model_data` in this database.
- `available_in_pos` exists on `product.template`.
- `canteen_published` and `canteen_category` are not registered fields on either `product.template` or `product.product`.
- `suppliers.csv` contains five suppliers and five unique External IDs.
- All five supplier External IDs resolve to `res.partner` records in the `__import__` namespace.

The corrected CSV and guide retain the existing External IDs, target `product.template` for products, and omit the two unsupported canteen fields.

## 3. Import test results

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| Local products.csv validation | 20 rows, unique SKUs and External IDs | 20 rows; 20 unique SKUs; 20 unique External IDs | PASS |
| Odoo Test products.csv | All 20 External IDs resolve without validation errors | Odoo displayed "Everything seems valid."; 8/8 columns mapped | PASS |
| First import products.csv | Import 20 product templates | Odoo reported 20 records successfully imported; database contains 20 UTH products and 20 unique SKUs | PASS |
| Product External ID integrity | 20 IDs link to 20 distinct product templates | 20 linked External IDs, 20 linked products, 20 unique SKUs | PASS |
| Local suppliers.csv validation | Five rows and five unique External IDs | Five suppliers and five unique External IDs | PASS |
| Odoo Test suppliers.csv | All five External IDs resolve without validation errors | Odoo displayed "Everything seems valid."; 9/9 columns mapped | PASS |
| First import suppliers.csv | Import five supplier contacts | Odoo reported five records successfully imported; database contains five linked suppliers | PASS |
| Supplier field verification | Supplier rank, customer rank and contact fields match CSV | All five rows show supplier_rank=1, customer_rank=0; email, phone, street, city and VAT match the CSV | PASS |
| Second import products.csv | No additional product templates or duplicate SKUs | Odoo reported 20 records successfully imported; database still contains 20 products, 20 unique SKUs and 20 External IDs linked to 20 distinct templates | PASS |
| Second import suppliers.csv | No duplicate supplier contacts | Odoo reported five records successfully imported; database still contains five suppliers and five distinct partners | PASS |
| Supplier re-import integrity | External IDs and supplier data remain correct | All five External IDs resolve; supplier_rank=1 and VAT values remain correct | PASS |

## 4. Evidence captured

The following Odoo screenshots have been captured in `functional/purchase_inventory/evidence/ERP-16/`:

- `TC-01-product-import-preview.png` – Product import preview and field mapping.
- `TC-02-product-import-success.png` – Product Odoo Test success message.
- `TC-03-supplier-import-preview.png` – Supplier import preview and field mapping.
- `TC-04-supplier-import-success.png` – Supplier Odoo Test success message.

The import completion messages and SQL verification results were checked during the test process. Separate screenshots or saved output files for import completion and SQL verification have not yet been added to the evidence folder.

## 5. Limitations

- Supplier details are fictional test data.
- Product list prices are POS selling prices, not supplier purchase prices.
- Product costs and recipe costing are outside this task's import scope.
- Import and re-import tests were performed against the test database `uth_canteen_erp13_test`.
- TV1 review and acceptance are still pending.

## 6. Conclusion

The corrected product and supplier CSV files passed Odoo Test Import and were imported successfully.

Both CSV files were imported a second time. Database verification confirmed that:

- Products remain at 20 records with 20 unique SKUs and 20 External IDs linked to 20 distinct product templates.
- Suppliers remain at five records with five distinct partners and five valid External IDs.
- Supplier rank and VAT values remain correct after re-import.

Four Odoo preview/Test screenshots have been captured. Import completion and SQL verification results have also been checked, but separate screenshot evidence for those results has not yet been added.

ERP-16 is **Import tests PASS; evidence partially captured; pending TV1 re-review**. Do not mark the task Done or the PR accepted until the remaining evidence and review requirements are satisfied.
# ERP-16 – CSV Import Test Report

## 1. Test information

- Jira Task: ERP-16
- Responsible: TV2 – Purchase & Inventory
- Database: uth_canteen_erp13_test
- Execution Date: 2026-11-23
- Status: Executed – Pending Review

## 2. Product import

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| Import products.csv | 20 products imported | 20 products imported | PASS |
| Unique SKU validation | 20 unique SKUs | 20 unique SKUs | PASS |
| POS availability | 20 products enabled | 20 products enabled | PASS |
| Re-import products.csv | No duplicate products | Product count remained 20 | PASS |

## 3. Supplier import

| Test | Expected result | Actual result | Status |
|---|---|---|---|
| Import suppliers.csv | 5 suppliers imported | 5 suppliers imported | PASS |

## 4. Evidence

- Product import completed successfully in Odoo.
- Supplier import completed successfully in Odoo.
- Product SQL validation confirmed 20 products, 20 unique SKUs and 20 POS-enabled products.
- Repeated product import did not increase the product count.

## 5. Limitations

- Supplier re-import idempotency has not been separately verified.
- Product costs and recipe costing are outside this task's import scope.
- Supplier records are fictional demonstration data.

## 6. Conclusion

The product and supplier CSV imports were successful in the test database.
Product count, SKU uniqueness and POS availability met the expected results.
Pending peer review and PR acceptance.

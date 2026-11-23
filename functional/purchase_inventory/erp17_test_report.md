# ERP-17 – Purchase & Inventory Configuration Test Report

**Owner:** TV2 – Purchase & Inventory
**Environment:** Odoo Community 20.0
**Database:** uth_canteen_erp13_test
**Status:** DEMO – Test Passed
**Currency:** VND

## 1. Configuration Verification

| Item | Result |
|---|---|
| Product, Purchase, Inventory modules | Installed |
| Units of Measure & Packagings | Enabled |
| Stock UoM | kg |
| Warehouse | WH – My Company |
| Receipt steps | One-step receipt |
| Raw materials | Storable products |
| Vendor pricelist | 10 supplier-product links |
| Supplier prices | Pending approved demo quotations |

## 2. Purchase-to-Inventory Test

| Field | Result |
|---|---|
| Vendor | Công ty Thực phẩm An Sáng UTH |
| Product | Gạo thơm ST25 Thượng hạng |
| Purchase Order | P00003 |
| Receipt | WH/IN/00004 |
| Ordered quantity | 1 kg |
| Received quantity | 1 kg |
| Receipt status | Done |
| Effective date | 2026-11-23 |
| Stock before receipt | 197 kg |
| Stock after receipt | 198 kg |

## 3. Test Result

**TC-01: PASS**

- RFQ created successfully.
- RFQ confirmed as Purchase Order.
- Receipt created from PO.
- Received quantity validated successfully.
- On-hand quantity increased from 197 kg to 198 kg.

## 4. Evidence

- `evidence/ERP-17/TC-01-stock-after-receipt.png`

## 5. Limitations

- Supplier purchase prices remain zero because approved demo quotations have not been provided.
- Packaging sizes require business validation before production use.
- Test data is fictional and must not be treated as actual commercial data.

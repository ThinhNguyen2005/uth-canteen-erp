# ERP-18 – Sample Purchase Orders Test Report

**Project:** UTH Canteen ERP  
**Jira:** ERP-18  
**Epic:** KAN-119  
**Owner:** TV2 – Purchase & Inventory  
**Target Version:** Odoo Community 20.0  
**Environment:** uth_canteen_erp13_test  
**Currency:** VND  
**Status:** DEMO – Completed, Pending Review  

## 1. Objective

Create and verify at least five sample Purchase Orders using multiple suppliers and products in Odoo.

All supplier, quantity, and unit-price data in this report are fictional DEMO data for ERP validation. They are not actual supplier quotations or commercial transactions.

## 2. Purchase Order Summary

| PO Reference | Supplier | Receipt Reference | Total (VND) | PO Status | Receipt Status |
|---|---|---|---:|---|---|
| P00004 | Công ty Thực phẩm An Sáng UTH | WH/IN/00005 | 2,010,000 | Purchase Order | Ready |
| P00005 | Công ty Thực phẩm An Sáng UTH | WH/IN/00006 | 2,360,000 | Purchase Order | Ready |
| P00006 | Hợp tác xã Nông sản Đà Lạt Xanh | WH/IN/00007 | 1,040,000 | Purchase Order | Ready |
| P00007 | Công ty Thực phẩm Tân Thuận | WH/IN/00008 | 3,780,000 | Purchase Order | Ready |
| P00008 | Công ty Gia vị Hương Việt | WH/IN/00009 | 2,860,000 | Purchase Order | Ready |
| **Total** | **4 suppliers** | **5 receipts** | **12,050,000** | **5/5 confirmed** | **5/5 Ready** |

## 3. Order Line Details

### P00004 – Công ty Thực phẩm An Sáng UTH

| Product | Quantity | UoM | Unit Price (VND) | Subtotal (VND) |
|---|---:|---|---:|---:|
| Gạo ST25 | 50 | kg | 27,000 | 1,350,000 |
| Bánh phở tươi | 30 | kg | 22,000 | 660,000 |
| **Total** | **80** | **kg** | | **2,010,000** |

Receipt: WH/IN/00005

### P00005 – Công ty Thực phẩm An Sáng UTH

| Product | Quantity | UoM | Unit Price (VND) | Subtotal (VND) |
|---|---:|---|---:|---:|
| Sữa đặc | 2 | Units | 1,180,000 | 2,360,000 |
| **Total** | **2** | **Units** | | **2,360,000** |

Receipt: WH/IN/00006

### P00006 – Hợp tác xã Nông sản Đà Lạt Xanh

| Product | Quantity | UoM | Unit Price (VND) | Subtotal (VND) |
|---|---:|---|---:|---:|
| Rau củ hỗn hợp nhặt sẵn Đà Lạt (Cà rốt bắp cải dưa leo) | 40 | kg | 26,000 | 1,040,000 |
| **Total** | **40** | **kg** | | **1,040,000** |

Receipt: WH/IN/00007

### P00007 – Công ty Thực phẩm Tân Thuận

| Product | Quantity | UoM | Unit Price (VND) | Subtotal (VND) |
|---|---:|---|---:|---:|
| Đùi gà tươi góc tư CP | 20 | Units | 52,000 | 1,040,000 |
| Sườn non heo Vissan | 15 | Units | 128,000 | 1,920,000 |
| Trứng gà Ba Huân (vỉ) | 10 | Units | 82,000 | 820,000 |
| **Total** | **45** | **Units** | | **3,780,000** |

Receipt: WH/IN/00008

### P00008 – Công ty Gia vị Hương Việt

| Product | Quantity | UoM | Unit Price (VND) | Subtotal (VND) |
|---|---:|---|---:|---:|
| Dầu ăn Tường An | 3 | Units | 790,000 | 2,370,000 |
| Trà lài | 5 | Units | 98,000 | 490,000 |
| **Total** | **8** | **Units** | | **2,860,000** |

Receipt: WH/IN/00009

## 4. Quantity and Amount Reconciliation

| Purchase Order | Quantity by UoM | Total (VND) |
|---|---|---:|
| P00004 | 80 kg | 2,010,000 |
| P00005 | 2 Units | 2,360,000 |
| P00006 | 40 kg | 1,040,000 |
| P00007 | 45 Units | 3,780,000 |
| P00008 | 8 Units | 2,860,000 |
| **Total** | **120 kg + 55 Units** | **12,050,000** |

Quantities are reconciled separately by unit of measure. Kilograms and Units are not added together.

## 5. Test Results

| Test ID | Test Description | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| ERP18-T01 | Create five sample RFQs | Five RFQs created | P00004–P00008 created | PASS |
| ERP18-T02 | Use multiple suppliers | Multiple suppliers represented | Four suppliers used | PASS |
| ERP18-T03 | Enter product quantities and unit prices | Order subtotals match planned values | All five totals match | PASS |
| ERP18-T04 | Confirm Purchase Orders | All five orders reach Purchase Order state | All five confirmed | PASS |
| ERP18-T05 | Generate incoming receipts | One receipt generated per PO | Five receipts generated | PASS |
| ERP18-T06 | Reconcile receipt quantities | Receipt quantities match ordered quantities | Checked for all five receipts | PASS |
| ERP18-T07 | Keep receipts unvalidated | Receipts remain pending validation | All five receipts show Ready | PASS |
| ERP18-T08 | Reconcile order totals | Aggregate equals 12,050,000 VND | Aggregate equals 12,050,000 VND | PASS |

## 6. Evidence

Evidence screenshots are stored under:

`functional/purchase_inventory/evidence/ERP-18/`

- `erp18_purchase_orders.png` – Purchase Orders list showing P00004–P00008 and their totals/statuses.
- `erp18_receipts.png` – Receipts list showing WH/IN/00005–WH/IN/00009 and Ready statuses.

## 7. Notes and Limitations

- All suppliers, quantities, and prices are fictional DEMO data.
- No active purchase taxes were applied to these orders.
- Product UoMs follow the existing Odoo product configuration. Some products use Units rather than kg.
- All five incoming receipts remain in Ready status and have not been validated.
- This test verifies purchase order creation, confirmation, receipt generation, and quantity/amount reconciliation. It does not verify physical stock receipt or inventory valuation.

## 8. Conclusion

ERP-18 sample purchase order testing is completed for five Purchase Orders across four suppliers.

All five Purchase Orders were confirmed, five incoming receipts were generated, and the aggregate order amount reconciles to 12,050,000 VND.

**Result: PASS – Pending peer review and acceptance.**

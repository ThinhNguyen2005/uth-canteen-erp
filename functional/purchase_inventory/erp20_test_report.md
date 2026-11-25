# [ERP-20][TV2] Báo cáo kiểm thử điều chỉnh tồn, nhập thiếu và hàng sắp hết

## 1. Thông tin chung

| Trường | Giá trị |
|---|---|
| Project | UTH Canteen ERP |
| Jira | ERP-20 |
| Epic | KAN-119 |
| Responsible | TV2 – Purchase & Inventory |
| Target Version | Odoo Community 20.0 |
| Database | uth_canteen_erp13_test |
| Test Date | 2026-11-25 |
| Branch | feature/ERP-20-stock-adjustment-low-stock |
| Status | Testing Completed – Pending Peer Review |

## 2. Mục tiêu kiểm thử

- Kiểm tra điều chỉnh tồn kho khi số lượng thực tế khác số lượng hệ thống.
- Kiểm tra cấu hình quy tắc bổ sung hàng khi tồn kho xuống dưới mức tối thiểu.
- Kiểm tra trạng thái sản phẩm hết hàng sau khi xuất toàn bộ số lượng tồn.
- Lưu bằng chứng giao diện Odoo và kết quả xác minh SQL.

## 3. Tổng hợp kết quả

| Test Case | Nội dung | Kết quả |
|---|---|---|
| T01 | Điều chỉnh chênh lệch tồn kho | PASS |
| T02 | Kiểm tra quy tắc hàng sắp hết | PASS |
| T03 | Kiểm tra sản phẩm hết hàng | PASS |

## 4. Chi tiết kiểm thử

### T01 – Inventory Discrepancy / Stock Adjustment

**Mục tiêu:** Kiểm tra điều chỉnh số lượng tồn kho theo kết quả kiểm kê thực tế.

Thông tin kiểm thử:

| Trường | Giá trị |
|---|---|
| Product ID | 23 |
| Product | Gạo thơm ST25 Thượng hạng (Bao 25kg) |
| Location | WH/Tồn kho |
| Location ID | 6 |
| System Quantity Before | 248 kg |
| Counted Quantity | 245 kg |
| Difference | -3 kg |
| System Quantity After | 245 kg |
| Reserved Quantity After | 0 kg |

Thực hiện:
1. Kiểm tra tồn kho ban đầu trên Odoo.
2. Nhập số lượng kiểm kê thực tế là 245 kg.
3. Xác nhận chênh lệch -3 kg.
4. Apply điều chỉnh trên dòng sản phẩm.
5. Truy vấn stock_quant để xác minh kết quả.

**Expected Result:** Tồn kho hệ thống được cập nhật bằng số lượng kiểm kê thực tế.

**Actual Result:** SQL xác nhận tồn kho tại WH/Tồn kho là 245 kg, reserved quantity bằng 0.

**Verdict: PASS**

Evidence:
- `evidence/ERP-20/erp20_t01_before.png`
- `evidence/ERP-20/erp20_t01_after.png`
- `evidence/ERP-20/erp20_t01_sql_verification.png`

### T02 – Low Stock / Reordering Rule

**Mục tiêu:** Kiểm tra quy tắc bổ sung hàng khi tồn kho xuống dưới mức tối thiểu.

Thông tin kiểm thử:

| Trường | Giá trị |
|---|---|
| Product ID | 30 |
| Product | Sữa đặc có đường Ông Thọ xanh lá (Thùng 48 lon) |
| Location | WH/Tồn kho |
| Location ID | 6 |
| Unit of Measure | Units |
| On Hand Quantity | 1 Unit |
| Reserved Quantity | 0 Unit |
| Trigger | Auto |
| Minimum Quantity | 5 Units |
| Maximum Quantity | 10 Units |
| Rule ID | 2 |
| Active | True |

Thực hiện:
1. Kiểm tra tồn kho thực tế của sản phẩm.
2. Tạo/cấu hình Reordering Rule cho đúng sản phẩm và vị trí kho.
3. Xác minh trigger là Auto.
4. Kiểm tra mức tồn tối thiểu 5 và tối đa 10.
5. Truy vấn stock_warehouse_orderpoint và stock_quant để xác minh.

**Expected Result:** Quy tắc được gắn đúng sản phẩm, đúng vị trí kho và tồn kho hiện tại thấp hơn mức tối thiểu.

**Actual Result:** SQL xác nhận tồn kho là 1 Unit, thấp hơn minimum 5 Units; quy tắc ID 2 đang active với trigger Auto và maximum 10 Units.

**Verdict: PASS**

Evidence:
- `evidence/ERP-20/erp20_t02_reordering_rule.png`
- `evidence/ERP-20/erp20_t02_sql_verification.png`

### T03 – Stockout / Zero Stock

**Mục tiêu:** Kiểm tra tồn kho sản phẩm sau khi xuất toàn bộ số lượng hiện có.

Thông tin sản phẩm:

| Trường | Giá trị |
|---|---|
| Product ID | 29 |
| Product | Trà lài Tân Cương ướp hoa tươi |
| Unit of Measure | kg |
| Location | WH/Tồn kho |
| Location ID | 6 |

**Giai đoạn 1 – Nhập thử hàng**

| Trường | Giá trị |
|---|---|
| Receipt | WH/IN/00011 |
| Operation Type | incoming |
| Source | Vendors |
| Destination | WH/Tồn kho |
| Quantity | 5 kg |
| State | Done |

SQL xác nhận phiếu nhập đã hoàn thành và stock_quant tại WH/Tồn kho tăng lên 5 kg.

**Giai đoạn 2 – Xuất toàn bộ hàng**

| Trường | Giá trị |
|---|---|
| Delivery | WH/OUT/00001 |
| Operation Type | outgoing |
| Source | WH/Tồn kho |
| Destination | Customers |
| Quantity | 5 kg |
| State | Done |

**Kết quả tồn kho:**

| Chỉ tiêu | Trước xuất | Sau xuất |
|---|---:|---:|
| On Hand | 5 kg | 0 kg |
| Reserved | 0 kg | 0 kg |
| Available | 5 kg | 0 kg |

**Expected Result:** Sau khi xuất đủ 5 kg, tồn kho nội bộ của sản phẩm tại WH/Tồn kho trở về 0 kg.

**Actual Result:** Phiếu WH/OUT/00001 ở trạng thái Done. SQL xác nhận quantity = 0, reserved_quantity = 0 và available_qty = 0.

**Verdict: PASS**

Evidence:
- `evidence/ERP-20/erp20_t03_before_stockout.png`
- `evidence/ERP-20/erp20_t03_receipt_done.png`
- `evidence/ERP-20/erp20_t03_after_stockout.png`
- `evidence/ERP-20/erp20_t03_delivery_done.png`

## 5. Tổng kết

| Chỉ tiêu | Kết quả |
|---|---:|
| Tổng số test case | 3 |
| PASS | 3 |
| FAIL | 0 |
| Tổng số ảnh bằng chứng | 9 |

Kết luận:
- T01: Điều chỉnh tồn kho thành công, số lượng hệ thống khớp số lượng kiểm kê.
- T02: Quy tắc bổ sung hàng được cấu hình đúng; tồn kho thấp hơn mức tối thiểu.
- T03: Xuất toàn bộ hàng thành công; tồn kho nội bộ trở về 0 kg.

Các kịch bản ERP-20 đã được thực hiện trên database thử nghiệm `uth_canteen_erp13_test`.

ERP-19 backorder được giữ nguyên, không xác nhận hoặc thay đổi trong quá trình kiểm thử ERP-20.

**Overall Result: PASS – 3/3 test cases.**

**Current Status: Pending Peer Review and Acceptance.**

## 6. Acceptance Checklist

- [x] T01 – Kiểm thử điều chỉnh chênh lệch tồn kho.
- [x] T02 – Kiểm thử cấu hình quy tắc hàng sắp hết.
- [x] T03 – Kiểm thử xuất hết hàng và xác minh tồn kho bằng 0.
- [x] Lưu ảnh bằng chứng cho từng test case.
- [x] Xác minh kết quả bằng SQL.
- [ ] Peer Review.
- [ ] PR được chấp nhận.
- [ ] Cập nhật Jira ERP-20 sau khi hoàn tất review.


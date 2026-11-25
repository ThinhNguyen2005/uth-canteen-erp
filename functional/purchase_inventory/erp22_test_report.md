# [ERP-22][TV2] Báo cáo kiểm thử hồi quy và sửa lỗi nghiệp vụ kho

**Phụ trách:** TV2 – Purchase & Inventory
**Database kiểm thử:** `uth_canteen_erp22_sandbox`
**Branch:** `feature/ERP-22-inventory-regression`
**Ngày thực hiện:** 2026-11-25
**Trạng thái:** Testing Completed – Pending Peer Review

## 1. Mục tiêu

Kiểm tra hồi quy các nghiệp vụ Purchase & Inventory, gồm:
- Nhận hàng đầy đủ và nhận hàng một phần.
- Kiểm tra hành vi xuất kho khi tồn kho không đủ.
- Xác minh điều chỉnh tồn và quy tắc bổ sung hàng.
- Kiểm thử nhập lại CSV sản phẩm và nhà cung cấp.

Các kiểm thử có rủi ro được thực hiện trên database sandbox được sao chép từ `uth_canteen_erp13_test`. Không thực hiện các thao tác kiểm thử phá hủy trên database chính.

## 2. Kết quả kiểm thử

| Test | Nội dung | Kết quả | Ghi chú |
|---|---|---|---|
| T01 | Kiểm tra tồn ST25 sau điều chỉnh | VERIFIED – INHERITED | Dữ liệu 245 kg được kế thừa từ ERP-20; chưa thực hiện điều chỉnh mới trong ERP-22 |
| T02 | Kiểm tra quy tắc bổ sung hàng sữa đặc | VERIFIED – INHERITED | Rule ID 2, min 5, max 10, active; kế thừa từ ERP-20 |
| T03 | Xuất kho khi không đủ tồn | PASS – OBSERVED | Odoo cho phép xác nhận giao hàng và tồn kho nội bộ giảm xuống -1 kg |
| T04 | Import CSV sản phẩm và nhà cung cấp | PASS | Import thực tế trên sandbox và xác minh bằng PostgreSQL |
| TC-FULL | Nhận hàng đầy đủ | VERIFIED – INHERITED | WH/IN/00005 đã Done; dữ liệu kế thừa từ ERP-19 |
| TC-PARTIAL | Nhận hàng một phần | VERIFIED – INHERITED | WH/IN/00006 đã Done; WH/IN/00010 vẫn Assigned; dữ liệu kế thừa từ ERP-19 |

### 2.1. T01 – Kiểm tra tồn kho ST25

- Product ID: 23 – Gạo thơm ST25 Thượng hạng.
- Location: `WH/Tồn kho` (ID 6).
- Số lượng hiện tại trong sandbox: 245 kg.
- Reserved: 0 kg.

**Kết luận:** Dữ liệu tồn kho được xác minh. Giá trị này là dữ liệu được sao chép từ ERP-20, không phải kết quả của một lần điều chỉnh tồn mới trong ERP-22.

### 2.2. T02 – Quy tắc bổ sung hàng

- Product ID: 30 – Sữa đặc có đường Ông Thọ xanh lá.
- Location: `WH/Tồn kho`.
- Reordering Rule ID: 2.
- Trigger: Auto.
- Minimum: 5.
- Maximum: 10.
- Active: True.

**Kết luận:** Quy tắc hiện có được xác minh trong sandbox. Đây là cấu hình kế thừa từ ERP-20, chưa tạo mới trong ERP-22.

### 2.3. T03 – Kiểm thử xuất kho âm

- Database: `uth_canteen_erp22_sandbox`.
- Picking: `WH/OUT/00002`.
- Product ID: 29 – Trà lài Tân Cương ướp hoa tươi.
- Source: `WH/Tồn kho` (Location ID 6).
- Destination: `Customers` (Location ID 2).
- Demand: 1 kg.
- Tồn trước khi xác nhận: 0 kg.
- Sau khi xác nhận: Picking `Done`.
- Tồn sau giao dịch: -1 kg.
- Reserved sau giao dịch: 0 kg.

**Kết luận:** Odoo cho phép xác nhận giao hàng dù tồn kho nội bộ không đủ, dẫn đến tồn âm -1 kg.

Đây là kết quả quan sát thực tế trên sandbox. ERP-21 hiện chưa xác định rõ chính sách bắt buộc chặn tồn âm, do đó cần TV1/nhóm dự án xác nhận yêu cầu nghiệp vụ trước khi kết luận đây là lỗi cần sửa.

**Bằng chứng:**
- `evidence/ERP-22/erp22_t03_delivery_done.png`
- `evidence/ERP-22/erp22_t03_negative_stock.png`
- `evidence/ERP-22/erp22_t03_negative_stock_result.txt`

### 2.4. T04 – Import CSV

Thực hiện trên database `uth_canteen_erp22_sandbox`.

**Products – `products.csv`:**
- Odoo thông báo `20 records successfully imported`.
- 20 sản phẩm POS.
- 20 SKU duy nhất.
- 20 External ID duy nhất.
- Tên sản phẩm tiếng Việt được lưu trong trường tên đã kiểm tra.

**Suppliers – `suppliers.csv`:**
- Odoo thông báo `5 records successfully imported`.
- 5 nhà cung cấp.
- 5 VAT duy nhất.
- 5 External ID duy nhất.
- Cả 5 nhà cung cấp có `supplier_rank = 1`.
- Cả 5 nhà cung cấp có `customer_rank = 0`.

**Kết quả SQL xác minh:**

| Chỉ tiêu | Kết quả |
|---|---:|
| POS products | 20 |
| Unique SKUs | 20 |
| Supplier records | 5 |
| Unique VAT | 5 |
| Supplier rank hợp lệ | 5 |
| Supplier External IDs | 5 |
| Unique supplier External IDs | 5 |

**Bằng chứng:**
- `evidence/ERP-22/erp22_t04_csv_import_verified.png`

### 2.5. Kiểm tra nhận hàng đầy đủ và một phần

Các chứng từ dưới đây được kiểm tra trong dữ liệu sandbox sao chép từ database trước đó. Đây không phải giao dịch mới được tạo trong ERP-22.

**Nhận hàng đầy đủ – WH/IN/00005:**
- Trạng thái: Done.
- Gạo ST25: 50 kg.
- Bánh phở: 30 kg.
- Purchase Order: P00004.

**Nhận hàng một phần – WH/IN/00006:**
- Purchase Order: P00005.
- Sữa đặc đặt: 2 Units.
- Đã nhận: 1 Unit.
- WH/IN/00006: Done.
- Backorder WH/IN/00010: Assigned, chưa xác nhận.

**Lưu ý:** Không xác nhận, hủy hoặc chỉnh sửa WH/IN/00010 trong quá trình kiểm thử ERP-22.

## 3. Tổng kết

- Import CSV sản phẩm: PASS.
- Import CSV nhà cung cấp: PASS.
- Xuất kho âm: Odoo cho phép thực hiện; cần xác nhận chính sách nghiệp vụ.
- Tồn kho ST25 và quy tắc bổ sung hàng: đã xác minh dữ liệu kế thừa.
- Nhận hàng đầy đủ và một phần: đã xác minh chứng từ kế thừa từ ERP-19.
- Chưa thực hiện lại giao dịch điều chỉnh tồn và tạo mới quy tắc bổ sung hàng trong ERP-22.

## 4. Vấn đề cần phối hợp

Đề nghị TV1/nhóm dự án xác nhận:
1. Hệ thống có bắt buộc chặn xác nhận giao hàng khi tồn kho nội bộ không đủ hay không?
2. Nếu có, cần thống nhất cấu hình hoặc giải pháp kỹ thuật để ngăn tồn kho âm.

## 5. Trạng thái bàn giao

**Testing Completed – Pending Peer Review**

Báo cáo ghi nhận riêng kết quả kiểm thử thực tế trong ERP-22 và dữ liệu lịch sử được kế thừa từ ERP-19/ERP-20. Chưa kết luận toàn bộ kiểm thử hồi quy đã PASS cho đến khi các ca còn thiếu được chạy lại và vấn đề chính sách tồn âm được xác nhận.

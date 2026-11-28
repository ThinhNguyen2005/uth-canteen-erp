# [ERP-21][TV2] Test Cases – Purchase & Inventory Setup

**Owner:** TV2 – Purchase & Inventory
**Target:** Odoo Community 20.0
**Scope:** Database mới, cài module, import CSV, warehouse, phân quyền, mua hàng, nhận hàng và kiểm tra tồn kho.
**Execution status:** Not Executed on a fresh database – Pending peer validation.

---

## 1. Mục tiêu

Xác nhận một thành viên khác có thể sử dụng `setup.md` để:

- Chuẩn bị database Odoo mới.
- Cài đặt các module cần thiết.
- Import dữ liệu sản phẩm POS và nhà cung cấp.
- Chuẩn bị sản phẩm nguyên liệu có thể mua và quản lý tồn kho.
- Cấu hình warehouse nhận hàng một bước.
- Cấp quyền người dùng.
- Tạo RFQ, xác nhận PO và nhận hàng.
- Kiểm tra tồn kho sau khi nhận đủ hoặc nhận thiếu.

## 2. Điều kiện chung

- Database kiểm thử mới, không phải database đã có dữ liệu nghiệp vụ.
- Odoo Community 20.0.
- Có tài khoản Administrator.
- Các module chuẩn cần thiết có sẵn.
- Có file CSV trong `functional/purchase_inventory/`.
- Có ít nhất một nhà cung cấp và một sản phẩm nguyên liệu phù hợp để mua.
- Sản phẩm có đơn vị tính hợp lệ và có thể phát sinh stock receipt.
- Giá mua là giá DEMO được người thực hiện xác nhận cho lần kiểm thử; không mặc định dùng Sales Price hoặc giá 0.

## 3. Test cases

### TC-01 – Create a new database

**Mục tiêu:** Xác nhận có thể tạo và truy cập database mới.

**Các bước:**
1. Mở trang quản lý database.
2. Tạo database mới với tên kiểm thử riêng.
3. Thiết lập tài khoản Administrator.
4. Đăng nhập vào database.
5. Kiểm tra database hoạt động bình thường.

**Kết quả mong đợi:**
- Database được tạo thành công.
- Administrator đăng nhập được.
- Database mới không phụ thuộc dữ liệu của `uth_canteen_erp13_test`.

**Bằng chứng:** Tên database và ảnh màn hình đăng nhập.

**Kết quả thực tế:** Pending.

---

### TC-02 – Install Purchase and Inventory modules

**Mục tiêu:** Xác nhận các module cần thiết được cài đặt.

**Các bước:**
1. Mở Apps.
2. Cài Contacts, Purchase, Inventory và các dependency cần thiết.
3. Kiểm tra `purchase_stock` đã được cài.
4. Cài `canteen_management` nếu phạm vi triển khai yêu cầu.
5. Mở Purchase, Inventory, Contacts và Products.

**Kết quả mong đợi:**
- Các module cần thiết có trạng thái Installed.
- Không có lỗi cài đặt dependency.
- Các menu nghiệp vụ truy cập được.

**Bằng chứng:** Ảnh danh sách module và menu ứng dụng.

**Kết quả thực tế:** Pending.

---

### TC-03 – Import POS products

**Mục tiêu:** Kiểm tra import 20 sản phẩm từ `products.csv`.

**Tiền điều kiện:** Database mới hoặc đã xác định rõ External ID hiện có.

**Các bước:**
1. Mở Products.
2. Chọn Import Records.
3. Tải `functional/purchase_inventory/products.csv`.
4. Chọn model Product (`product.template`).
5. Map các trường theo `import_guide.md`.
6. Chọn Test.
7. Kiểm tra lỗi và External ID.
8. Import khi preview hợp lệ.
9. Kiểm tra số lượng bản ghi và SKU.

**Kết quả mong đợi:**
- 20 sản phẩm được import.
- 20 SKU duy nhất.
- 20 External ID được liên kết đúng model.
- `available_in_pos` được map đúng.
- Không tạo bản ghi trùng khi re-import.

**Lưu ý:** Đây là danh mục sản phẩm POS, không thay thế danh mục nguyên liệu quản lý tồn kho.

**Bằng chứng:** Preview, kết quả import và danh sách sản phẩm.

**Kết quả tham chiếu ERP-16:** PASS trên database tham chiếu.

**Kết quả fresh database:** Pending.

---

### TC-04 – Import suppliers

**Mục tiêu:** Kiểm tra import 5 nhà cung cấp từ `suppliers.csv`.

**Các bước:**
1. Mở Contacts.
2. Chọn Import Records.
3. Tải `functional/purchase_inventory/suppliers.csv`.
4. Map các trường External ID, Name, Supplier Rank, Customer Rank, Email, Phone, Street, City và VAT.
5. Chọn Test.
6. Kiểm tra preview.
7. Import.
8. Mở các contact và kiểm tra thông tin.
9. Import lại để kiểm tra duplicate.

**Kết quả mong đợi:**
- 5 nhà cung cấp được tạo hoặc cập nhật.
- Supplier Rank = 1.
- Customer Rank = 0.
- Thông tin liên hệ khớp CSV.
- Re-import không tạo contact trùng.

**Bằng chứng:** Preview, kết quả import và danh sách Contacts.

**Kết quả tham chiếu ERP-16:** PASS trên database tham chiếu.

**Kết quả fresh database:** Pending.

---

### TC-05 – Prepare a storable purchase product

**Mục tiêu:** Xác nhận sản phẩm nguyên liệu có thể được mua và nhận vào kho.

**Các bước:**
1. Mở Products.
2. Tạo hoặc chọn một nguyên liệu DEMO.
3. Thiết lập Internal Reference duy nhất.
4. Chọn loại sản phẩm hỗ trợ theo dõi tồn kho trên Odoo 20.
5. Bật Can be Purchased.
6. Chọn UoM phù hợp, ví dụ kg hoặc Units.
7. Lưu sản phẩm.
8. Kiểm tra sản phẩm có thể được chọn trong RFQ.
9. Xác nhận sản phẩm có thể phát sinh receipt.

**Kết quả mong đợi:**
- Sản phẩm được lưu.
- Có thể chọn trên RFQ.
- UoM đúng.
- Sản phẩm có thể được nhận vào vị trí kho nội bộ.

**Bằng chứng:** Form sản phẩm và dòng sản phẩm trên RFQ.

**Kết quả thực tế:** Pending trên database mới.

---

### TC-06 – Configure warehouse and one-step receipt

**Mục tiêu:** Xác nhận warehouse có thể nhận hàng theo một bước.

**Các bước:**
1. Mở Inventory → Configuration → Warehouses.
2. Kiểm tra hoặc tạo warehouse.
3. Đặt mã kho theo cấu hình dự án, tham chiếu `WH`.
4. Chọn One-step receipt.
5. Lưu cấu hình.
6. Kiểm tra các vị trí kho.
7. Xác nhận có vị trí tồn kho nội bộ và operation type nhận hàng.

**Kết quả mong đợi:**
- Warehouse hoạt động.
- Cấu hình nhận hàng một bước.
- Có vị trí kho nội bộ.
- Có thể phát sinh incoming receipt từ PO.

**Cấu hình tham chiếu ERP-17:**

| Thuộc tính | Giá trị |
|---|---|
| Warehouse | WH – My Company |
| Receipt Steps | One-step |
| Input Location | WH/Đầu vào |
| Stock Location | WH/Tồn kho |

**Bằng chứng:** Ảnh warehouse và locations.

**Kết quả tham chiếu ERP-17:** PASS.

**Kết quả fresh database:** Pending.

---

### TC-07 – Verify user permissions

**Mục tiêu:** Xác nhận nhân viên mua hàng và nhân viên kho có quyền phù hợp.

**Các bước:**
1. Tạo hoặc chọn tài khoản Purchasing Staff.
2. Cấp Purchase User.
3. Tạo hoặc chọn tài khoản Warehouse Staff.
4. Cấp Inventory User.
5. Đăng nhập từng tài khoản.
6. Kiểm tra menu và thao tác được phép.
7. Thử truy cập chức năng quản trị không thuộc vai trò để xác nhận giới hạn quyền.

**Kết quả mong đợi:**
- Purchasing Staff truy cập được nghiệp vụ mua hàng theo quyền.
- Warehouse Staff truy cập được nghiệp vụ kho theo quyền.
- Tài khoản thông thường không có quyền Administrator.
- Không cấp quyền vượt quá yêu cầu công việc.

**Bằng chứng:** Ảnh cấu hình quyền và kiểm tra bằng tài khoản tương ứng.

**Kết quả thực tế:** Pending.

---

### TC-08 – Create and confirm a Purchase Order

**Mục tiêu:** Kiểm tra quy trình RFQ đến PO.

**Tiền điều kiện:**
- Có supplier.
- Có sản phẩm nguyên liệu có thể mua.
- Có UoM hợp lệ.
- Người dùng có quyền Purchase phù hợp.
- Có giá mua DEMO đã xác nhận.

**Các bước:**
1. Mở Purchase → Requests for Quotation.
2. Chọn New.
3. Chọn supplier.
4. Thêm sản phẩm nguyên liệu.
5. Nhập số lượng và giá mua.
6. Lưu RFQ.
7. Kiểm tra thông tin.
8. Chọn Confirm Order.
9. Mở PO và kiểm tra Receipt được tạo.

**Kết quả mong đợi:**
- RFQ được lưu.
- RFQ được xác nhận thành PO.
- Có incoming receipt liên kết với PO.
- Sản phẩm, số lượng và nhà cung cấp khớp dữ liệu đã nhập.

**Bằng chứng:** RFQ, PO và receipt reference.

**Kết quả thực tế:** Pending trên database mới.

---

### TC-09 – Receive the full ordered quantity

**Mục tiêu:** Kiểm tra nhận đủ hàng và cập nhật tồn kho.

**Tiền điều kiện:**
- Có PO đã xác nhận.
- Có incoming receipt.
- Hàng đã được kiểm tra vật lý.

**Các bước:**
1. Ghi nhận On Hand trước khi nhận.
2. Mở incoming receipt.
3. Kiểm tra sản phẩm và số lượng đặt.
4. Nhập số lượng thực nhận bằng số lượng đặt.
5. Chọn Validate.
6. Xác nhận receipt chuyển sang Done.
7. Kiểm tra On Hand sau khi nhận.

**Kết quả mong đợi:**
- Receipt ở trạng thái Done.
- Không phát sinh backorder.
- On Hand tăng đúng số lượng thực nhận, giả định không có stock movement đồng thời.

**Bằng chứng:** PO, receipt Done và tồn kho sau nhận.

**Kết quả tham chiếu ERP-17:** P00003 / WH/IN/00004, nhận 1 kg ST25; tồn kho tăng từ 197 kg lên 198 kg.

**Kết quả tham chiếu ERP-19:** P00004 / WH/IN/00005, nhận đủ 50 kg ST25 và 30 kg bánh phở.

**Kết quả fresh database:** Pending.

---

### TC-10 – Receive a partial quantity and create backorder

**Mục tiêu:** Kiểm tra xử lý giao thiếu.

**Tiền điều kiện:**
- Có PO đã xác nhận.
- Nhà cung cấp chỉ giao một phần và dự kiến giao phần còn lại sau.

**Các bước:**
1. Mở incoming receipt.
2. Kiểm tra số lượng đặt.
3. Nhập số lượng thực nhận thấp hơn số lượng đặt.
4. Chọn Validate.
5. Chọn tạo Backorder khi Odoo hỏi cách xử lý phần còn lại.
6. Mở receipt ban đầu và backorder.
7. Kiểm tra số lượng đã nhận, còn thiếu và trạng thái.
8. Kiểm tra On Hand.

**Kết quả mong đợi:**
- Receipt ban đầu ghi nhận đúng số lượng thực nhận.
- Backorder giữ đúng số lượng còn thiếu.
- Số lượng chưa nhận không được cộng vào On Hand.
- PO phản ánh số lượng đã nhận và còn lại.
- Backorder không được Validate trước khi hàng thực sự đến.

**Bằng chứng:** Receipt Done, Backorder và tồn kho.

**Kết quả tham chiếu ERP-19:** P00005 / WH/IN/00006; đặt 2 Units, nhận 1 Unit, tạo WH/IN/00010 còn 1 Unit ở trạng thái Assigned.

**Giới hạn tham chiếu:** Backorder WH/IN/00010 được giữ Assigned, chưa Validate.

**Kết quả fresh database:** Pending.

---

### TC-11 – Inventory quantity reconciliation

**Mục tiêu:** Đối chiếu tồn kho sau khi nhận hàng.

**Các bước:**
1. Ghi lại On Hand trước receipt.
2. Validate receipt.
3. Ghi lại số lượng thực nhận.
4. Mở sản phẩm và vị trí kho.
5. Kiểm tra On Hand sau receipt.
6. Đối chiếu công thức:

`On Hand sau = On Hand trước + Số lượng thực nhận`

**Kết quả mong đợi:**
- Số lượng tồn kho tăng đúng số lượng thực nhận.
- Không tính phần backorder chưa nhận.
- Không có chênh lệch không giải thích được.

**Bằng chứng:** Sản phẩm, vị trí, receipt và số lượng trước/sau.

**Kết quả tham chiếu ERP-19:**
- ST25: 198 kg + 50 kg = 248 kg.
- Bánh phở: 0 kg + 30 kg = 30 kg.
- Sữa đặc: 0 Units + 1 Unit = 1 Unit.

**Kết quả fresh database:** Pending.

---

### TC-12 – Inventory adjustment

**Mục tiêu:** Kiểm tra ghi nhận chênh lệch kiểm kê.

**Tiền điều kiện:**
- Có sản phẩm theo dõi tồn kho.
- Có số lượng kiểm đếm thực tế.
- Người dùng có quyền thực hiện điều chỉnh.

**Các bước:**
1. Ghi lại On Hand hiện tại.
2. Mở chức năng kiểm kê/Physical Inventory.
3. Chọn sản phẩm và vị trí.
4. Nhập số lượng thực đếm.
5. Kiểm tra chênh lệch.
6. Xác nhận điều chỉnh theo quyền được cấp.
7. Kiểm tra On Hand sau điều chỉnh.

**Kết quả mong đợi:**
- Chênh lệch được tính đúng.
- Điều chỉnh được ghi nhận.
- On Hand bằng số lượng đã kiểm đếm, giả định không có stock movement đồng thời.
- Có thể truy vết giao dịch điều chỉnh.

**Kết quả tham chiếu ERP-20:** ST25 tại `WH/Tồn kho`, 248 kg được kiểm đếm thành 245 kg, chênh lệch -3 kg.

**Trạng thái ERP-21:** Cần đối chiếu báo cáo ERP-20 và kiểm thử lại trên database mới; không coi đây là kết quả fresh-database của ERP-21.

---

### TC-13 – Reordering rule configuration

**Mục tiêu:** Kiểm tra cấu hình min/max cho sản phẩm tồn kho.

**Các bước:**
1. Chọn sản phẩm nguyên liệu hoặc hàng hóa có tồn kho.
2. Mở Reordering Rules.
3. Chọn sản phẩm và vị trí kho.
4. Chọn trigger phù hợp.
5. Nhập Minimum và Maximum.
6. Lưu rule.
7. Kiểm tra sản phẩm, vị trí, min/max và trạng thái rule.

**Kết quả mong đợi:**
- Rule được lưu đúng sản phẩm và vị trí.
- Min/Max đúng dữ liệu cấu hình.
- Có thể kiểm tra forecast và lượng cần bổ sung.

**Kết quả tham chiếu ERP-20:** Sữa đặc Ông Thọ, location `WH/Tồn kho`, Minimum 5, Maximum 10, On Hand 1 Unit, Incoming 1 Unit, Forecast 2 Units, lượng cần bổ sung tính toán 8 Units.

**Giới hạn:** Không xác nhận tự động tạo RFQ nếu chưa kiểm thử scheduler và dữ liệu nhà cung cấp/giá mua hợp lệ. Báo cáo ERP-20 ghi nhận giá supplierinfo bằng 0 VND nên không chạy scheduler để tránh tạo RFQ với giá chưa được xác nhận.

**Trạng thái ERP-21:** Tham chiếu; cần xác nhận lại trên database mới.

---

## 4. Execution Summary

| Test ID | Nội dung | Kết quả tham chiếu | Kết quả fresh DB |
|---|---|---|---|
| TC-01 | Create new database | Chưa có | Pending |
| TC-02 | Install modules | ERP environment đã cài | Pending |
| TC-03 | Import POS products | ERP-16 PASS | Pending |
| TC-04 | Import suppliers | ERP-16 PASS | Pending |
| TC-05 | Prepare storable product | ERP-17 có raw materials | Pending |
| TC-06 | Configure warehouse | ERP-17 PASS | Pending |
| TC-07 | Verify permissions | Chưa có bằng chứng độc lập | Pending |
| TC-08 | Create and confirm PO | ERP-17/19 PASS | Pending |
| TC-09 | Full receipt | ERP-17/19 PASS | Pending |
| TC-10 | Partial receipt/backorder | ERP-19 PASS | Pending |
| TC-11 | Stock reconciliation | ERP-17/19 PASS | Pending |
| TC-12 | Inventory adjustment | ERP-20 tham chiếu | Pending |
| TC-13 | Reordering rule | ERP-20 tham chiếu | Pending |

## 5. Evidence Checklist

- [ ] Database mới và thông tin môi trường.
- [ ] Module đã cài.
- [ ] Import products preview và kết quả.
- [ ] Import suppliers preview và kết quả.
- [ ] Sản phẩm nguyên liệu có thể mua và theo dõi tồn kho.
- [ ] Warehouse one-step và locations.
- [ ] Phân quyền Purchasing Staff và Warehouse Staff.
- [ ] RFQ và PO đã xác nhận.
- [ ] Receipt nhận đủ ở trạng thái Done.
- [ ] Receipt nhận thiếu ở trạng thái Done.
- [ ] Backorder với số lượng còn thiếu.
- [ ] Tồn kho trước và sau receipt.
- [ ] Inventory adjustment (nếu thực hiện).
- [ ] Reordering rule (nếu thực hiện).

## 6. Acceptance Criteria

ERP-21 được đề xuất chấp nhận khi:

1. Một thành viên khác tạo được database mới.
2. Cài được module cần thiết theo `setup.md`.
3. Import được CSV sản phẩm POS và nhà cung cấp.
4. Chuẩn bị được sản phẩm nguyên liệu có thể mua và theo dõi tồn kho.
5. Cấu hình được warehouse nhận hàng một bước.
6. Tài khoản được phân quyền có thể thực hiện đúng vai trò.
7. Tạo và xác nhận được RFQ/PO.
8. Nhận đủ hàng và xác minh tồn kho.
9. Nhận thiếu hàng, tạo backorder và xác minh phần còn thiếu chưa được cộng vào tồn kho.
10. Thành viên thực hiện không cần trợ giúp đặc biệt.
11. Có ảnh/chứng từ và kết quả kiểm thử được lưu trong repository.
12. Peer review và xác nhận nghiệp vụ hoàn tất.

**Không đánh dấu PASS cho các test case chỉ vì có kết quả tham chiếu từ database cũ. Kết quả trên database mới phải được ghi nhận riêng.**
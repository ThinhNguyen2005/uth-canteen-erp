# [ERP-21][TV2] Hướng dẫn cấu hình Purchase và Inventory

**Phụ trách:** TV2 – Purchase & Inventory
**Phiên bản mục tiêu:** Odoo Community 20.0
**Database tham chiếu:** `uth_canteen_erp13_test`
**Trạng thái:** Hướng dẫn DEMO – chờ peer review và xác nhận trên database mới
**Phạm vi:** Cài đặt module, import dữ liệu, cấu hình kho, phân quyền và quy trình mua hàng – nhận hàng.

---

## 1. Mục tiêu và phạm vi

Tài liệu hướng dẫn thành viên dự án thiết lập các chức năng Purchase và Inventory trên một database Odoo mới, sau đó thực hiện quy trình:

1. Chuẩn bị sản phẩm và nhà cung cấp.
2. Tạo Request for Quotation (RFQ).
3. Xác nhận RFQ thành Purchase Order (PO).
4. Nhận hàng và xác nhận phiếu nhập kho.
5. Xử lý trường hợp nhận đủ hoặc nhận thiếu.
6. Kiểm tra số lượng tồn kho sau khi nhận hàng.

Dữ liệu trong repository là dữ liệu DEMO phục vụ kiểm thử. Không sử dụng thông tin nhà cung cấp, giá hoặc số lượng này như dữ liệu thương mại thực tế.

### 1.1. Tài liệu liên quan

| Tài liệu | Nội dung |
|---|---|
| `import_guide.md` | Hướng dẫn import sản phẩm POS và nhà cung cấp ERP-16 |
| `products.csv` | 20 sản phẩm POS |
| `suppliers.csv` | 5 nhà cung cấp DEMO |
| `demo_raw_materials.csv` | Dữ liệu mẫu nguyên liệu, cần kiểm tra tương thích trước khi import |
| `supplier_product_mapping.csv` | Mapping nhà cung cấp – sản phẩm |
| `supplier_purchase_terms.md` | Điều khoản mua hàng DEMO |
| `erp17_test_report.md` | Kết quả cấu hình Purchase & Inventory |
| `erp19_test_report.md` | Kết quả kiểm thử nhận đủ và nhận thiếu |
| `test-cases.md` | Các kịch bản kiểm thử ERP-21 |

## 2. Yêu cầu trước khi bắt đầu

### 2.1. Môi trường

- Odoo Community 20.0.
- PostgreSQL tương thích với môi trường triển khai.
- Có quyền truy cập database mới và tài khoản Administrator.
- Các addon chuẩn `product`, `purchase`, `purchase_stock`, `stock` có sẵn.
- Addon tùy chỉnh `canteen_management` có trong source code nếu cần sử dụng các chức năng riêng của UTH Canteen.

### 2.2. Tạo database mới

1. Khởi động các dịch vụ Odoo và PostgreSQL theo cấu hình dự án.
2. Mở trang quản lý database của Odoo.
3. Tạo database mới với tên riêng cho lần kiểm thử.
4. Thiết lập tài khoản quản trị và thông tin cơ bản.
5. Đăng nhập bằng tài khoản Administrator.
6. Không sử dụng database kiểm thử hiện có làm database mới nếu mục tiêu là xác nhận khả năng triển khai độc lập.

**Lưu ý:** Các mã chứng từ như `P00003`, `WH/IN/00004` trong báo cáo cũ là mã của database kiểm thử tham chiếu. Database mới có thể sinh mã khác.

## 3. Cài đặt module

Cài đặt các ứng dụng sau từ Apps:

| Module / Ứng dụng | Mục đích | Yêu cầu |
|---|---|---|
| Contacts | Quản lý nhà cung cấp | Cần |
| Purchase | RFQ và Purchase Order | Cần |
| Inventory | Kho, vị trí kho, phiếu nhập | Cần |
| Product | Danh mục sản phẩm | Cần |
| UoM | Đơn vị tính | Cần |
| UTH Canteen Management (`canteen_management`) | Chức năng riêng của dự án | Khi triển khai đầy đủ dự án |

`purchase_stock` là module tích hợp Purchase với Inventory và là dependency của luồng mua hàng – kho. Kiểm tra module này đã được cài đặt cùng các dependency tương ứng.

### 3.1. Kiểm tra sau cài đặt

- Mở Purchase và xác nhận có thể truy cập Requests for Quotation.
- Mở Inventory và xác nhận có thể truy cập Operations.
- Mở Contacts và xác nhận có thể tạo nhà cung cấp.
- Mở Products và xác nhận có thể tạo sản phẩm.
- Nếu cài addon tùy chỉnh, kiểm tra trạng thái module là Installed.

**Chú ý:** Addon `canteen_management` có dependency riêng được khai báo trong `__manifest__.py`. Không thay thế việc cài module chuẩn bằng cách chỉ cài addon tùy chỉnh.

## 4. Cấu hình đơn vị tính và sản phẩm

### 4.1. Đơn vị tính

Bật Units of Measure trong cấu hình Inventory nếu chức năng này chưa được kích hoạt.

Đơn vị tham chiếu đã sử dụng trong kiểm thử:

- `kg` cho nguyên liệu cân theo khối lượng.
- `Units` cho sản phẩm được quản lý theo đơn vị.

Không tự đổi sản phẩm từ Units sang kg nếu chưa có xác nhận về quy cách và dữ liệu sản phẩm.

### 4.2. Phân biệt sản phẩm POS và nguyên liệu kho

Repository có nhiều nhóm dữ liệu với mục đích khác nhau:

- `products.csv`: 20 sản phẩm POS, có SKU UTH, `type=consu`, bật bán hàng và POS.
- `demo_raw_materials.csv`: dữ liệu mẫu nguyên liệu phục vụ Purchase & Inventory.

Không mặc định rằng 20 sản phẩm POS trong `products.csv` là nguyên liệu có thể quản lý tồn kho.

Đối với sản phẩm cần nhận hàng và theo dõi tồn kho:

1. Mở Products.
2. Tạo sản phẩm nguyên liệu hoặc kiểm tra sản phẩm đã tồn tại.
3. Đặt tên và Internal Reference/SKU duy nhất.
4. Chọn loại sản phẩm có hỗ trợ theo dõi tồn kho theo cấu hình Odoo 20.
5. Bật khả năng mua hàng (Can be Purchased).
6. Chọn đơn vị tính phù hợp, ví dụ kg hoặc Units.
7. Lưu sản phẩm.
8. Kiểm tra sản phẩm có thể được chọn trên dòng RFQ và có thể phát sinh receipt.

**Quan trọng:** Không import `demo_raw_materials.csv` trực tiếp vào database mới nếu chưa kiểm tra mapping trường trên Odoo 20. File mẫu có cột `detailed_type` và `uom_po_id/id`; không được mặc định các trường này tương thích với cấu trúc database hiện tại. Hãy xác nhận trường trên giao diện Import trước khi thực hiện.

## 5. Import dữ liệu CSV

### 5.1. Import sản phẩm POS

File: `functional/purchase_inventory/products.csv`

Mục đích: nhập 20 sản phẩm POS vào model Product (`product.template`).

Thực hiện:

1. Mở Products.
2. Chọn Import Records.
3. Chọn file `products.csv`.
4. Kiểm tra model đích là Product (`product.template`), không phải Product Variants.
5. Kiểm tra mapping các trường:
   - External ID
   - Internal Reference
   - Name
   - Product Type
   - Can be Sold
   - Sales Price
   - Unit of Measure
   - Available in POS
6. Chọn Test để kiểm tra dữ liệu.
7. Chỉ Import khi preview không có lỗi và mapping đúng.
8. Kiểm tra số lượng sản phẩm sau import.

**Xử lý External ID trên database mới:**

- Trên database mới hoàn toàn, lần import đầu có thể tạo các bản ghi và External ID từ CSV.
- Trên database đã có dữ liệu, phải kiểm tra các External ID có trỏ tới đúng sản phẩm hiện hữu trước khi import để tránh tạo bản ghi trùng.
- Không thay đổi tùy tiện các ID `__import__.*` trong CSV.

Kết quả tham chiếu ERP-16: 20 sản phẩm, 20 SKU duy nhất, 20 External ID. Import lần thứ hai trên database tham chiếu không làm tăng số lượng sản phẩm.

### 5.2. Import nhà cung cấp

File: `functional/purchase_inventory/suppliers.csv`

Mục đích: nhập 5 nhà cung cấp vào Contacts (`res.partner`).

Thực hiện:

1. Mở Contacts.
2. Chọn Import Records.
3. Chọn file `suppliers.csv`.
4. Kiểm tra mapping:
   - External ID
   - Name
   - Supplier Rank
   - Customer Rank
   - Email
   - Phone
   - Street
   - City
   - VAT
5. Chọn Test.
6. Kiểm tra preview và Import khi dữ liệu hợp lệ.
7. Mở từng nhà cung cấp để xác nhận thông tin.

Các nhà cung cấp DEMO:

- Công ty Thực phẩm An Sáng UTH.
- Hợp tác xã Nông sản Đà Lạt Xanh.
- Công ty Thực phẩm Tân Thuận.
- Nhà phân phối Đồ uống Sông Xanh.
- Công ty Gia vị Hương Việt.

External ID của nhà cung cấp trong CSV không có tiền tố `__import__.`. Giữ nguyên ID để tương thích với `demo_suppliers.csv`.

### 5.3. Kiểm tra sau import

- 20 sản phẩm POS có SKU duy nhất.
- 5 nhà cung cấp có Supplier Rank = 1.
- Customer Rank của các nhà cung cấp bằng 0 theo CSV.
- Email, điện thoại, địa chỉ và VAT khớp dữ liệu CSV.
- Import lại không tạo bản ghi trùng.
- Không tự xem Sales Price là Purchase Price.
- Giá mua và điều khoản mua hàng phải được xác nhận riêng.

### 5.4. Dữ liệu nguyên liệu

Các file `demo_raw_materials.csv`, `product_import_raw_materials_template.csv` và mapping nhà cung cấp là dữ liệu tham khảo.

Trước khi import nguyên liệu:
1. Xác nhận model đích.
2. Xác nhận các trường có trong Odoo 20.
3. Xác nhận loại sản phẩm có theo dõi tồn kho.
4. Xác nhận UoM và danh mục.
5. Chạy Test Import.
6. Kiểm tra preview trước khi Import.

Nếu mapping không hợp lệ, tạo nguyên liệu trực tiếp trên giao diện Odoo và ghi nhận các trường đã sử dụng. Không sửa cấu trúc CSV hoặc database một cách tùy tiện để ép import thành công.

## 6. Cấu hình Warehouse và Inventory

### 6.1. Warehouse tham chiếu

Cấu hình đã được kiểm thử trong ERP-17:

| Thuộc tính | Giá trị |
|---|---|
| Warehouse Code | `WH` |
| Warehouse Name | My Company |
| Receipt Steps | One-step receipt |
| Input Location | `WH/Đầu vào` |
| Stock Location | `WH/Tồn kho` |
| Stock UoM tham chiếu | kg |

### 6.2. Thiết lập

1. Mở Inventory.
2. Truy cập Configuration → Warehouses.
3. Mở warehouse hiện có hoặc tạo warehouse mới.
4. Kiểm tra mã kho và tên kho.
5. Thiết lập Incoming Shipments theo One-step receipt.
6. Lưu cấu hình.
7. Kiểm tra các vị trí kho được sinh ra.
8. Xác nhận vị trí tồn kho nội bộ và vị trí đầu vào phù hợp.

Tên menu có thể khác nhẹ theo quyền truy cập hoặc giao diện Odoo. Không tạo thêm warehouse trùng nếu database đã có warehouse mặc định phù hợp.

**Lưu ý:** ERP-17 đã kiểm thử quy trình nhận hàng một bước. Không đổi sang hai bước hoặc ba bước khi làm theo hướng dẫn này.

### 6.3. Kiểm tra cấu hình kho

- Có warehouse hoạt động.
- Có vị trí tồn kho nội bộ.
- Có thể tạo incoming receipt từ Purchase Order.
- Receipt sử dụng đúng operation type.
- Sau khi Validate, số lượng nhận được cập nhật vào tồn kho.

## 7. Phân quyền người dùng

Phân quyền theo nguyên tắc tối thiểu cần thiết. Tên nhóm có thể hiển thị khác nhau tùy phiên bản và bản dịch Odoo.

| Vai trò | Nhóm quyền tham chiếu | Phạm vi |
|---|---|---|
| System Administrator | Administration / Settings | Cài module, cấu hình hệ thống và phân quyền |
| Purchasing Staff | Purchase User | Tạo RFQ, quản lý đơn mua theo quyền được cấp |
| Purchasing Manager | Purchase Administrator / Manager | Quản lý và xác nhận nghiệp vụ mua hàng theo chính sách |
| Warehouse Staff | Inventory User | Xem và xử lý hoạt động kho được phân quyền |
| Inventory Manager | Inventory Administrator / Manager | Cấu hình kho và quản lý nghiệp vụ tồn kho |
| Canteen Manager | Nhóm quản lý phù hợp của dự án | Phối hợp nghiệp vụ căn tin |

### 7.1. Cách cấp quyền

1. Đăng nhập bằng Administrator.
2. Mở Settings → Users & Companies → Users.
3. Chọn người dùng.
4. Cấp quyền Purchase hoặc Inventory phù hợp.
5. Lưu.
6. Đăng xuất và đăng nhập lại bằng tài khoản được cấp quyền.
7. Kiểm tra người dùng chỉ truy cập được chức năng phù hợp vai trò.

### 7.2. Nguyên tắc bảo mật

- Không dùng tài khoản Administrator cho công việc hằng ngày.
- Nhân viên mua hàng không mặc nhiên được quyền cấu hình toàn bộ hệ thống.
- Nhân viên kho chỉ được cấp quyền cần thiết để xử lý receipt và hoạt động kho.
- Quyền xác nhận PO, điều chỉnh tồn và cấu hình kho phải được thống nhất với người phụ trách nghiệp vụ.
- Không khẳng định một cấp quyền đã đáp ứng quy trình phê duyệt nhiều cấp nếu chưa cấu hình và kiểm thử riêng.

## 8. Quy trình mua hàng và nhận hàng (SOP)

### 8.1. Tạo RFQ

1. Mở Purchase → Requests for Quotation.
2. Chọn New.
3. Chọn nhà cung cấp.
4. Thêm sản phẩm nguyên liệu đã được cấu hình để mua.
5. Nhập số lượng và đơn vị tính.
6. Nhập giá mua đã được phê duyệt cho dữ liệu kiểm thử.
7. Kiểm tra ngày dự kiến nhận hàng và các thông tin liên quan.
8. Lưu RFQ.

Không sử dụng Sales Price của sản phẩm làm giá mua nếu chưa có xác nhận.

### 8.2. Xác nhận Purchase Order

1. Mở RFQ vừa tạo.
2. Kiểm tra nhà cung cấp, sản phẩm, số lượng và giá.
3. Xác nhận theo quy trình phê duyệt đã thống nhất.
4. Chọn Confirm Order.
5. Kiểm tra trạng thái PO.
6. Mở Receipt được tạo từ PO.

### 8.3. Nhận đủ hàng

1. Mở incoming receipt từ PO.
2. Đối chiếu hàng thực tế với sản phẩm trên phiếu.
3. Kiểm tra số lượng và tình trạng hàng.
4. Nhập số lượng thực nhận.
5. Chọn Validate sau khi hoàn tất kiểm tra vật lý.
6. Xác nhận receipt chuyển sang Done.
7. Kiểm tra tồn kho tăng đúng số lượng đã nhận.

### 8.4. Nhận thiếu hàng

1. Mở incoming receipt.
2. Kiểm tra số lượng thực tế.
3. Cập nhật số lượng nhận đúng với số lượng hàng đạt yêu cầu.
4. Chọn Validate.
5. Khi Odoo hỏi cách xử lý phần còn lại, chọn tạo Backorder nếu nhà cung cấp sẽ giao tiếp.
6. Mở backorder và kiểm tra số lượng còn thiếu.
7. Kiểm tra PO đã nhận bao nhiêu và còn bao nhiêu.

Nếu nhà cung cấp xác nhận không giao phần còn lại, xử lý hủy số lượng còn lại theo quyết định nghiệp vụ thay vì giữ một backorder không còn cần thiết.

**Không xác nhận backorder nếu hàng chưa thực sự được giao và kiểm tra.**

### 8.5. Kiểm tra tồn kho

1. Mở Inventory.
2. Tra cứu sản phẩm tại vị trí tồn kho nội bộ.
3. Kiểm tra On Hand.
4. Đối chiếu số lượng tăng với số lượng thực nhận.
5. Nếu có chênh lệch, kiểm tra stock moves và các giao dịch liên quan trước khi điều chỉnh.

### 8.6. Điều chỉnh tồn kho

Chỉ thực hiện khi đã kiểm kê thực tế:

1. Mở Inventory và chức năng kiểm kê/Physical Inventory.
2. Chọn sản phẩm và vị trí kho.
3. Ghi nhận số lượng hệ thống.
4. Nhập số lượng kiểm đếm thực tế.
5. Kiểm tra chênh lệch.
6. Ghi lý do điều chỉnh theo quy định.
7. Xác nhận điều chỉnh bởi người có thẩm quyền.
8. Kiểm tra số lượng tồn sau điều chỉnh.

Không dùng Inventory Adjustment để thay thế thao tác nhận hàng từ PO.

## 9. Bằng chứng và tiêu chí hoàn thành

Mỗi lần triển khai database mới cần lưu:

- Tên database và phiên bản Odoo.
- Danh sách module đã cài.
- Ảnh cấu hình warehouse và receipt steps.
- Kết quả Test Import và Import CSV.
- Ảnh RFQ/PO.
- Ảnh receipt Done.
- Ảnh backorder nếu có.
- Ảnh tồn kho trước và sau.
- Mã chứng từ thực tế của database mới.
- Người thực hiện và ngày kiểm thử.

ERP-21 chỉ được xem là hoàn thành sau khi một thành viên khác có thể tạo database mới và thực hiện quy trình mua hàng – nhận hàng theo hướng dẫn, không cần trợ giúp đặc biệt; đồng thời tài liệu được peer review và chấp nhận.

## 10. Giới hạn và lưu ý

- Các báo cáo ERP-17 và ERP-19 được thực hiện trên database tham chiếu `uth_canteen_erp13_test`.
- Database mới phải tự xác nhận lại module, External ID, sản phẩm, nhà cung cấp và warehouse.
- Giá mua DEMO chưa được xác nhận là giá thương mại.
- Một số file nguyên liệu có trường cần kiểm tra tương thích với Odoo 20 trước khi import.
- Tài liệu này không bao gồm hóa đơn nhà cung cấp, thanh toán, định giá kế toán, thuế hoặc phê duyệt nhiều cấp chưa được kiểm thử.
- Kết quả ERP-20 cần được đối chiếu với báo cáo và PR tương ứng sau khi được tích hợp vào nhánh dùng chung.
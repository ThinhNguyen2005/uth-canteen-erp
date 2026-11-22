# PRODUCT CATALOG SPECIFICATION

## UTH Canteen ERP – ERP-13

|Thông tin|Giá trị|
|-|-|
|Project|UTH Canteen ERP|
|Jira Task|ERP-13|
|Responsible|TV2 – Purchase \& Inventory|
|Target Version|Odoo Community 20.0|
|Currency|VND|
|Status|Draft – Pending Validation|
|Related Epic|KAN-119|

\---

## 1\. Mục đích

Tài liệu này mô tả cấu trúc và quy tắc thiết kế danh mục sản phẩm cho UTH Canteen ERP. Danh mục được chuẩn bị để sử dụng trong các nghiệp vụ Purchase, Inventory và POS, đồng thời hỗ trợ dữ liệu món ăn trên thực đơn QR.

Mục tiêu của ERP-13 là có ít nhất 20 mặt hàng với SKU duy nhất, tên và loại sản phẩm rõ ràng, đơn vị đo hợp lệ, giá phù hợp và thuộc tính đáp ứng nghiệp vụ. Danh mục phải được TV3 xác nhận có thể tái sử dụng.

## 2\. Phạm vi dữ liệu

### 2.1. Nguyên liệu (Raw Materials)

Nguồn dữ liệu hiện có: `functional/purchase\_inventory/demo\_raw\_materials.csv`.

File hiện có 10 dòng nguyên liệu:

* Gạo ST25.
* Đùi gà.
* Sườn non heo.
* Thịt bò.
* Bánh phở.
* Dầu ăn.
* Trà lài.
* Sữa đặc.
* Rau củ.
* Trứng gà.

Các bản ghi mẫu hiện bật `purchase\_ok = True`, `sale\_ok = False` và có `list\_price = 0`. Cách thiết lập này phù hợp với nguyên liệu chỉ mua vào để chế biến, không bán trực tiếp. Cần xác nhận lại với nghiệp vụ thực tế trước khi chốt.

### 2.2. Sản phẩm bán trực tiếp (POS Products)

Nguồn tham khảo hiện có: `addons/canteen\_management/demo/canteen\_demo\_data.xml`.

File XML demo chứa 13 sản phẩm POS thuộc các nhóm:

* Cơm (`rice`).
* Bún/Phở/Mì (`noodle`).
* Đồ uống (`drink`).
* Ăn vặt (`snack`).
* Đồ ăn nhanh (`fastfood`).

Các sản phẩm POS đã có SKU dạng `UTH-RICE-01`, `UTH-DRINK-01`, v.v. Cần tái sử dụng các sản phẩm phù hợp và tránh tạo bản ghi trùng lặp.

**Lưu ý về phạm vi:** Repository đang có tổng cộng 23 bản ghi sản phẩm mẫu nếu cộng 10 nguyên liệu và 13 sản phẩm POS. Con số này chưa tự động chứng minh ERP-13 đã đạt nghiệm thu: cần xác nhận danh sách nào thuộc danh mục bàn giao, SKU, giá, UoM, khả năng import và việc TV3 tái sử dụng được.

## 3\. Quy ước SKU

### 3.1. Trường lưu SKU

SKU được lưu trong trường `default\_code` (Internal Reference) của sản phẩm Odoo. Trường `id` trong CSV là External ID dùng để nhận diện bản ghi khi import; `id` và `default\_code` không thay thế cho nhau.

### 3.2. Cấu trúc đề xuất

* Nguyên liệu: `RM-\\\[CATEGORY]-\\\[NUMBER]`
* Sản phẩm POS hiện có: giữ nguyên quy ước `UTH-\\\[CATEGORY]-\\\[NUMBER]` đã dùng trong dữ liệu demo.

### 3.3. SKU đề xuất cho 10 nguyên liệu hiện có

|External ID|SKU đề xuất|Sản phẩm|
|-|-|-|
|`raw\_rice\_st25`|`RM-RIC-001`|Gạo ST25|
|`raw\_chicken\_thigh`|`RM-MEA-001`|Đùi gà|
|`raw\_pork\_rib`|`RM-MEA-002`|Sườn non heo|
|`raw\_beef\_tenderloin`|`RM-MEA-003`|Thịt bò|
|`raw\_pho\_noodle`|`RM-NDL-001`|Bánh phở|
|`raw\_cooking\_oil`|`RM-OIL-001`|Dầu ăn|
|`raw\_green\_tea`|`RM-TEA-001`|Trà lài|
|`raw\_condensed\_milk`|`RM-MIL-001`|Sữa đặc|
|`raw\_vegetable\_mix`|`RM-VEG-001`|Rau củ|
|`raw\_egg\_chicken`|`RM-EGG-001`|Trứng gà|

Các SKU trên là đề xuất của TV2, cần kiểm tra không trùng với SKU đang có trong database Odoo và được nhóm thống nhất trước khi import.

### 3.4. Quy tắc

* SKU duy nhất trong toàn bộ danh mục.
* Dùng chữ in hoa, chữ số và dấu gạch ngang.
* Không dùng dấu tiếng Việt hoặc khoảng trắng.
* Không cấp lại SKU đã sử dụng cho sản phẩm khác.
* Không thay đổi SKU tùy tiện sau khi sản phẩm đã được tham chiếu bởi giao dịch.

## 4\. Cấu trúc dữ liệu sản phẩm

Danh mục dự kiến dựa trên model sản phẩm chuẩn `product.template` của Odoo.

|Trường|Tên kỹ thuật|Mục đích|
|-|-|-|
|External ID|`id`|Định danh bản ghi khi import|
|SKU|`default\_code`|Mã nội bộ sản phẩm|
|Tên sản phẩm|`name`|Tên hiển thị|
|Loại sản phẩm|`type`|Loại sản phẩm theo Odoo 20|
|Danh mục chuẩn|`categ\_id`|Nhóm sản phẩm chuẩn Odoo|
|Giá bán|`list\_price`|Giá bán bằng VND|
|Giá vốn|`standard\_price`|Giá vốn sản phẩm|
|Đơn vị tồn|`uom\_id`|Đơn vị kiểm đếm/tồn kho|
|Đơn vị mua|`product.supplierinfo.uom\_id`|Đơn vị mua được cấu hình theo từng nhà cung cấp|
|Có thể mua|`purchase\_ok`|Cho phép mua hàng|
|Có thể bán|`sale\_ok`|Cho phép bán hàng|
|Theo dõi tồn|`is\_storable`|Cấu hình theo dõi số lượng tồn; cần kiểm tra trên Odoo 20 instance|
|Có trên POS|`available\_in\_pos`|Cho phép hiển thị trên POS|
|Nhóm món căn tin|`canteen\_category`|Phân loại món theo Data Contract|
|Hiển thị menu|`canteen\_published`|Cờ hiển thị menu theo Data Contract|
|Tạm hết món|`canteen\_is\_out\_of\_stock`|Trạng thái hết món theo Data Contract|
|Hiệu lực|`active`|Trạng thái hoạt động|

Ghi chú:

* `categ\_id` là danh mục sản phẩm chuẩn Odoo; `canteen\_category` là phân loại món ăn riêng của UTH Canteen.
* `standard\_price` là giá vốn, không phải bảng giá mua riêng theo từng nhà cung cấp.
* Nhà cung cấp và giá mua theo nhà cung cấp cần được cấu hình bằng Vendor Pricelist nếu nghiệp vụ yêu cầu.
* Các trường mở rộng như `available\_in\_pos`, `canteen\_category`, `canteen\_published` và `canteen\_is\_out\_of\_stock` phải khớp với module và Data Contract thực tế.
* Trước khi tạo CSV import, cần xác nhận chính xác tên trường và giá trị lựa chọn trên Odoo 20 đang chạy.

## 5\. Quy tắc đơn vị đo (Unit of Measure)

### 5.1. Nguyên tắc

* Đơn vị tồn kho phải phù hợp với cách căn tin kiểm đếm thực tế.
* Đơn vị mua hàng phải phản ánh cách nhà cung cấp giao hàng.
* Nếu đơn vị mua và đơn vị tồn khác nhau, hai đơn vị phải thuộc cùng nhóm đo lường và có tỷ lệ chuyển đổi hợp lệ.
* Không tự tạo đơn vị đo mới nếu Odoo đã có đơn vị phù hợp.
* Phải ghi rõ giá mua đang tính theo kg, quả, lon, vỉ, thùng hay can; không suy luận đơn vị giá chỉ từ tên sản phẩm.

### 5.2. Các trường hợp cần xác nhận

|Sản phẩm|Đơn vị hiện có trong CSV|Câu hỏi cần xác nhận|
|-|-|-|
|Gạo ST25|kg / kg|Giá vốn 24.000 VND tính theo kg hay bao? Tên đang ghi bao 25kg|
|Đùi gà|kg / kg|Giá vốn tính theo kg|
|Sườn non heo|kg / kg|Giá vốn tính theo kg|
|Thịt bò|kg / kg|Giá vốn tính theo kg|
|Bánh phở|kg / kg|Giá vốn tính theo kg|
|Dầu ăn|Units / Units|Một Units là một can 25L? Giá vốn 750.000 VND/can?|
|Trà lài|kg / kg|Giá vốn tính theo kg|
|Sữa đặc|Units / Units|Một Units là một lon hay một thùng 48 lon? Giá vốn 1.120.000 VND đang tính theo đơn vị nào?|
|Rau củ|kg / kg|Giá vốn tính theo kg|
|Trứng gà|Units / Units|Một Units là một quả hay một vỉ 30 quả? Giá vốn 75.000 VND đang tính theo đơn vị nào?|

Không thay đổi UoM hoặc tỷ lệ chuyển đổi trước khi xác nhận cách nhập hàng và kiểm đếm kho.

## 6\. Quy tắc giá

### 6.1. Giá mua và giá vốn

* `standard\_price` lưu giá vốn của sản phẩm trong Odoo.
* Giá mua theo từng nhà cung cấp có thể được cấu hình riêng trong Vendor Pricelist (`seller\_ids`).
* Giá mẫu trong CSV là dữ liệu demo, chưa được xác nhận là báo giá thực tế.
* Giá vốn phải gắn với đơn vị tính rõ ràng.
* Không dùng giá của một thùng làm giá của một lon hoặc ngược lại nếu chưa quy đổi.

### 6.2. Giá bán

* Sản phẩm bán trực tiếp cần có `sale\_ok = True` và giá bán lớn hơn 0.
* Nguyên liệu không bán trực tiếp có thể đặt `sale\_ok = False`; giá bán 0 chỉ áp dụng khi phù hợp với cấu hình và chính sách của dự án.
* Giá bán sử dụng VND theo quy ước dự án; không tự thêm phần thập phân.
* Không tự đặt giá bán hoặc giá mua giả làm dữ liệu thực tế. Nếu dùng giá minh họa, phải ghi rõ là giá demo.

## 7\. Quy tắc nghiệp vụ Purchase, Inventory và POS

### 7.1. Purchase

* Sản phẩm cần mua phải bật `purchase\_ok = True`.
* Hàng hóa vừa mua vừa bán có thể bật đồng thời `purchase\_ok` và `sale\_ok`.
* Nhà cung cấp liên kết với sản phẩm theo cấu hình Vendor Pricelist khi có dữ liệu được xác nhận.
* MOQ, thời gian giao hàng và giá NCC chỉ điền khi có cơ sở dữ liệu.

### 7.2. Inventory

* Xác định sản phẩm nào cần theo dõi tồn kho thực tế.
* Chọn UoM tồn phù hợp với cách kiểm đếm.
* Chỉ bật Lot Tracking cho sản phẩm cần quản lý theo lô/hạn sử dụng.
* Không bật Serial Tracking cho hàng tiêu dùng thông thường nếu không có yêu cầu.
* Kiểm tra số lượng nhập và tồn bằng đơn vị thống nhất.

### 7.3. POS và Menu QR

Sản phẩm bán trực tiếp cần được cấu hình để bán và hiển thị trên POS theo Data Contract và cấu hình module thực tế.

Các nhóm `canteen\_category` được Data Contract quy định:

* `rice`
* `noodle`
* `drink`
* `snack`
* `fastfood`

Các trường `canteen\_published` và `canteen\_is\_out\_of\_stock` phải được xác nhận với module thực tế trước khi import hoặc test.

## 8\. Quy tắc kiểm tra dữ liệu

|ID|Tiêu chí|Điều kiện|
|-|-|-|
|VAL-01|Số lượng|Có ít nhất 20 sản phẩm trong danh mục được đề xuất nghiệm thu|
|VAL-02|SKU|Không trùng lặp và không rỗng|
|VAL-03|External ID|Không trùng lặp|
|VAL-04|Tên|Không để trống|
|VAL-05|Loại sản phẩm|Khớp các giá trị hợp lệ của Odoo 20|
|VAL-06|Giá bán|Không âm; sản phẩm bán phải có giá lớn hơn 0|
|VAL-07|Giá vốn|Không âm và xác định rõ đơn vị tính|
|VAL-08|Đơn vị tồn|Có tồn tại trong Odoo|
|VAL-09|Đơn vị mua|Có tồn tại; cùng nhóm UoM với đơn vị tồn nếu cần chuyển đổi|
|VAL-10|Purchase|Sản phẩm cần mua phải bật `purchase\_ok`|
|VAL-11|POS|Sản phẩm POS phải bật thuộc tính bán và POS tương ứng|
|VAL-12|Inventory|Xác nhận cấu hình theo dõi tồn cho từng sản phẩm|
|VAL-13|Danh mục|Giá trị danh mục hợp lệ|
|VAL-14|Tiền tệ|Giá theo VND và không có phần thập phân theo quy ước dự án|
|VAL-15|Trùng bản ghi|Không tạo sản phẩm trùng External ID, SKU hoặc sản phẩm demo đã có|

## 9\. Kế hoạch kiểm thử và nghiệm thu

### 9.1. Kiểm tra file

* Kiểm tra header và định dạng CSV.
* Kiểm tra số lượng sản phẩm.
* Kiểm tra SKU và External ID duy nhất.
* Kiểm tra giá và đơn vị tính.
* Đối chiếu với dữ liệu demo hiện có.
* Kiểm tra các trường kỹ thuật trước khi import.

### 9.2. Kiểm thử trên Odoo

Thực hiện trên database thử nghiệm:

1. Import danh mục sản phẩm.
2. Kiểm tra bản ghi được tạo hoặc cập nhật đúng.
3. Kiểm tra Internal Reference.
4. Kiểm tra giá bán và giá vốn.
5. Kiểm tra đơn vị tồn và đơn vị mua.
6. Kiểm tra Purchase và Inventory.
7. Kiểm tra khả năng sử dụng sản phẩm trong POS với TV3.
8. Ghi lại lỗi, log và kết quả kiểm thử.

### 9.3. Bằng chứng nghiệm thu

* File CSV danh mục sản phẩm.
* Tài liệu đặc tả danh mục.
* Ảnh chụp danh sách sản phẩm trên Odoo.
* Test report hoặc log import.
* Link Pull Request.
* Xác nhận của TV3 về khả năng tái sử dụng danh mục.

## 10\. Nội dung cần phối hợp và xác nhận

|Nội dung|Thành viên|
|-|-|
|Xác nhận danh sách sản phẩm dùng chung POS|TV3|
|Xác nhận trường dữ liệu và model sản phẩm|TV4|
|Xác nhận giao diện và thuộc tính POS|TV5|
|Xác nhận quy trình tích hợp|TV1|

Các điểm chưa được chốt:

1. CSV nguồn đang có cột `detailed\_type`; cần kiểm tra tên trường import đúng trên Odoo 20 trước khi đổi sang `type`.
2. CSV nguồn chưa có `default\_code` và chưa thể hiện rõ cấu hình theo dõi tồn.
3. XML demo đang dùng `canteen\_available`, trong khi Data Contract quy định `canteen\_published`; cần TV4/TV5 xác nhận và xử lý thống nhất.
4. Đơn vị tính và đơn vị giá cho dầu ăn, sữa đặc, trứng gà và gạo cần được xác nhận.
5. Giá và thông tin liên hệ của nhà cung cấp demo chưa được xác minh là dữ liệu thực tế.

TV2 không tự ý sửa file thuộc quyền sở hữu của thành viên khác. Các thay đổi liên vùng cần có sự phối hợp/review của owner.

## 11\. Tài liệu tham khảo

* `docs/srs.md`
* `docs/data-contract.md`
* `AGENTS.md`
* `functional/purchase\_inventory/demo\_raw\_materials.csv`
* `functional/purchase\_inventory/demo\_suppliers.csv`
* `addons/canteen\_management/demo/canteen\_demo\_data.xml`
* [Odoo 20 – Product Types](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/inventory/product_management/configure/type.html)
* [Odoo 20 – Units of Measure](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/inventory/product_management/configure/uom.html)
* [Odoo 20 – Purchase](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/purchase.html)

**Document Owner:** TV2 – Purchase \& Inventory
**Document Status:** Draft – Pending Validation and TV3 Review.

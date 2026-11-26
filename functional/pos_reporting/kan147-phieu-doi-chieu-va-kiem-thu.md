# KAN-147 Phiếu đối chiếu và kiểm tra giá POS

Trạng thái: **Chưa thực hiện trên Odoo**. Tài liệu dùng chuẩn bị review và ghi kết quả, không xác nhận giá được duyệt hay sản phẩm đã có trên database thử.

## Kết quả rà soát tĩnh

Nguồn catalog: functional/purchase_inventory/product_catalog.csv tại develop commit 7030bc746bf74500d8cf3d265de4282f9aa8815c. Nguồn demo: addons/canteen_management/demo/canteen_demo_data.xml tại cùng commit.

- Có 20 dòng đánh dấu available_in_pos; 20 SKU và 20 external ID không trống, không trùng; tên, giá, đơn vị nguồn và nhóm đều có dữ liệu.
- Trong đó 13 SKU có trong XML demo; external ID, tên, giá và nhóm của 13 dòng khớp giữa hai nguồn. Catalog ghi nhận tái sử dụng 13 sản phẩm nhưng vẫn chờ kiểm chứng sản phẩm và luồng tồn trên Odoo.
- Bảy dòng còn lại được catalog đánh dấu chờ TV3 review, giá và luồng nghiệp vụ. Cả 20 giá trong bảng tham khảo đều chờ phê duyệt; kiểm tra tĩnh không xác nhận SKU, giá, thuế hoặc tồn trên database.
- Cả 20 dòng dùng UoM nguồn uom.product_uom_unit. TV2 cần xác nhận đơn vị bán thực tế và quy đổi với đơn vị kho nếu có. Không suy ra tự động từng món có đơn vị nghiệp vụ nào.

## Bảng ghi quyết định

| Nội dung | Cần xác nhận | Người xác nhận và ngày | Quyết định hoặc liên kết |
| --- | --- | --- | --- |
| Catalog dùng chung | Phiên bản, danh sách SKU, tên, đơn vị và dữ liệu hiện có trên database | | |
| Giá bán | Giá từng SKU, ngày hiệu lực và người có thẩm quyền duyệt | | |
| Thuế | Mức thuế, áp dụng cho món nào, bao gồm trong giá hay cộng thêm, quy tắc làm tròn | | |
| Giá ưu đãi và combo | Chính sách, điều kiện, phạm vi, thời gian, cộng dồn, khả năng bản Odoo đang chạy | | |
| Quyền | Tài khoản quản lý giá và thu ngân, quyền sửa giá và phạm vi kiểm thử | | |
| Môi trường | URL, database thử, quầy và phạm vi được phép ghi | | |

## Kịch bản kiểm thử giá

Chỉ chạy sau khi có phê duyệt và quyền trên database thử. Trước mỗi ca ghi người chạy, ngày giờ, Odoo phiên bản, DB/quầy, mã phiên, SKU, đơn vị, giá và thuế đã duyệt. Ghi mã đơn nếu có, kết quả thực tế, trạng thái, ảnh và đường dẫn chứng cứ. Khi điều kiện chưa có, để Chưa thực hiện; nếu đã bắt đầu nhưng bị chặn, ghi Blocked và lý do.

| ID | Kiểm tra | Kỳ vọng cần so | Bằng chứng | Trạng thái |
| --- | --- | --- | --- | --- |
| GIA-01 | Tra SKU do TV2 xác nhận trong catalog và POS | Cùng sản phẩm, đơn vị và giá đã duyệt; không phát sinh bản ghi trùng | Catalog, chi tiết sản phẩm, POS | Chưa thực hiện |
| GIA-02 | Một món, số lượng 1; thanh toán tiền mặt | Giá dòng, thuế và tổng khớp quy tắc đã duyệt; biên lai khớp đơn | Giỏ, thuế, thanh toán, biên lai | Chưa thực hiện |
| GIA-03 | Hai món hoặc số lượng lớn hơn 1; thanh toán mô phỏng | Tổng bằng tổng dòng và điều chỉnh thuế/giảm giá/làm tròn theo cấu hình đã duyệt; phương thức đúng | Giỏ từng dòng, cách tính, biên lai | Chưa thực hiện |
| GIA-04 | So quyền quản lý giá và thu ngân | Hành vi truy cập/sửa giá đúng ma trận quyền được TV1 duyệt | Cấu hình quyền, thao tác, thông báo và kết quả | Chưa thực hiện |
| GIA-05 | Thử ưu đãi/combo nếu có chính sách và tính năng được duyệt | Giá ưu đãi và điều kiện đúng quyết định; giá niêm yết gốc được giữ theo chính sách | Cấu hình, điều kiện, giỏ và biên lai | Chưa thực hiện |

Nếu không có chính sách hoặc tính năng ưu đãi để thử, ghi rõ lý do và xin quyết định người phụ trách; không tự kết luận phiên bản Odoo không hỗ trợ.

Mẫu từng ca: ID __; ngày/giờ/người chạy __; DB/quầy/phiên __; SKU/đơn vị __; giá và thuế đã duyệt __; mã đơn __; phép tính kỳ vọng __; kết quả thực tế __; ảnh/link __; trạng thái Chưa thực hiện; ghi chú __.

## Điều kiện còn thiếu

TV1 xác nhận database thử, URL, tài khoản và phạm vi ghi; TV2 xác nhận catalog, đơn vị và tình trạng sản phẩm trên database; người có thẩm quyền duyệt giá, thuế và chính sách ưu đãi. Cần review KAN-146, chạy các ca và đính kèm kết quả trước khi đề nghị nghiệm thu KAN-147.

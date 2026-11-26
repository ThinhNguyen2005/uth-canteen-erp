# KAN-147 ERP-25 Đề xuất mô hình giá bán POS

Trạng thái: **Dự thảo chờ xác nhận**. Chưa áp dụng trên Odoo, chưa được duyệt giá hoặc kiểm thử thực tế. Bảng giá kèm theo trích catalog TV2 trên develop tại commit 7030bc746bf74500d8cf3d265de4282f9aa8815c; không chứng minh dữ liệu đã có trên database thử.

## Phương án đề xuất

- Dùng một bản ghi sản phẩm chung của TV2, đối chiếu External ID và SKU; không tạo catalog thứ hai cho POS. Chỉ đưa lên quầy những sản phẩm đã được TV2 xác nhận.
- Dùng giá niêm yết VND theo sản phẩm và đơn vị bán đã được duyệt. Bảng kèm giữ nguyên giá và UoM trong catalog nguồn, không tự quyết định giá thực tế hay quy đổi đơn vị.
- Người có thẩm quyền xác nhận mức thuế, hiệu lực và giá đã bao gồm thuế hay chưa trước khi cấu hình. Kiểm tra giá và tổng trên POS với cấu hình thực tế; không giả định mức thuế.
- Ưu đãi sinh viên và combo chỉ áp dụng sau khi thống nhất đối tượng, điều kiện, thời gian, cách xác minh, quy tắc cộng dồn và kiểm tra khả năng của bản Odoo đang chạy. Không ghi đè giá niêm yết; nếu chưa xác nhận, để chưa triển khai.
- TV1 xác nhận quyền quản lý giá và quyền thu ngân. Thử quyền bằng tài khoản được cấp trên database thử trước khi kết luận.

## Nguồn và phạm vi bảng giá mẫu

Nguồn: functional/purchase_inventory/product_catalog.csv trên develop tại commit nêu trên; đối chiếu với addons/canteen_management/demo/canteen_demo_data.xml. Catalog có 20 dòng đánh dấu POS: 13 dòng ghi nhận đồng ý tái sử dụng và 7 dòng đang chờ TV3 review, giá và luồng nghiệp vụ. Đồng ý tái sử dụng không đồng nghĩa phê duyệt giá, xác nhận tồn hay đã kiểm thử Odoo. Bảy món sau là đề xuất, không xem là đã có trên database. Tên, mã, đơn vị và giá trong CSV là ảnh chụp nguồn để review, không phải chỉ dẫn import.

Bảng giá: kan147-bang-gia-tham-khao.csv. Trạng thái giá, thuế và kết quả thực tế đều chờ xác nhận. Nếu dữ liệu thực tế khác nguồn, yêu cầu TV2 xác nhận và cập nhật nguồn chung trước khi quyết định.

## Kiểm tra và nghiệm thu

1. TV2 xác nhận SKU, tên, đơn vị bán, giá và trạng thái trên database thử; kiểm tra không trùng bản ghi. Phân biệt đơn vị bán và đơn vị kho, không tự suy ra hệ số quy đổi.
2. Người có thẩm quyền duyệt giá, thuế và điều kiện ưu đãi; ghi người duyệt, ngày và liên kết quyết định.
3. Trên database thử do TV1 xác nhận, kiểm tra POS hiển thị đúng SKU, đơn vị, giá và tổng khi thanh toán tiền mặt và chuyển khoản mô phỏng; kiểm tra quyền thay đổi giá. Nếu có ưu đãi đã duyệt, kiểm tra điều kiện và kết quả. Lưu phiên bản Odoo, mã đơn, ảnh và kết quả thực tế.
4. Gắn bảng giá, kết quả review và bằng chứng vào KAN-147; kiểm tra phụ thuộc KAN-146. Chỉ chuyển Done sau khi đáp ứng các điều kiện.

Chưa thể chốt giá, thuế, quyền, ưu đãi hay kiểm thử khi chưa có xác nhận và database thử. Kiểm tra CSV không phải kiểm thử Odoo.

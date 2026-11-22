# Kịch bản kiểm thử POS

Dùng DB thử do TV1 duyệt. Ghi mã quầy, phiên, đơn, SKU, tài khoản theo vai trò và bằng chứng tương ứng. Dữ liệu trong bước kiểm thử là đầu vào dự kiến.

| ID | Mục tiêu | Bước và dữ liệu | Kết quả mong đợi |
| --- | --- | --- | --- |
| TC-POS-01 | Mở phiên | Đăng nhập tài khoản thu ngân, chọn quầy, nhập tiền đầu ca và mở phiên. | Phiên mở đúng quầy, ghi nhận đúng tiền đầu ca. |
| TC-POS-02 | Bán một món | Chọn 1 món TV2 có giá xác nhận, thanh toán đủ. | Đơn hoàn tất và ghi đúng món, số lượng, giá. |
| TC-POS-03 | Bán nhiều món | Thêm hai món khác nhau, tăng giảm số lượng, thanh toán. | Đơn lưu các dòng và số lượng cuối cùng. |
| TC-POS-04 | Kiểm tra tổng | Tính độc lập theo giá đã duyệt, thuế, chiết khấu và làm tròn áp dụng. So với giỏ và biên lai. | Tổng giỏ và biên lai khớp phép tính. |
| TC-POS-05 | Tiền mặt và tiền thừa | Nhập số tiền khách đưa lớn hơn tổng và hoàn tất. | Tiền thừa bằng số nhận trừ tổng. Doanh thu ghi đúng giá trị đơn. |
| TC-POS-06 | Chuyển khoản mô phỏng | Chọn phương thức mô phỏng, thu ngân xác nhận thủ công và hoàn tất. | Đơn ghi đúng phương thức. Không phát sinh giao dịch ngân hàng. |
| TC-POS-07 | Tra cứu đơn và biên lai | Ghi mã biên lai, mở danh sách đơn và tìm theo mã. | Tra được đúng đơn, giá trị và phương thức thanh toán. |
| TC-POS-08 | Đóng phiên và đối soát | Sau khi đồng bộ đơn, kiểm đếm tiền và đóng ca. Ghi tiền đầu ca, tiền bán ròng, thu/chi và số đếm. | Số kỳ vọng khớp phép đối chiếu. Chênh lệch nếu có được ghi riêng. |
| TC-POS-09 | Tồn kho sau bán | Ghi tồn tại vị trí xuất của một SKU có quản lý tồn. Bán 3 đơn vị, kiểm tra phiếu xuất và tồn sau khi chuyển kho hoàn tất. | Tồn giảm đúng 3 nếu không có biến động khác. Phiếu xuất đúng vị trí và SKU. |
| TC-POS-10 | Doanh thu | Lọc cùng ngày, quầy, phiên và trạng thái. So tổng tiền và số đơn với danh sách giao dịch. | Số đơn và doanh thu khớp theo cùng quy ước thuế, làm tròn và hoàn tiền. |
| TC-POS-11 | Lượng bán theo món | Nhóm báo cáo theo sản phẩm, đối chiếu tổng số lượng dòng đơn theo SKU. | Số lượng khớp theo SKU và cùng quy ước hoàn tiền. |
| TC-POS-12 | Giới hạn quyền thu ngân | Quản lý mở cấu hình quầy. Đăng nhập riêng bằng tài khoản thu ngân và thử truy cập, chỉnh cấu hình tương ứng. | Quản lý có quyền. Thu ngân vẫn bán được và bị chặn chỉnh cấu hình quản lý. |

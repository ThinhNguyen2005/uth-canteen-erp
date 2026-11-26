# KAN-146 — Chuẩn bị kiểm thử POS

Ghi chú cập nhật: các trạng thái bên dưới phản ánh kế hoạch ban đầu. Xem `kan146-ket-qua-native-20261126.md` để biết các ca ORM đã chạy và giới hạn còn lại.

Trạng thái: **Chưa thực hiện**. Bộ 12 ca dựa trên functional/pos_reporting/test-cases.md của nhánh main. Chỉ chạy trên database thử và trong phạm vi ghi được TV1 xác nhận; dùng danh mục, giá, kho và tồn do TV2 bàn giao. Không dùng dữ liệu khách hoặc giao dịch ngân hàng thật.

## Quy trình thu ngân và thanh toán mô phỏng

1. Chờ TV1 xác nhận tên/URL database, tài khoản cấu hình POS và tạo user thử, quyền ghi ít nhất 30 đơn trừ tồn và phương thức chuyển khoản mô phỏng do thu ngân xác nhận thủ công. Chờ TV2 bàn giao mã, tên, giá, nhóm, kho/vị trí và sản phẩm theo dõi tồn đủ số lượng.
2. Quản lý kiểm tra cấu hình quầy và phương thức hiện có; chỉ cấu hình khi được phép. Chuyển khoản mô phỏng không kết nối ngân hàng hoặc cổng thanh toán. Nếu cấu hình thực tế khác dự kiến, hỏi TV1 trước khi tiếp tục.
3. Thu ngân mở phiên, ghi tiền đầu ca; chọn món, số lượng, kiểm tra tổng; nhận tiền mặt hoặc chọn chuyển khoản mô phỏng và xác nhận thủ công. Tiền thừa bằng tiền khách đưa trừ tổng. Lưu mã đơn và biên lai.
4. Đồng bộ và tra đơn, kiểm tra xuất kho và tồn cùng vị trí. Cuối ca ghi tiền mặt dự kiến, thực đếm, chênh lệch và đóng phiên. Đối chiếu tiền mô phỏng riêng, không cộng vào két.

## Rà soát 12 ca và bảng ghi kết quả

Mỗi ca ghi ngày/giờ, người chạy, DB/quầy, mã phiên, mã đơn, tiền mặt đầu ca và cuối ca thực đếm, phương thức, kết quả thực tế và đường dẫn ảnh. Ghi N/A kèm lý do nếu không tạo đơn hoặc không thanh toán; nếu chưa đóng ca thì bổ sung tiền cuối ca sau. Không ghi mật khẩu. Chỉ ghi Pass sau khi so kết quả thực tế với kỳ vọng; dùng Fail hoặc Blocked kèm lý do khi phù hợp.

| ID | Kỳ vọng | Ảnh cần lưu | Trạng thái | Kết quả thực tế / ảnh |
| --- | --- | --- | --- | --- |
| TC-POS-01 | Mở đúng quầy và tiền đầu ca | Quầy, phiên và tiền đầu ca | Chưa thực hiện | |
| TC-POS-02 | Bán một món đúng số lượng, giá | Giỏ, thanh toán và biên lai/mã đơn | Chưa thực hiện | |
| TC-POS-03 | Nhiều món, số lượng sau chỉnh đúng | Giỏ sau chỉnh và biên lai | Chưa thực hiện | |
| TC-POS-04 | Tổng khớp tính độc lập theo thuế, giảm giá và làm tròn đã xác nhận | Giỏ, chi tiết thuế/giảm giá và biên lai | Chưa thực hiện | |
| TC-POS-05 | Tiền thừa đúng; doanh thu đúng giá trị đơn | Số tiền nhận, tiền thừa và biên lai | Chưa thực hiện | |
| TC-POS-06 | Ghi đúng chuyển khoản mô phỏng, xác nhận thủ công | Màn thanh toán và phương thức trên đơn | Chưa thực hiện | |
| TC-POS-07 | Tra đúng đơn và biên lai theo mã | Kết quả tìm kiếm và chi tiết đơn | Chưa thực hiện | |
| TC-POS-08 | Tiền kỳ vọng, thực đếm và chênh lệch đúng | Tổng kết phiên, tiền đầu/cuối và màn đóng ca | Chưa thực hiện | |
| TC-POS-09 | Bán 3 đơn vị SKU quản lý tồn; tồn giảm 3 nếu không có biến động khác | Tồn trước/sau cùng vị trí, dòng đơn và phiếu xuất hoàn tất | Chưa thực hiện | |
| TC-POS-10 | Số đơn duy nhất và doanh thu khớp Pivot cùng phạm vi | Bộ lọc, danh sách đơn gốc và Pivot | Chưa thực hiện | |
| TC-POS-11 | Tổng số lượng từng SKU khớp Pivot cùng quy ước hoàn | Dòng đơn và Pivot theo sản phẩm với bộ lọc | Chưa thực hiện | |
| TC-POS-12 | Quản lý cấu hình được; thu ngân bán được nhưng bị chặn sửa cấu hình | Quyền quản lý, thông báo bị chặn, màn bán của thu ngân | Chưa thực hiện | |

Mẫu từng lần chạy: ID: __; ngày/giờ/người chạy: __; DB/quầy: __; mã phiên: __; mã đơn: __; đầu ca: __; cuối ca thực đếm: __; phương thức: __; kết quả thực tế: __; trạng thái: Chưa thực hiện; ảnh/link: __; ghi chú/N/A: __.

TC-09 cần bán 3 đơn vị cùng SKU, có thể trong một đơn; không nhầm với 30 đơn mẫu. TC-10 đếm mã đơn duy nhất, không đếm dòng sản phẩm.

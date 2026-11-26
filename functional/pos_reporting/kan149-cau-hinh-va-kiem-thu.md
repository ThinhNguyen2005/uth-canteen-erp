# KAN-149 — Cấu hình quầy POS và kiểm thử

Trạng thái: **chưa cấu hình hoặc chạy trên Odoo**. Phụ thuộc KAN-148 và môi trường thử do TV1 bàn giao. Tham khảo `setup.md`, `payment-config.md` và `test-cases.md` cùng thư mục; chỉ cấu hình trong database thử đã xác định, dùng dữ liệu và thanh toán giả lập.

## Điều kiện trước khi chạy

- Ghi phiên bản Odoo, URL và tên database thử, công ty, quầy và quyền tài khoản; không ghi mật khẩu hoặc dữ liệu khách thật.
- TV1 xác nhận phạm vi cấu hình, cấp tài khoản thu ngân và quản lý thử, quyền tạo phiên và phương thức thanh toán. Không thay đổi công ty hoặc cấu hình dùng chung khi chưa xác định ảnh hưởng.
- Xác nhận thiết kế ca KAN-148, danh mục TV2 và thuế/giá được duyệt. Kiểm tra quầy, nhóm quyền và phương thức hiện có trước khi tạo mới.

## Cấu hình và ca nghiệm thu

| ID | Thao tác | Kết quả cần đối chiếu | Trạng thái |
| --- | --- | --- | --- |
| CF-01 | Kiểm tra ứng dụng POS, công ty, quầy thử và quyền thu ngân/quản lý | Đúng database, công ty, quầy; quyền phù hợp phạm vi được duyệt | Chưa chạy |
| CF-02 | Kiểm tra phương thức tiền mặt và chuyển khoản mô phỏng trên quầy | Hai phương thức đúng cấu hình thử; không kết nối hoặc ghi nhận giao dịch ngân hàng thật | Chưa chạy |
| CF-03 | Thu ngân mở phiên, nhập tiền đầu ca, tạo đơn và thanh toán tiền mặt | Phiên mở, đơn và biên lai ghi đúng quầy, sản phẩm, giá và số tiền | Chưa chạy |
| CF-04 | Tạo đơn thử, thanh toán bằng phương thức mô phỏng | Đơn ghi đúng phương thức; lưu tham chiếu giả lập và kết quả xác minh thủ công | Chưa chạy |
| CF-05 | Đếm tiền, đối chiếu và đóng phiên | Tiền dự kiến, tiền đếm, chênh lệch và trạng thái phiên khớp kết quả thực tế | Chưa chạy |
| CF-06 | Kiểm tra quyền thay đổi cấu hình bằng tài khoản thu ngân và quản lý | Đối chiếu với ma trận quyền được duyệt; ghi thông báo và kết quả | Chưa chạy |

Mỗi ca ghi thời gian, người chạy, cấu hình/phiên bản, mã phiên/đơn, bước, giá trị kỳ vọng, giá trị thực tế và ảnh hoặc log; đánh dấu Pass chỉ khi đã đối chiếu. Không ghi thông tin đăng nhập vào bằng chứng. Đính kèm kết quả và review vào issue trước Done.

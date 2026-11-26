# KAN-151 và KAN-152 — Kết quả chuẩn bị môi trường

- PostgreSQL 18.4 tại `127.0.0.1:5434`: kết nối thành công bằng tài khoản đã cấu hình cục bộ; không ghi thông tin xác thực vào báo cáo.
- Đã tạo database thử riêng `uth_kan151_152_test_20261126`. Truy vấn chỉ đọc xác nhận database tồn tại và chưa có bảng trong schema `public` tại thời điểm kiểm tra.
- Chưa khởi tạo module Odoo, cấu hình POS, tạo đơn hoặc cấu hình ưu đãi. Không có ca chức năng nào được xác nhận Pass; chưa có lỗi chức năng được xác minh để sửa hoặc chạy regression.
- Cần khởi tạo Odoo và các module trên database thử, sau đó thực hiện các ca và lưu bằng chứng theo KAN-151/KAN-152. Việc chạy Odoo cần được đánh giá về thao tác xóa tệp tự động theo quy tắc không xóa tệp của workspace.

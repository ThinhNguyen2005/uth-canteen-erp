# Thiết lập POS trên database thử

1. Xác nhận với TV1 URL, DB thử, quyền sửa cấu hình và quyền tạo tài khoản thu ngân/quản lý. Cấu hình kết nối bằng `ODOO_URL`, `ODOO_DB`, `ODOO_USER`, `ODOO_PASSWORD` trong môi trường local. Không đưa mật khẩu vào evidence.
2. Kiểm tra Apps, công ty, tiền tệ VND, quầy và phiên hiện có. Nếu phải cài app, đổi tiền tệ công ty hoặc cấu hình dùng chung, thống nhất với TV1 trước.
3. Trong Point of Sale, tìm quầy `UTH Canteen - Main Counter`, tạo nếu chưa có. Đối chiếu công ty và loại hoạt động kho/vị trí nguồn với TV2 trước khi gán.
4. Kiểm tra và tái sử dụng nhóm POS Cơm, Bún/Phở, Đồ uống, Ăn vặt. Với từng SKU TV2 xác nhận, bật bán trên POS và gán nhóm. Đọc giá, thuế và thiết lập tồn để ghi vào CSV. Nếu giá hoặc tồn sai, chuyển TV2 kiểm tra.
5. Cấu hình [hai phương thức thanh toán](payment-config.md) và gắn riêng cho quầy thử.
6. Tạo hoặc tái sử dụng tài khoản thử riêng cho Thu ngân và Quản lý POS. Kiểm tra nhóm quyền thực tế trên DB rồi chạy TC-POS-12 bằng hai phiên đăng nhập riêng.
7. Chạy một ca thử ngắn. Nếu kết quả phù hợp, thực hiện tối thiểu 30 đơn qua POS, dùng cả hai phương thức, nhiều SKU và đơn nhiều dòng. Ghi nhận mã phiên, mã đơn, tiền đầu/cuối ca, tồn trước/sau và bằng chứng.
8. Đóng phiên, đối chiếu [báo cáo](reporting-analysis.md) và cập nhật [kết quả](test-results.md).

Tên menu có thể khác theo ngôn ngữ và quyền. Các bước cần xác nhận trên DB đích trước khi dùng để nghiệm thu.

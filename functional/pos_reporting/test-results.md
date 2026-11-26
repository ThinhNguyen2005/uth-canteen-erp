# Kết quả kiểm thử POS

## KAN-151/152 — Odoo Native, 26/11/2026

**Cập nhật:** Sau kiểm thử KAN-148, phiên 1 và phiên 2 đã đóng; các đơn thanh toán tương ứng chuyển từ `paid` sang `done`. Hai phiên dùng tiền tệ **USD** của công ty thử mặc định; các giá trị số bên dưới không phải VND.

- Database thử `uth_kan151_152_test_20261126`, Odoo Community 20.0; module `point_of_sale` và `canteen_management` đã cài. HTTP `/web/login` trả 200; phiên đăng nhập HTTP xác nhận đúng database. [Ảnh trang đăng nhập](kan151-152-login-20261126.png) chỉ chứng minh giao diện hiển thị.
- KAN-151: tạo và thanh toán 30 đơn dữ liệu giả qua ORM Odoo, phiên 1, ID 1–30; 22 tiền mặt và 8 chuyển khoản mô phỏng. Tổng đơn và thanh toán đều 1.425.000 theo truy vấn PostgreSQL. [CSV kết quả](kan151-don-thuc-te-20261126.csv). Đây là kiểm thử backend, không phải thao tác trên giao diện POS.
- KAN-152: tạo bảng giá thử 10% cho sản phẩm A khi số lượng từ 2; giá A số lượng 1 = 20.000, A số lượng 2 = 18.000, B số lượng 2 = 35.000 theo API bảng giá. Đơn ORM ID 31, phiên 2, chọn bảng giá thử, số lượng 2, thanh toán giả lập 36.000 và trạng thái `paid`. Đây là quy tắc giả lập, chưa xác minh quyền sinh viên hoặc thanh toán trên giao diện.
- Regression chỉ đọc qua ORM kiểm tra số đơn, trạng thái `paid`, tổng, số thanh toán theo phương thức và ba giá trên: thành công.
- Ca biên ORM: đơn nháp ID 32 được sửa số lượng từ 1 thành 2 (tổng 40.000), sau đó chuyển `cancel` và không có thanh toán. Chưa kiểm thử hoàn tiền.
- Chưa thực hiện: bán hàng qua UI, hoàn tiền, đối chiếu tồn, đóng ca, quy tắc ưu đãi sinh viên được phê duyệt và ảnh các ca POS. Chưa đề nghị Done.
- Lỗi thiết lập thử đã sửa trong script: thiếu trường loại phương thức thanh toán và không thể mở ca bằng Odoo superuser; chạy lại với loại `cash`/`bank` và người dùng quản trị Odoo thành công.

Chưa có lượt chạy trên DB đích. Điền ngày, kết quả và link ảnh thật sau từng lượt. Với Fail, ghi kết quả thực tế, nguyên nhân nghi ngờ và cách kiểm tra lại.

| ID | Kết quả | Ngày chạy | Ghi chú | Bằng chứng |
| --- | --- | --- | --- | --- |
| TC-POS-01 | Chưa thực hiện | — | — | — |
| TC-POS-02 | Chưa thực hiện | — | — | — |
| TC-POS-03 | Chưa thực hiện | — | — | — |
| TC-POS-04 | Chưa thực hiện | — | — | — |
| TC-POS-05 | Chưa thực hiện | — | — | — |
| TC-POS-06 | Chưa thực hiện | — | — | — |
| TC-POS-07 | Chưa thực hiện | — | — | — |
| TC-POS-08 | Chưa thực hiện | — | — | — |
| TC-POS-09 | Chưa thực hiện | — | — | — |
| TC-POS-10 | Chưa thực hiện | — | — | — |
| TC-POS-11 | Chưa thực hiện | — | — | — |
| TC-POS-12 | Chưa thực hiện | — | — | — |

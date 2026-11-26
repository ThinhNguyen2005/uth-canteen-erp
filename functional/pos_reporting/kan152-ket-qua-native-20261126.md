# KAN-152 — Kết quả Odoo Native 26/11/2026

- Database thử `uth_kan151_152_test_20261126`, Odoo 20, module `point_of_sale` và `canteen_management` đã cài.
- Bảng giá giả lập `KAN152 Student Test`: giảm 10% đối với sản phẩm thử A từ số lượng 2. API giá trả A/1 = 20.000, A/2 = 18.000, B/2 = 35.000. Đây là chính sách thử tự tạo, chưa phải chính sách sinh viên được phê duyệt.
- Tạo quầy riêng và đơn POS qua ORM: ID 31, phiên 2, hai đơn vị A giá 18.000, tổng và thanh toán chuyển khoản mô phỏng 36.000, trạng thái `paid`. Không có thanh toán thật. Script: `kan152-native-pos-sale.py`.
- Regression qua ORM sau khi tạo đơn xác nhận tổng, trạng thái, bảng giá và dòng đơn; đồng thời xác nhận 30 đơn của phiên 1 và tổng thanh toán.
- Còn thiếu: xác minh điều kiện là sinh viên, chính sách được duyệt, kiểm thử qua giao diện POS, điều kiện thời gian/cộng dồn, thuế và bằng chứng giao diện cho các ca. Không đánh dấu Done.

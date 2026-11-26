# KAN-148 — Kết quả kiểm thử ca Odoo Native

Ngày 26/11/2026, database thử `uth_kan151_152_test_20261126`, Odoo Community 20.0:

- Phiên 2 có một đơn thanh toán mô phỏng 36.000 và một đơn hủy: đóng qua ORM thành công, đơn thanh toán chuyển `done`, đơn hủy giữ `cancel`; lần đóng lại bị chặn.
- Phiên 1 có 30 đơn thử: đóng qua ORM với tiền mặt đối chiếu 1.145.000 và chuyển khoản mô phỏng 380.000; 30 đơn chuyển `done`.
- Ba phiên thử 3–5 dùng tiền mở ca giả lập 100.000, tiền đếm 99.000, 101.000 và 90.000. Cả ba đóng; các dòng điều chỉnh tương ứng −1.000, +1.000 và −10.000 được ghi trong sổ thử. Sổ còn có dòng điều chỉnh mở ca riêng do số dư phiên trước; không nhầm dòng đó với chênh lệch cuối ca.
- `kan148-native-regression.py` chạy thành công: kiểm tra năm phiên đóng, 30 đơn hoàn tất và ba dòng điều chỉnh.
- Phiên 6: hệ thống chặn đóng khi còn đơn nháp; sau khi hủy đơn nháp, phiên đóng thành công và đơn hoàn tiền mặt giả lập −40.000 chuyển `done`.
- Phiên 7 VND: đơn thử ID 36 chưa thanh toán bị chặn khi yêu cầu chuyển `paid`, sau đó được hủy. Regression kiểm tra lại các phiên và đơn này thành công.

Các phiên dùng **USD** của công ty thử mặc định; đây là số liệu giả lập, không phải VND hoặc giao dịch thật. Chưa kiểm thử giao diện, quyền thu ngân/quản lý, lỗi giao dịch chưa xác minh, hay đối chiếu tài khoản theo chính sách TV1. Cần review và bổ sung bằng chứng trước Done.

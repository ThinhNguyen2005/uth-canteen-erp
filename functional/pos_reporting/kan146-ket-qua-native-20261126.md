# KAN-146 — Kết quả kiểm thử Odoo Native

Ngày 26/11/2026, database thử `uth_kan151_152_test_20261126`, Odoo Community 20.0. `kan146-native-five-cases.py` chạy thành công và đối chiếu năm đơn ORM đã hoàn tất: một loại hàng và nhiều loại hàng với tiền mặt hoặc chuyển khoản mô phỏng, cùng một đơn giá ưu đãi mô phỏng. Kiểm tra số dòng, phương thức, tổng, thanh toán và phiên đã đóng. Đơn nháp ID 32 giữ trạng thái hủy, không có thanh toán.

Đã thử hoàn tiền mặt giả lập cho đơn gốc ID 9: đơn hoàn ID 33 có tổng và thanh toán −40.000, sau khi đóng phiên 6 chuyển `done`. Regression `kan146-native-five-cases.py` kiểm tra lại các đơn gốc, đơn hủy và đơn hoàn thành công.

Các phiên thử trên dùng **USD** của công ty mặc định và giá giả lập; không diễn giải các giá trị này là VND hoặc chính sách đã duyệt. Đây là kiểm thử ORM, chưa chứng minh thao tác, biên lai/in hóa đơn, phân quyền, hoàn tiền hoặc tồn kho trên giao diện. TV1 cần review sơ đồ, vai trò và năm kịch bản theo yêu cầu Jira; chưa đủ căn cứ Done.

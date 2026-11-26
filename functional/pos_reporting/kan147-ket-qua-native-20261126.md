# KAN-147 — Kết quả đối chiếu Odoo Native

Ngày 26/11/2026, đã dùng snapshot bảng giá tham khảo trong `kan147-bang-gia-tham-khao.csv` để tạo 20 sản phẩm thử trong công ty thử riêng `KAN147 Test VND` trên database `uth_kan151_152_test_20261126`. Script `kan147-native-regression.py` kiểm tra lại qua ORM: 20 SKU duy nhất trong công ty thử, tên, đơn vị nguồn, cờ bán POS và giá số khớp CSV; tiền tệ công ty thử là VND. Không nhập dữ liệu vào catalog TV2 hoặc database thật.

Đã mở quầy thử VND và tạo đơn qua ORM cho SKU `UTH-RICE-01`: ID 35, số lượng 1, tổng và thanh toán tiền mặt giả lập 35.000 VND, trạng thái `paid`. Regression đã kiểm tra lại 20 SKU và đơn thử.

Kết quả này không chứng minh SKU/external ID trên database dùng chung, tồn kho, thuế, hiển thị POS hoặc giá đã được chấp thuận. Không tạo hay xác nhận external ID từ snapshot. Cần TV2 đối chiếu catalog thực tế, người có thẩm quyền duyệt giá/thuế, và chạy kiểm thử giao diện POS trước Done. Dữ liệu ưu đãi và chính sách vẫn là giả lập.

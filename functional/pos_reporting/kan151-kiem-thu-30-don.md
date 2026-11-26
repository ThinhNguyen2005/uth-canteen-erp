# KAN-151 — Kế hoạch kiểm thử 30 giao dịch

Trạng thái: **chưa thực hiện**. `kan151-ke-hoach-30-don.csv` chỉ là 30 dòng kế hoạch với mã nội bộ, không phải ID đơn hoặc bằng chứng giao dịch. KAN-149 và KAN-150 vẫn In Progress; cần môi trường và catalog thử được xác nhận trước khi chạy.

1. Ghi phiên bản Odoo, DB/quầy, phiên, thời gian, người chạy, danh sách SKU/giá/thuế/đơn vị và cấu hình kho được duyệt. Chỉ dùng dữ liệu thử và thanh toán giả lập.
2. Thực hiện tối thiểu 30 đơn được lưu thực tế, đa dạng một/nhiều món, số lượng, thời điểm và phương thức. Ghi các ca hủy/sửa riêng cùng trạng thái và chính sách tính vào tổng được xác nhận; không mặc định đơn hủy được tính là giao dịch hoàn tất.
3. Với mỗi đơn, ghi ID thực tế, các dòng SKU, số lượng, giá, thuế/giảm giá, tổng kỳ vọng và thực tế, phương thức, trạng thái và bằng chứng. Bảng kế hoạch cần bổ sung chi tiết từng dòng nếu một đơn có nhiều món.
4. Đối chiếu số ID duy nhất, tổng từng dòng và tổng đơn với giá, thuế, làm tròn, hoàn/hủy theo chính sách được duyệt; đối chiếu tổng theo phương thức và tổng báo cáo cùng phạm vi. Ghi mọi chênh lệch và ảnh/log.
5. Chỉ ghi Pass sau khi kiểm tra dữ liệu thực tế và review; không dùng mã kế hoạch làm ID Odoo. Không có giao dịch thật hoặc dữ liệu khách thật.

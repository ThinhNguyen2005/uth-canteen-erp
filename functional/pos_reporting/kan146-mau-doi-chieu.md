# KAN-146 — Mẫu đối chiếu giao dịch và Pivot

Trạng thái: **Chưa thực hiện**. Ghi DB/quầy: __; phiên: __; thời gian từ/đến và múi giờ: __; người chạy/ngày: __; trạng thái đơn: __; tiền tệ: __; quy ước thuế, giảm giá, làm tròn: __; cách tính hoàn/hủy: __; bộ lọc Pivot: __; link nguồn/ảnh: __.

1. Lấy danh sách giao dịch gốc cùng phạm vi, thời điểm chốt: mã đơn duy nhất, trạng thái, tổng, phương thức, SKU và số lượng từng dòng. Không tính đơn nháp/hủy chưa thanh toán vào doanh thu. Ghi riêng hoàn tiền và thống nhất chỉ tiêu gộp hoặc thuần trên cả hai nguồn.
2. Mở Pivot Orders và áp dụng cùng quầy, phiên, thời gian, trạng thái và quy ước. Xác nhận chỉ tiêu doanh thu gồm hay không gồm thuế và cách làm tròn. Chỉ đếm đơn duy nhất nếu Pivot hỗ trợ đúng cấp dữ liệu; không suy số đơn từ số dòng sản phẩm.
3. Tổng hợp số lượng dòng đơn theo SKU, trừ hoàn nếu dùng quy ước thuần; so với Pivot theo cùng SKU và quy ước. Ghi rõ nếu Pivot không hỗ trợ chỉ tiêu hoặc không hiển thị SKU.
4. Chênh lệch = Pivot − nguồn. Kiểm tra bộ lọc, đồng bộ, thuế, hoàn và làm tròn; lưu ảnh bộ lọc, giao dịch gốc, Pivot và chi tiết chênh lệch. Không kết luận Pass khi chưa có bằng chứng.

| Chỉ tiêu | Nguồn gốc | Pivot | Chênh lệch | Bằng chứng/giải thích | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| Số mã đơn duy nhất | | | | | Chưa thực hiện |
| Doanh thu theo quy ước đã ghi | | | | | Chưa thực hiện |
| Số lượng SKU: __ | | | | | Chưa thực hiện |
| Số lượng SKU: __ | | | | | Chưa thực hiện |

Đối chiếu tiền mặt riêng: đầu ca + tiền mặt khách đưa − tiền thừa − hoàn tiền mặt + thu thêm − chi ra = tiền dự kiến. Hoặc dùng tiền bán ròng và không trừ tiền thừa/hoàn hai lần. Thực đếm − dự kiến = chênh lệch. Chuyển khoản mô phỏng không cộng vào két. Đầu ca: __; thu ròng: __; thu thêm: __; chi: __; dự kiến: __; thực đếm: __; lệch: __; ảnh: __. Liệt kê riêng giao dịch ngoài 30 đơn hoặc biến động kho khác trước khi đối chiếu.

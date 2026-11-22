# Đối chiếu báo cáo POS

Chưa có số liệu đo trên DB đích. Mỗi lượt ghi quầy, mã phiên, ngày theo giờ Việt Nam, phạm vi trạng thái và cách xử lý hoàn tiền.

1. Mở **Point of Sale → Reporting → Orders**, chọn Pivot hoặc Graph. Lọc quầy, phiên, ngày và phạm vi đơn giống nhau khi trích nguồn.
2. So sánh số đơn theo mã đơn duy nhất và tổng doanh thu với danh sách đơn gốc. Kiểm tra chỉ tiêu có gồm thuế hay không trước khi so. Báo cáo theo sản phẩm đối chiếu với tổng số lượng trên dòng đơn, cùng quy ước dấu của hoàn hàng.
3. Đối soát két bằng tiền đầu ca + tiền bán ròng bằng tiền mặt + tiền thu thêm − tiền chi ra. Ghi số đếm và chênh lệch. Tiền mô phỏng đối chiếu riêng từ danh sách thanh toán.
4. Kiểm tra SKU, vị trí xuất, phiếu xuất đã hoàn tất và tồn trước/sau. Ghi riêng biến động ngoài ca nếu có.

| Chỉ tiêu | Nguồn đối chiếu | Giá trị nguồn | Giá trị báo cáo | Chênh lệch / bằng chứng |
| --- | --- | --- | --- | --- |
| Số đơn và doanh thu theo phiên/ngày | Danh sách đơn | — | — | — |
| Lượng bán từng SKU | Dòng đơn | — | — | — |
| Tiền cuối ca | Sổ tiền mặt và số đếm | — | — | — |
| Tồn sau bán | Tồn và dịch chuyển tại vị trí nguồn | — | — | — |

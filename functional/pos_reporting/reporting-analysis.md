# Đối chiếu báo cáo POS

## Đối chiếu backend — 26/11/2026

**Cập nhật:** Phiên 1 sau đó đã đóng và 30 đơn chuyển sang `done`. Công ty thử dùng USD; tổng số dưới đây không phải doanh thu VND.

Trên database thử `uth_kan151_152_test_20261126`, phiên 1 có 30 đơn `paid` được tạo qua ORM; tổng `amount_total` = `amount_paid` = 1.425.000. Bảng thanh toán có 22 khoản tiền mặt tổng 1.045.000 và 8 khoản chuyển khoản mô phỏng tổng 380.000; cộng lại bằng 1.425.000. Chi tiết: [CSV từ PostgreSQL](kan151-don-thuc-te-20261126.csv). Số liệu dùng sản phẩm giả lập, thuế bằng 0 và tiền tệ của công ty thử; không phải doanh thu kinh doanh thực.

Chưa đối chiếu Pivot/Graph trên giao diện, tồn kho hoặc tiền đếm cuối ca; bảng bên dưới vẫn ghi trạng thái chưa thực hiện đối với các ca trên DB đích.

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

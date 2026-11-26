# KAN-152 — Khảo sát ưu đãi POS

Trạng thái: **chưa cấu hình và chưa kiểm thử trên Odoo**. Phụ thuộc KAN-147 và KAN-149. Chính sách ưu đãi sinh viên, đối tượng, thời hạn, cách xác minh, cộng dồn, thuế và làm tròn cần người phụ trách xác nhận trước khi áp dụng.

## Bằng chứng đọc mã

Bản Odoo cục bộ revision `fa2c1d6e67fff519d450f43271717ab1c93dac9b`, `addons/point_of_sale/models/pos_config.py`, có các trường `use_pricelist`, `pricelist_id`, `available_pricelist_ids`, `manual_discount` và `module_pos_discount`. Ràng buộc trong cùng tệp yêu cầu bảng giá mặc định được liệt kê trong danh sách áp dụng khi bật pricelist, cùng tiền tệ và công ty phù hợp. Đây là kết quả đọc mã một revision, không xác nhận tính năng đã cài, cấu hình hay hoạt động trên database thử.

## Kiểm thử sau khi có môi trường và chính sách

| ID | Tình huống | Kỳ vọng cần đối chiếu | Trạng thái |
| --- | --- | --- | --- |
| UD-01 | Kiểm tra phiên bản, tính năng pricelist/discount và quyền cấu hình tại quầy thử | Ghi tính năng khả dụng, cấu hình hiện tại và bằng chứng | Chưa chạy |
| UD-02 | Khách đủ điều kiện, sản phẩm và thời điểm thuộc phạm vi | Giá và tổng khớp chính sách, thuế và làm tròn đã duyệt | Chưa chạy |
| UD-03 | Khách, sản phẩm hoặc thời điểm không đủ điều kiện | Không áp dụng ưu đãi ngoài phạm vi đã duyệt | Chưa chạy |
| UD-04 | Kết hợp ưu đãi khác hoặc đổi số lượng | Kết quả đúng quy tắc cộng dồn và ngưỡng được duyệt | Chưa chạy |
| UD-05 | Thanh toán giả lập, kiểm tra đơn và biên lai | Giá, giảm giá, tổng và phương thức khớp cấu hình và phép tính độc lập | Chưa chạy |

Ghi phiên bản, quầy, cấu hình, tài khoản thử không có mật khẩu, SKU, giá niêm yết, điều kiện, phép tính kỳ vọng, kết quả thực tế và ảnh/log. Nếu tính năng không hoạt động, ghi cách tái hiện, bằng chứng và phương án xử lý để người phụ trách thống nhất; không kết luận bản Community không hỗ trợ chỉ từ việc đọc mã.

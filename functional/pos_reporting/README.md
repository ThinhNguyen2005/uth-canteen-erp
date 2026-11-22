# POS & Reporting — TV3

Dùng POS chuẩn của Odoo Community 20 cho quầy **UTH Canteen - Main Counter**. Các tài liệu trong thư mục mô tả cách cấu hình và kiểm thử. Kết quả quan sát thực tế ghi trong [test-results.md](test-results.md).

| Việc | Thời điểm thực hiện |
| --- | --- |
| Quy trình, thanh toán mô phỏng, 12 kịch bản và mẫu đối chiếu | Làm song song với TV1, TV2, TV4 và TV5. |
| Kiểm kê cấu hình, viết và xác minh script cấu hình, tạo quầy và user | Chờ môi trường truy cập được, DB thử và quyền do TV1 xác nhận. |
| Ánh xạ danh mục, bán 30 đơn, kiểm tra tồn và báo cáo | Chờ sản phẩm, giá, kho, SKU có tồn do TV2 bàn giao trên DB thử. |
| Kiểm thử thanh toán đơn đặt | Chờ mã đặt và luồng tra cứu/giao món từ TV4/TV5. Có thể thực hiện sau luồng POS tại quầy. |
| Giá sinh viên và dashboard riêng | Xem xét sau kiểm thử bắt buộc. MVP dùng Pivot/Graph chuẩn. |

[Thiết lập](setup.md) · [Quy trình](business-process.md) · [Thanh toán](payment-config.md) · [Test case](test-cases.md) · [Báo cáo](reporting-analysis.md)

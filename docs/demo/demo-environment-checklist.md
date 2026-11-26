# Database và checklist dry run — ERP-58

Dùng database demo riêng trong project uth-canteen-erp. Ghi revision, image, timezone và tên database vào phiếu chạy. Cài addon theo hướng dẫn repository sau khi dependency được merge. Chuẩn bị sản phẩm, nhà cung cấp, kho/receipt, POS config/phương thức thanh toán, ca còn chỗ và ca đầy, hai người đặt và một phiếu confirmed. Dùng dữ liệu giả lập và giữ credential ngoài tài liệu.

| Giai đoạn | Tài khoản chuẩn bị | Kiểm tra trước khi quay |
|---|---|---|
| Purchase → Inventory | Purchaser và người nhận hàng | PO có product và supplier, receipt xác nhận được, tồn kho đối chiếu được |
| POS | Cashier POS | Phiên mở được, sản phẩm bán được, có phương thức thanh toán thử |
| Slot → Booking | Manager, Booking User, Cashier | Ca draft/open/full, phiếu đúng giờ, role theo ma trận duyệt |
| Security → Reporting | Tài khoản giới hạn và người xem báo cáo | Dùng fixture khác owner, báo cáo thuộc revision đã tích hợp |

Dry run theo demo-plan.md. Ghi thời lượng, actual và link ảnh theo từng bước. Nếu một bước bị lỗi, giữ bằng chứng, dùng fixture dự phòng rồi ghi rõ bước nào được bỏ hoặc chạy lại. Giữ Pending Demo khi chưa chạy. Chỉ quay khi kịch bản đã kiểm tra; ẩn thông tin tài khoản, thông báo và dữ liệu cá nhân. Chỉ ghi link video, feedback và acceptance khi thực sự có.

# ERP-58 — Demo và bàn giao

PENDING DEMO. Dependency ERP-12/23/34/46 và ERP-54–57 cần xác nhận trên cùng revision. Dùng DB demo riêng, dữ liệu giả lập, tài khoản theo role. Chuẩn bị nhà cung cấp, sản phẩm, PO, tồn kho, cấu hình POS, slot, booking và báo cáo. Không dùng dữ liệu thật. Kiểm tra lại log cài addon và sign-off UAT trước dry run.

| Bước | Module / người trình bày dự kiến | Vai trò | Thao tác và expected | Recovery |
|---|---|---|---|---|
| 1 | Intro / điều phối | Presenter | Giới thiệu phạm vi và đăng nhập | Chuẩn bị link localhost và phiên test |
| 2–5 | Purchase/Inventory / TV2 | Purchaser | Tạo, confirm PO, nhận hàng, xem tồn | Dùng PO fixture riêng |
| 6–9 | POS / TV3 | Cashier | Mở POS, tạo đơn, thanh toán và đối chiếu | Phiên POS test dự phòng |
| 10–13 | Slot / TV5 | Manager | Tạo ca, capacity và Open | Slot draft test dự phòng |
| 14–19 | Booking / TV5 | Theo ma trận | Create, confirm theo workflow đã duyệt, xem booked_count, serve, xem Served, hủy phiếu khác | Fixture từng state |
| 20–24 | Capacity/Security / TV5 | Manager và Booking User | Hoàn capacity, full, validation, phân quyền, đóng ca | Tài khoản role riêng |
| 25–26 | Reporting / TV1 | Presenter | Báo cáo và tổng kết theo kết quả đã kiểm tra | Bỏ bước chưa được xác minh và ghi known issue |

Actual và duration từng bước: chưa chạy. Phân công trên là đề xuất, chờ nhóm xác nhận. Không khẳng định đồng bộ tự động.

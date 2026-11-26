# ERP-57 — Kế hoạch UAT

PENDING UAT và PENDING SIGN-OFF. Môi trường dự kiến Compose uth-canteen-erp, DB UAT riêng với dữ liệu mẫu. Ghi SHA đã tích hợp và phiên bản khi bàn giao cho người tham gia. Điều kiện vào: addon cài/nâng cấp được, đủ tài khoản vai trò, UI/ACL đã tích hợp, test ERP-55/56 đạt. Điều kiện ra: người nghiệp vụ chạy checklist, ghi expected/actual và quyết định; blocker/critical được xử lý trước demo.

Manager tạo ca hợp lệ, cấu hình capacity, mở ca, kiểm tra booking rồi đóng ca. Cashier tìm booking, giao suất và đối chiếu trạng thái. Booking User đăng nhập theo cơ chế đã duyệt, xem ca, tạo và xem phiếu cá nhân, hủy đúng hạn, kiểm tra cảnh báo đầy. Chỉ đưa Purchase/Inventory/POS/Reporting vào UAT sau khi có evidence liên kết thực tế. Người nghiệm thu, thời gian và phản hồi chờ xác nhận.

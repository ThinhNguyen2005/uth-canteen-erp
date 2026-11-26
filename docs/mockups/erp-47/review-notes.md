# Review notes — ERP-47

## Workflow đề xuất, chưa phê duyệt

1. Tạo booking: chọn ca và số suất; kiểm tra quyền, ca mở và capacity. Baseline SRS tạo confirmed trực tiếp; KAN-159 đề xuất draft. Cần chốt.
2. Confirm: draft → confirmed khi ca open và đủ chỗ; backend phải khóa slot và kiểm tra lại.
3. Cancel: draft hoặc confirmed → cancelled; confirmed yêu cầu đúng owner và trước hạn 30 phút theo SRS, giải phóng capacity. Quyền ngoại lệ chờ xác nhận.
4. Serve: cashier check-in confirmed → served trong giờ ca; served vẫn chiếm capacity. Cần xác nhận action và phản hồi khi gọi lại.
5. Lỗi validation, hết suất hoặc thiếu quyền: giữ dữ liệu, hiển thị thông báo; enforcement phía server.

| Nút | State đề xuất | Role đề xuất | Trạng thái |
|---|---|---|---|
| Confirm | draft | Manager; quyền người đặt chưa chốt | Pending Review |
| Cancel | draft/confirmed | Owner trong hạn; ngoại lệ chưa chốt | Pending Review |
| Serve | confirmed | Cashier | Pending Review |

## Câu hỏi TV4 / TV1

- Booking user internal hay portal? Ownership có dựa vào partner_id không?
- Confirm trực tiếp khi tạo hay draft? Ai xác nhận/hủy ngoại lệ?
- Duplicate áp dụng draft và confirmed hay chỉ confirmed? Đặt lại sau served?
- Hủy/serve lặp trả trạng thái hay từ chối? Có served_at không?
- Khi nào slot được mở lại? Cron no-show và quyền direct state write được bảo vệ thế nào?
- Xác nhận tên fields/actions, XML IDs, timezone và quyền truy cập theo role.

TV1 review docs và phối hợp manifest cho các task sau. Đây chỉ là mockup tĩnh; không xác nhận thiết kế hoặc quyền đã duyệt.

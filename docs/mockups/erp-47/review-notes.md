# Review notes — ERP-47

## Workflow theo PR #38 và #40

1. Phiếu thường tạo ở confirmed. Draft nội bộ của Manager không giữ suất.
2. Confirm chuyển draft → confirmed sau kiểm tra ca và capacity. Kiểm thử khóa slot chờ ERP-43.
3. Cancel chuyển draft hoặc confirmed → cancelled. Hủy confirmed hoàn suất.
4. Serve chuyển confirmed → served. Served vẫn chiếm suất.
5. Served và cancelled kết thúc. Action lặp trả UserError. Lỗi validation, hết suất và thiếu quyền được xử lý phía server.

| Nút | State | Role |
|---|---|---|
| Confirm | draft | Manager |
| Cancel | draft | Manager |
| Cancel | confirmed | Manager ngoại lệ hoặc Booking User sở hữu phiếu và còn ít nhất 30 phút trước ca |
| Serve | confirmed | Manager hoặc Cashier |

## Nội dung chờ TV4 và TV1

- Chốt internal/portal, phạm vi quyền ORM và quyền hiển thị khi quyền cộng dồn.
- Chốt cửa sổ giờ phục vụ và no-show với SRS.
- Xác minh timezone và rule chuyển trạng thái slot khi tích hợp.
- TV1 review docs và phối hợp manifest. Mockup minh họa giao diện; kiểm thử quyền nghiệp vụ thực hiện trên addon tích hợp.

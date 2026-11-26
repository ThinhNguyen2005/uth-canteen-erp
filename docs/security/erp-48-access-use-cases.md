# ERP-48 — Allow/Deny use cases (NOT RUN)

Mọi expected dưới đây là PROPOSED/PENDING REVIEW; kiểm thử bằng user thường, xác minh record không thay đổi sau deny.

| ID | Role / hành động | Kỳ vọng dự thảo |
|---|---|---|
| SEC-01 | User đọc booking của mình | Allow trong phạm vi đã duyệt |
| SEC-02 | User đọc booking người khác bằng search và ID | Deny/không trả dữ liệu |
| SEC-03 | User create partner_id của người khác | Deny hoặc server gán chính mình; cần chốt |
| SEC-04 | User đổi owner | Deny |
| SEC-05 | Cashier confirm/cancel khi không được giao | Deny tại server |
| SEC-06 | Manager quản lý slot hợp lệ | Allow theo ACL/guard |
| SEC-07 | User sửa capacity qua ORM/RPC | Deny; capacity không đổi |
| SEC-08 | Role trái quyền gọi confirm/cancel/serve qua RPC | Deny; state/count không đổi |
| SEC-09 | User ghi state trực tiếp | Deny bypass; state không đổi |
| SEC-10 | User sửa quantity/slot sau confirm | Deny theo policy cần duyệt |
| SEC-11 | Không group nhưng có quyền chuẩn khác | Kết quả theo quyền hiệu lực, không giả định chỉ kiểm tra menu |
| SEC-12 | User nhiều group | So sánh hợp ACL, group rules và global rules với ma trận đã chốt |
| SEC-13 | Cashier đọc booking ngoài ca/phạm vi | Deny nếu policy quy định giới hạn; cần chốt |
| SEC-14 | User thay đổi owner qua nested create/write | Deny hoặc ép owner; cần chốt |

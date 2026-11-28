# ERP-48 — Ma trận phân quyền dự thảo

Trạng thái: PENDING REVIEW. Baseline develop 23fd49d chưa có booking/slot models; ERP-47 mockup là bản nháp chưa review. Không có ACL/record rule được duyệt; bảng sau là đề xuất thảo luận, không cấp quyền triển khai.

CONFIRMED từ security XML: group_canteen_kitchen và group_canteen_cashier imply group_canteen_user; group_canteen_manager imply kitchen và cashier. XML baseline chưa cài được trên Odoo 20. Fixture ERP-53 với patch manifest đã kiểm tra được cây nhóm và membership, chưa xác nhận quyền CRUD. Canteen Admin là vai trò nghiệp vụ yêu cầu phân tích, chưa có group riêng được xác nhận; không đồng nhất với superuser. Internal/portal của Booking User: PENDING REVIEW; SRS yêu cầu đăng nhập tài khoản UTH nhưng không xác định loại user Odoo.

| Role × model | Create | Read | Write | Unlink | Phạm vi | Trạng thái |
|---|---|---|---|---|---|---|
| Không có group × cả hai | Deny | Deny | Deny | Deny | Không có | PROPOSED; kiểm tra quyền cộng dồn khác |
| Booking User × Slot | Deny | Allow | Deny | Deny | Ca mở được phép xem | PROPOSED |
| Booking User × Booking | Allow | Allow | Conditional | Deny | Bản ghi của mình | PROPOSED; owner, state và thay đổi field cần guard |
| Cashier × Slot | Deny | Allow | Deny | Deny | Ca cần phục vụ | PROPOSED |
| Cashier × Booking | Deny | Allow | Conditional | Deny | Phiếu cần check-in; phạm vi chưa chốt | PENDING REVIEW |
| Manager × Slot | Allow | Allow | Allow | Deny | Ca nghiệp vụ | PROPOSED |
| Manager × Booking | Conditional | Allow | Conditional | Deny | Ngoại lệ được giao | PENDING REVIEW |
| Canteen Admin × hai model | PENDING | PENDING | PENDING | PENDING | Chưa xác định | PENDING REVIEW |

| Action | Role đề xuất | State/ownership/điều kiện | Trạng thái |
|---|---|---|---|
| Create | Booking User | Owner chính mình; slot open; 1–3; chưa trùng; capacity đủ | PROPOSED |
| Confirm | Manager (draft nội bộ) | draft; khóa slot; capacity đủ | PENDING REVIEW; luồng public xác nhận trực tiếp |
| Cancel | Manager; Booking User chính chủ | Manager xử lý draft/confirmed. Chính chủ chỉ hủy confirmed khi còn ít nhất 30 phút | Action đối chiếu PR #40; ACL PENDING REVIEW |
| Serve | Manager hoặc Cashier | confirmed, ca active và open/full; không phát hai lần | Action đối chiếu PR #40; giới hạn giờ phục vụ PENDING REVIEW |
| No-show | Cron | confirmed; sau end_at +15 phút | SRS yêu cầu; implementation MISSING |
| Sửa quantity/slot/owner | Booking User | Deny sau confirmed. Draft là phiếu nội bộ của Manager | Guard và phạm vi sửa draft PENDING REVIEW |
| Sửa capacity | Manager | Không nhỏ hơn booked_count | PROPOSED |
| Delete booking | Vai trò nghiệp vụ thông thường | Deny; dùng Cancel theo policy | TV4 xác nhận; ACL chờ ERP-42/53 |
| Xem booking người khác | Cashier/Manager | Phạm vi cần phục vụ/ngoại lệ | PENDING REVIEW |

ACL cộng dồn theo mọi group, không thu hồi quyền cấp bởi group khác. Cách kết hợp domain trên ir.access cần được xác minh bằng test tích hợp trước khi áp dụng ma trận. Owner domain candidate [('partner_id', '=', user.partner_id.id)] cần xác minh field và yêu cầu; không áp dụng global rule khiến manager/cashier mất truy cập. Quyền tạo không chứng minh client không giả owner: backend phải gán/kiểm tra partner_id. Bảo vệ action và direct write state/quantity/slot/partner tại server; ẩn nút không thay thế ACL/rule/guards. Kiểm tra user nhiều group và group chuẩn khác; không dùng sudo để né quyền.
## Quyền hiển thị và quyền sửa slot bổ sung

| Vai trò | Menu Bookings | Menu Meal Slots | Open/Close | Capacity / state / archive |
|---|---|---|---|---|
| Manager | Chờ chốt phạm vi | Đề xuất cho phép | Guard trên PR #25; Open draft/active/capacity > 0, Close open/full | Capacity đề xuất cho phép; state chỉ qua action; archive chờ duyệt |
| Cashier | Đề xuất chỉ dữ liệu phục vụ | Chờ duyệt read | Action guard từ chối trong fixture | Đề xuất từ chối |
| Booking User | Own scope, qua portal hay internal chưa chốt | Ca khả dụng qua kênh đã duyệt | Action guard từ chối trong fixture | Đề xuất từ chối |
| Admin nghiệp vụ / không nhóm | Admin chờ chốt; không nhóm đề xuất từ chối | Cùng điều kiện | Không suy ra từ quyền Settings | Chờ duyệt |

ERP-53 cần kiểm tra domain và operation trên ir.access của runtime. Visibility menu và field chỉ là một phần của thiết kế. Backend guard cho create/write state của TV4 còn mở.

## Quy tắc workflow đã đối chiếu PR #40

- Manager confirm draft, cancel draft/confirmed (có ngoại lệ thời hạn) và serve confirmed; Cashier chỉ serve confirmed trong phạm vi action nghiệp vụ.
- Booking User chỉ hủy confirmed của chính mình (partner_id = user.partner_id) khi còn ít nhất 30 phút. Kiểm tra mốc 31/30/29 phút. Không sửa trực tiếp quantity, slot_id, partner_id, state sau confirmed; không unlink.
- Dùng bốn nhóm canteen hiện có, không thêm Canteen Admin. Kitchen read, toàn bộ CRUD, menu và rules còn Pending Review; ERP-42 phải bảo vệ ORM/RPC và owner khi create.

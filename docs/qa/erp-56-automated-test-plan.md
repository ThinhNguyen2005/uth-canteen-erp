# ERP-56 — Kế hoạch automated suite

BLOCKED bởi ERP-43/44, model booking, ACL ERP-53 và ERP-54. Chưa có suite concurrency thực thi. Tách kiểm tra ORM model khỏi HttpCase và test quyền trên user thường. Đăng ký tests qua tests/__init__.py, xác minh discovery và test count từ log Odoo 20 ở revision tích hợp.

| Suite | Cases | Dependency |
|---|---|---|
| Booking | create, confirm, cancel, serve, duplicate, quantity, state, replay, rollback | API booking duyệt |
| Slot | invalid time/capacity, open/close, inactive, full, count, state sync | TV4 fix và tích hợp PR #25 |
| Security | CRUD, ownership, action permissions, user nhiều group | ACL ERP-48/53 |
| Race | 10 suất, đã đặt 9; hai yêu cầu hợp lệ mỗi yêu cầu 1 suất | ERP-43 và API confirm thực tế |

Race dùng fixture đã commit trong DB test riêng, hai connection/cursor và hai ORM environment. Barrier trước khi gọi nghiệp vụ, timeout hữu hạn, mỗi worker commit hoặc rollback và ghi outcome. Đọc lại bằng transaction mới: đúng một yêu cầu đạt, tổng 10, slot full, booking thua không giữ thêm suất, count khớp tổng confirmed/served. Xác minh retry theo contract. Không dùng chung cursor hay mô phỏng tuần tự. Dọn dữ liệu fixture theo run ID sau khi join cả hai workers.

Lưu SHA, phiên bản, DB, thời điểm, command, test count và exit code. Kết quả cũ của model fixture không tính vào suite này.

Đã thêm TransactionCase dành cho Meal Slot và Booking. Chạy với source fixture PR #40 và patch manifest ERP-53. Test role/ownership, concurrency và RPC chờ ERP-42/43/44. Kết quả fixture không áp dụng cho các kiểm tra đang chờ.

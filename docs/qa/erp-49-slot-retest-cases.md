# ERP-49 — Ca kiểm thử slot bổ sung

Cả bảy expected results dưới đây đều PENDING REVIEW (TV4). Các ca dưới đây là thiết kế. Cập nhật actual và evidence khi chạy cùng revision tích hợp trên DB test.

| ID | Requirement / role / priority | Preconditions và dữ liệu | Steps | Expected | Actual / Status / Evidence |
|---|---|---|---|---|---|
| SLOT-44 | ERP-51/53 / Manager / High | Slot draft active, capacity 10, count 0; ACL đã duyệt | Open, reload; Close, reload | open rồi closed, count giữ nguyên | Chưa chạy / NOT RUN / — |
| SLOT-45 | ERP-51/53 / Manager / High | Slot draft inactive hoặc capacity 0 | Thử mở từng mẫu, reload | Từ chối, giữ draft | Tích hợp chưa chạy / NOT RUN / probe system riêng đã ghi trong PR #25 |
| SLOT-46 | ERP-53 / Cashier và Booking User / High | Slot draft/open; hai tài khoản thường theo ACL tích hợp | Kiểm tra quyền gọi action trên từng role | AccessError và state giữ nguyên | Tích hợp chưa chạy / NOT RUN / probe ORM riêng đã ghi trong PR #25 |
| SLOT-47 | ERP-54 / Manager / High | Chính sách state và fix TV4 đã duyệt | Chạy regression cho lưu trạng thái và kiểm tra invariant theo policy | Không lưu state vi phạm capacity; bản ghi hợp lệ vẫn lưu được | Chờ TV4 / BLOCKED / PR25 F01 |
| SLOT-48 | ERP-51 / Manager / Medium | Hai slot ở hai phía mốc ngày theo timezone user | Lọc Start Date và Group by Start Day | Kết quả theo ngày local của user | Chưa chạy / NOT RUN / — |
| SLOT-49 | ERP-51/54 / Manager / High | Slot mở, hai mức capacity hợp lệ và booked_count đã khởi tạo | Cập nhật capacity về mức đầy rồi tăng lên; đọc lại DB sau mỗi lần | full khi hết suất, open khi có suất và policy cho phép; count không bị sửa tay | Chưa chạy / NOT RUN / — |
| SLOT-50 | ERP-51/53 / Manager / High | Nhóm và quyền CRUD đã duyệt; DB riêng | Kiểm tra từng thao tác CRUD và archive với bản ghi riêng; xác minh dữ liệu sau deny | Theo ma trận ERP-48 đã duyệt; deny không đổi dữ liệu | Chờ duyệt / BLOCKED / — |

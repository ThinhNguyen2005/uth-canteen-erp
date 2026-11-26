# ERP-49 — Ca kiểm thử slot bổ sung

Expected của SLOT-47 đã đối chiếu fix PR #25 và chạy với quyền hệ thống. Quyền Manager thường vẫn NOT RUN. Các expected còn lại PENDING REVIEW (TV4). Cập nhật actual và evidence khi chạy cùng revision tích hợp trên DB test.

| ID | Requirement / role / priority | Preconditions và dữ liệu | Steps | Expected | Actual / Status / Evidence |
|---|---|---|---|---|---|
| SLOT-44 | ERP-51/53 / Manager / High | Slot draft active, capacity 10, count 0; ACL đã duyệt | Open, reload; Close, reload | open rồi closed, count giữ nguyên | Chưa chạy / NOT RUN / — |
| SLOT-45 | ERP-51/53 / Manager / High | Slot draft inactive hoặc capacity 0 | Thử mở từng mẫu, reload | Từ chối, giữ draft | Tích hợp chưa chạy / NOT RUN / probe system riêng đã ghi trong PR #25 |
| SLOT-46 | ERP-53 / Cashier và Booking User / High | Slot draft/open; hai tài khoản thường theo ACL tích hợp | Kiểm tra quyền gọi action trên từng role | AccessError và state giữ nguyên | Tích hợp chưa chạy / NOT RUN / probe ORM riêng đã ghi trong PR #25 |
| SLOT-47 | ERP-54 / System và Manager / High | Fixture có fix ed18146. Ca Manager cần ACL tích hợp | Chạy regression cho lưu trạng thái và kiểm tra invariant theo policy | Không lưu state vi phạm capacity; bản ghi hợp lệ vẫn lưu được | System: PASS (fixture) với create/write open + capacity 0, tv5-backend-alignment-install.log. Manager: NOT RUN. |
| SLOT-48 | ERP-51 / Manager / Medium | Hai slot ở hai phía mốc ngày theo timezone user | Lọc Start Date và Group by Start Day | Kết quả theo ngày local của user | Chưa chạy / NOT RUN / — |
| SLOT-49 | ERP-51/54 / Manager / High | Slot mở, hai mức capacity hợp lệ và booked_count đã khởi tạo | Cập nhật capacity về mức đầy rồi tăng lên; đọc lại DB sau mỗi lần | full khi hết suất, open khi có suất và policy cho phép; count không bị sửa tay | Chưa chạy / NOT RUN / — |
| SLOT-50 | ERP-51/53 / Manager / High | Nhóm và quyền CRUD đã duyệt; DB riêng | Kiểm tra từng thao tác CRUD và archive với bản ghi riêng; xác minh dữ liệu sau deny | Theo ma trận ERP-48 đã duyệt; deny không đổi dữ liệu | Chờ duyệt / BLOCKED / — |

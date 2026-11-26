# ERP-49 — Bộ ca kiểm thử dự thảo

Bộ thiết kế gồm 50 ca: [43 ca CSV](erp-49-test-cases.csv) và [7 ca Slot](erp-49-slot-retest-cases.md). Chưa thực thi ca tích hợp nào. Mỗi ca có scenario, role, preconditions, data, steps, expected/actual, evidence và priority. Expected là PENDING REVIEW vì ERP-48 và contract chưa được duyệt. Kiểm thử runtime bị BLOCKED do addon chưa cài và model booking chưa tồn tại trên develop. Đây là thiết kế, không phải kết quả test.

Concurrency: cần ít nhất hai session PostgreSQL/ORM độc lập có transaction riêng; barrier trước thao tác, chờ cả hai kết thúc, kiểm tra invariant bằng transaction thứ ba; worker thất bại tự rollback. Không dùng thao tác tuần tự hay threading.Lock giả lập database. Chi tiết retry/deadlock và expected chính xác chờ ERP-43/TV4.

# Data contract — DỰ THẢO, chưa được TV4/TV5 chấp thuận

| Model dự kiến | Trường dự kiến | Quy tắc đề xuất |
| --- | --- | --- |
| canteen.meal.slot | name, start_at, end_at, capacity | capacity không âm; start trước end |
| canteen.meal.booking | partner_id, slot_id, quantity, state | quantity dương; số xác nhận không vượt capacity |
| res.partner | mở rộng nếu cần | tái sử dụng model chuẩn |

Một slot có nhiều booking, mỗi booking thuộc một slot và partner. Trạng thái dự kiến draft, confirmed, served, cancelled. Cần xác nhận chuyển trạng thái, hoàn chỗ, quyền, unique booking, liên kết POS và thanh toán. Lưu thời gian UTC theo Odoo, hiển thị theo múi giờ người dùng; chốt timezone nghiệp vụ Asia/Ho_Chi_Minh. Capacity cần xử lý đồng thời an toàn trong PostgreSQL khi triển khai. TV1, TV4, TV5 cần review và ghi biên bản trước khi code.

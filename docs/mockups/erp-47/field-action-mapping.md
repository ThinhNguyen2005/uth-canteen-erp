# Field và action mapping

Nguồn: develop aefdeed (Meal Slot) và PR #38/#40 (Booking, đang review).

| Màn hình | Field hoặc action | Trạng thái |
|---|---|---|
| Booking | booking_ref Char; partner_id Many2one; slot_id Many2one; quantity Integer; state Selection; booked_at Datetime; note Char | Có trong source PR #38 |
| Slot | name Char; product_id Many2one; start_at/end_at Datetime; capacity/booked_count Integer; state Selection; active Boolean | Có trên develop |
| Slot | capacity - booked_count | Giá trị thiết kế; không có field remaining |
| Booking | action_confirm_booking, action_cancel_booking, action_mark_booking_served | Có trong source PR #40 |
| Slot | action_open_slot, action_close_slot | Có trên develop |

PR #38 tính booked_count từ tổng quantity confirmed và served. Draft không giữ suất. Partial unique index giới hạn bản ghi confirmed trùng người và ca. Ownership dùng partner_id = user.partner_id. ERP-42/43 vẫn cần xác minh bảo vệ ownership và concurrency. Contract hiện chưa có served_at.

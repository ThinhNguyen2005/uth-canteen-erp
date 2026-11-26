# Field và action mapping — Pending Review

Nguồn: develop 23fd49d, docs/data-contract.md, KAN-158/159; branch TV4 ERP-38 09957db chưa merge. Trên develop booking và slot chưa có model Python.

| Màn hình | Field | Trạng thái |
|---|---|---|
| Booking | booking_ref Char; partner_id Many2one; slot_id Many2one; quantity Integer; state Selection; booked_at Datetime; note Char | Contract; chưa có code develop |
| Slot | name Char; product_id Many2one; start_at/end_at Datetime; capacity/booked_count Integer; state Selection; active Boolean | Có trên branch ERP-38, chưa merge |
| Slot | capacity - booked_count | Đề xuất hiển thị; không có field remaining xác minh |
| Booking | action_confirm_booking, action_cancel_booking, action_mark_booking_served | Tên đề xuất; chưa có code develop |
| Slot | action_open_slot, action_close_slot | Có trên branch ERP-38; chưa xác minh runtime |

booked_count dự kiến tổng quantity confirmed + served. ERP-38 chưa có booking_ids/dependency tự tính lại. Không có chứng cứ backend enforce ownership hoặc concurrency.

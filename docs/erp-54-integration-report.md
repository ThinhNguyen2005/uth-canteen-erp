# ERP-54 — Kiểm tra tích hợp

Baseline develop 849b116. Odoo Community 20.0-20261123.

| UI / data | Backend / security | Kết quả và dependency |
|---|---|---|
| ERP-51 list/form/search | PR #25 09957db và group XML ERP-53 | Registry fixture đạt 3/3. Chờ TV4 xử lý invariant và merge model. |
| Booking list/form/search | Model, Confirm/Cancel/Serve | Chưa có backend xác minh trên develop. |
| ERP-52 actions/menu | Slot/Booking model, XML IDs view và group | Chờ ERP-50/51/53 và các quyền menu được duyệt. |
| Security load | XML nhóm → ir.access.csv → rules → views | ERP-53 fixture install/upgrade đạt. TV1 cần đổi ACL path trong manifest. Fixture chưa có ACL nghiệp vụ. |
| Capacity/count | booked_count của PR #25, booking compute dependencies | Chưa được xác minh từ booking thực tế và transaction độc lập. |

Chưa chạy E2E. Sau khi các branch được tích hợp, ghi SHA, database test, role, timezone, trạng thái và count trước/sau cho từng luồng. Ưu tiên cài/nâng cấp sạch, mở/đóng ca, create/confirm/serve/cancel, kiểm tra capacity rồi reload, lọc theo ngày và kiểm tra quyền theo ERP-48. Lưu log và ảnh tại từng bước thực thi. Không dùng log import view thay kết quả E2E.

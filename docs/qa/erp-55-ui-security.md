# ERP-55 — Kiểm thử UI và quyền

BLOCKED cho nghiệm thu tích hợp. Các kết quả dưới đây dựa trên probe PR #25 ngày 26/11, Odoo 20.0-20261123, DB uth_erp53_fix_20261125. Fixture dùng model 09957db và XML nhóm ERP-53 local, không có ACL slot đã duyệt.

| ID | Vai trò | Kiểm tra | Expected | Actual | Status | Owner / Evidence |
|---|---|---|---|---|---|---|
| SLOT-07/08 | Cashier thường | Gọi Open/Close qua ORM fixture | AccessError | Cả hai bị từ chối | PASS fixture | TV5 / pr25-tv5-action-probe-2026-11-26.log |
| SLOT-09 | Booking User thường | Gọi hai action qua ORM fixture | AccessError | Cả hai bị từ chối | PASS fixture | TV5 / cùng log |
| SLOT-10 | Internal không nhóm nghiệp vụ | Đọc slot fixture | AccessError | Bị từ chối, fixture không có ACL slot | PASS fixture | TV5 / cùng log |
| UI-01 | Mỗi role | Menu, list/form/search, breadcrumb, filter/group | Đúng role và action | Chưa có stack tích hợp | BLOCKED | TV5 / ERP-52–54 |
| UI-02 | Manager | Create/edit/save/discard, reload, archive, statusbar, capacity | Theo policy và dữ liệu nhất quán | Chưa chạy | BLOCKED | TV5 / ERP-51/53 |
| UI-03 | Booking User | Empty, no results, validation, nút theo state | Đúng thông báo và policy | Chưa có view booking | BLOCKED | TV5 / ERP-50 |
| SEC-01 | Các role và tổ hợp group | CRUD, scope own/other, field/action visibility | Theo ERP-48 đã duyệt | Ma trận chưa chốt | BLOCKED | TV4/TV5 |
| SEC-02 | Các role | Direct URL, RPC và server-side authorization | Không truy cập/thay đổi ngoài quyền | Chưa chạy | BLOCKED | TV4/TV5 |

Retest sau khi slot/booking, ACL và manifest sẵn sàng. Đối chiếu dữ liệu trước/sau và chạy hồi quy với tài khoản thường. Log cài ERP-53: KeyError ir.model.access. Không có ảnh giao diện tích hợp.

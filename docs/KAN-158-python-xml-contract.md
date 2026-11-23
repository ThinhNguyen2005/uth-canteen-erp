# KAN-158 — Contract Python–XML cho đặt món QR

> **Trạng thái:** Bản nháp TV4, chờ TV5 xác nhận và TV1 review vị trí lưu trong `docs/`.
> **Nguồn:** `docs/data-contract.md` và `docs/srs.md` trên `develop` tại `a89bef3`.
> **Phạm vi:** QR bàn cho ăn tại bàn; QR quầy cho mang đi; không tạo bàn ảo. Contract này thống nhất tên dùng giữa model Python, view/action XML và nhóm quyền, không triển khai giao diện hoặc bảo mật.

## 1. Quy ước chung

- Kế thừa các model Odoo chuẩn; không tạo model trùng cho bàn, món, đơn hoặc dòng đơn.
- Dùng các XML ID có tiền tố module `canteen_management`; các ID đề xuất dưới đây cần TV5 xác nhận trước khi dùng.
- QR bàn và QR quầy là hai ngữ cảnh riêng. Backend suy ra `fulfillment_type` từ QR token; client không tự chọn loại đơn.
- Khách công khai không đăng nhập. Không cấp ACL model cho `base.group_public`; route public chỉ thao tác qua controller đã xác thực token và kiểm tra payload.

## 2. Model, field, view và quyền

| Model | Technical fields Python | XML surface / XML ID đề xuất | Nhóm thao tác | Quy ước |
|---|---|---|---|---|
| `restaurant.table` | `name`, `floor_id`, `seats`, `qr_token`, `active` | Kế thừa form bàn: `view_restaurant_table_form_inherit_canteen_qr` | `group_canteen_manager` cấu hình/in QR; public chỉ quét token | Chỉ bàn vật lý. `qr_token` readonly trên form; `active=False` thì QR bị từ chối. |
| `pos.config` | `takeaway_qr_token`, `takeaway_qr_active` | Kế thừa form POS: `view_pos_config_form_inherit_canteen_takeaway` | `group_canteen_manager` xem/bật/tắt/tạo lại QR quầy | Dùng phương thức đã có trong contract: `action_regenerate_takeaway_qr`. Không tạo `restaurant.table` giả. |
| `product.template` | `canteen_published`, `canteen_is_out_of_stock`, `canteen_category` | Kế thừa form/list món: `view_product_template_form_inherit_canteen`, `view_product_template_list_inherit_canteen` | Manager sửa `canteen_published`/`canteen_category`; Kitchen sửa `canteen_is_out_of_stock` | Món hết vẫn hiện trên QR với nhãn “HẾT MÓN”, nhưng không thêm vào giỏ được. |
| `pos.order` | `fulfillment_type`, `table_id`, `floor_id`, `service_location_display`, `service_state`, `access_token`, `idempotency_key`, `request_hash` | Kế thừa list/form/Kanban đơn: `view_pos_order_tree_inherit_canteen`, `view_pos_order_form_inherit_canteen`, `view_pos_order_kanban_inherit_canteen` | Kitchen xem/cập nhật tiến độ bếp; Cashier/Waiter xác nhận thanh toán/giao món; nhân viên được phép hủy theo quy tắc trạng thái | Ăn tại bàn: `table_id` bắt buộc, `floor_id` lấy từ bàn. Mang đi: cả hai để trống. Khách tra cứu bằng `access_token`, không dùng ID tuần tự. |
| `pos.order.line` | `order_id`, `product_id`, `qty`, `price_unit`, `currency_id`, `price_subtotal`, `price_subtotal_incl`, `customer_note` | Hiển thị dòng món trên form/Kanban đơn; dùng cùng XML ID form đơn nêu trên nếu không cần view riêng | Kitchen/Cashier/Waiter đọc; khách gửi qua route public đã kiểm tra | Giá và thành tiền do server/POS tính; `customer_note` là ghi chú của khách. |

Các menu XML đã có: `menu_canteen_root`, `menu_canteen_operations`, `menu_canteen_configuration`. Ưu tiên gắn view/action vào menu hiện có; không tạo menu trùng chức năng POS chuẩn.

## 3. Trạng thái và nút/action

| Python field | Chuyển trạng thái | Nút hiển thị | Phương thức Python đề xuất | Nhóm |
|---|---|---|---|---|
| `pos.order.service_state` | `received` → `preparing` | Bắt đầu nấu | `action_start_preparing` | `group_canteen_kitchen` |
| `pos.order.service_state` | `preparing` → `ready` | Nấu xong | `action_mark_ready` | `group_canteen_kitchen` |
| `pos.order.service_state` | `ready` → `completed` | Đã giao món | `action_mark_completed` | `group_canteen_cashier` (Waiter) |
| `pos.order.service_state` | Trạng thái được phép hủy → `cancelled` | Hủy đơn | `action_cancel_service` | `group_canteen_kitchen`, `group_canteen_cashier`, `group_canteen_manager`; backend kiểm tra trạng thái |
| `product.template.canteen_is_out_of_stock` | `False` ↔ `True` | Báo hết món / Mở bán lại | `action_set_out_of_stock`, `action_set_available` | `group_canteen_kitchen` |
| `pos.config.takeaway_qr_token` | Sinh lại token | Tạo lại QR mang đi | `action_regenerate_takeaway_qr` | `group_canteen_manager` |

Tên bốn phương thức `action_start_preparing`, `action_mark_ready`, `action_mark_completed`, `action_cancel_service` và hai phương thức hết món là **đề xuất để TV4/TV5 chốt**, chưa phải tên đã tồn tại trong code. Backend phải chặn gọi trực tiếp nếu sai nhóm hoặc sai trạng thái; ẩn nút XML không thay thế kiểm tra quyền phía server.

## 4. XML ID đề xuất

| Loại | XML ID đề xuất | Ghi chú |
|---|---|---|
| Form món | `view_product_template_form_inherit_canteen` | Kế thừa form chuẩn; thêm trường menu và nút trạng thái hết món. |
| List món | `view_product_template_list_inherit_canteen` | Hiển thị trạng thái bán/hết món. |
| Form bàn | `view_restaurant_table_form_inherit_canteen_qr` | Quản lý token QR bàn vật lý. |
| Form cấu hình POS | `view_pos_config_form_inherit_canteen_takeaway` | Quản lý token/active QR quầy mang đi. |
| List đơn | `view_pos_order_tree_inherit_canteen` | Hiển thị mã đơn, vị trí, thời điểm, tổng tiền, trạng thái. |
| Form đơn | `view_pos_order_form_inherit_canteen` | Hiển thị dòng món/ghi chú và các nút chuyển trạng thái phù hợp. |
| Kanban đơn | `view_pos_order_kanban_inherit_canteen` | Dùng `service_state` làm cột KDS; nổi bật đơn mang đi. |

Các XML ID view cha của Odoo và ID `ir.actions.act_window` cụ thể cần TV5 xác nhận theo view chuẩn đang dùng trong Odoo 20 trước khi viết XML. Không tự thêm action/menu mới nếu có thể mở từ POS chuẩn.

## 5. Nhóm quyền hiện có

| XML ID group | Vai trò | Quyền nghiệp vụ QR |
|---|---|---|
| `group_canteen_user` | Customer / Student | Không dùng ACL để đặt đơn công khai; route QR public xử lý riêng. |
| `group_canteen_kitchen` | Kitchen Staff | Xem đơn; chuyển tiến độ nấu; đánh dấu món hết/mở lại. |
| `group_canteen_cashier` | Cashier / Waiter | Xem đơn; xác nhận thu tiền qua POS; xác nhận đã giao món. |
| `group_canteen_manager` | Canteen Manager | Bao gồm Kitchen và Cashier; cấu hình menu, QR bàn/quầy và quyền quản lý. |

## 6. Xác nhận của TV5

- [ ] Đồng ý tên model/field Python nêu trên với `docs/data-contract.md`.
- [ ] Đồng ý field nào xuất hiện trên form/list/Kanban và vị trí hiển thị.
- [ ] Đồng ý tên phương thức/nút chuyển trạng thái; bổ sung hoặc sửa tên nếu cần.
- [ ] Đồng ý nhóm được xem/sửa/thực hiện từng action; ACL public chỉ qua controller.
- [ ] Xác nhận XML ID view cha Odoo 20 và XML ID module đề xuất.
- [ ] Xác nhận không tạo bàn ảo; đơn mang đi không có `table_id`/`floor_id`.

Sau khi TV5 phản hồi, TV4 cập nhật bảng này và đồng bộ tên method/field với phần model; TV5 triển khai view/security theo contract đã duyệt. TV1 review thay đổi tài liệu trước khi nhập vào tài liệu chính.

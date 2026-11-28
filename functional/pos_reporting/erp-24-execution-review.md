# ERP-24 — Hướng dẫn thực thi và phiếu review

Trạng thái: **Đã thực thi kiểm thử VND trên Odoo 20 (5/5 kịch bản PASS); chỉ còn chờ TV1 phê duyệt**. Tài liệu này cụ thể hóa năm dòng trong `erp-24-scenarios.csv`; các giao dịch đều chạy trên môi trường thử độc lập `uth_kan151_152_test_20261126` (công ty `KAN147 Test VND`, tiền tệ `VND`, quầy `KAN147 Test VND POS` ID 4), không dùng dữ liệu khách thật hoặc tiền thật.

## Môi trường và kết quả thực thi (28/11/2026)

- **Phiên bản:** Odoo Community 20.0 (PostgreSQL 18.4, DB `uth_kan151_152_test_20261126`).
- **Người thực hiện:** Tạ Huy Thiên Văn (TV3) — ngày `28/11/2026`.
- **Quầy & phương thức thử:** `KAN147 Test VND POS` (ID 4), `KAN147 Test VND Cash` (ID 6, `cash`), `KAN147 Test VND Transfer Sim` (ID 7, `bank` mô phỏng).
- **Script tái kiểm read-only:** `functional/pos_reporting/kan146-vnd-regression.py`.

| ID | Điểm kiểm tra sau khi làm các bước trong CSV | Bằng chứng thực tế (DB `uth_kan151_152_test_20261126`, VND) | Kết quả thực tế |
| --- | --- | --- | --- |
| POS-01 | Tổng đơn 40.000; thu 50.000, trả 10.000; một đơn đã trả; tiền mặt dự kiến 140.000 với ca riêng. | Phiên `KAN147 Test VND POS/00009` (ID 9, `closed`); đơn ID `38` (`260-4-000003`, `done`), tổng `40.000 VND`, thu `50.000` trả thừa `10.000`, tiền mặt chốt ca `140.000 VND`, chênh lệch `0`. | **PASS** (ORM VND) |
| POS-02 | Giỏ sau sửa 20.000; hủy trước thu; không có khoản thu/doanh thu từ giỏ đó. Lưu vết hủy chỉ kiểm nếu quy định đã được duyệt. | Phiên `KAN147 Test VND POS/00010` (ID 10, `closed`); đơn ID `39` (`260-4-000004`, `cancel`), giỏ `35.000` sửa còn `20.000 VND` rồi hủy; `0` giao dịch thanh toán; tiền chốt ca giữ nguyên `100.000 VND`. | **PASS** (ORM VND) |
| POS-03 | Khi chưa rõ không hoàn tất; nếu nguồn thanh toán xác nhận thành công thì không thu lại; sau cùng tối đa một khoản thu thành công cho đơn. | Phiên `KAN147 Test VND POS/00011` (ID 11, `closed`); đơn ID `40` (`260-4-000005`, `done`, `30.000 VND`): bị chặn `UserError` khi chưa thanh toán và bị chặn đóng ca (`draft_orders`); sau khi xác nhận chuyển khoản giả lập ghi đúng `1` thanh toán `KAN147 Test VND Transfer Sim`. | **PASS** (ORM VND) |
| POS-04 | Đơn gốc 40.000; hoàn một món 20.000; liên kết đơn gốc, thuần 20.000; kiểm tra số lượng còn có thể hoàn. | Phiên `KAN147 Test VND POS/00012` (ID 12, `closed`); đơn gốc ID `41` (`40.000 VND`), đơn hoàn ID `42` (`-20.000 VND`) liên kết trực tiếp `refunded_orderline_id` về dòng gốc (`refunded_qty = 1`, còn lại `1`); tiền mặt thuần `+20.000`, chốt ca `120.000 VND`, chênh lệch `0`. | **PASS** (ORM VND) |
| POS-05 | Lỗi in không làm thu lại; có bằng chứng tìm lại đơn. Cuối ca dự kiến 140.000, đếm 139.000, chênh lệch −1.000; ghi nhận và chuyển quản lý. | Phiên `KAN147 Test VND POS/00013` (ID 13, `closed`); tra cứu lại đơn ID `43` (`260-4-000008`, đúng `1` thanh toán `40.000 VND`, không thu trùng); đếm cuối ca `139.000 VND`, sổ tiền mặt ghi dòng điều chỉnh `-1.000 VND` (`[40000.0, -1000.0]`). | **PASS** (ORM VND) |

> **Ghi chú phạm vi:** Các phép tính đơn, hoàn một phần, chặn đơn nháp/chưa thanh toán và điều chỉnh chênh lệch cuối ca đã được xác minh trực tiếp trên Odoo Community 20.0 bằng tiền tệ **VND** qua ORM. Chính sách phân quyền thu ngân/quản lý, lưu vết hủy, thời hạn hoàn và mẫu in biên lai vật lý chờ TV1 xác nhận trong phiếu review bên dưới.

## Phiếu TV1 review

| Nội dung | Quyết định | Người duyệt / ngày / liên kết |
| --- | --- | --- |
| Sơ đồ, gồm xử lý giao dịch thanh toán chưa rõ | Chờ TV1 (@thangvn0987) duyệt | Chờ review PR #50 |
| Vai trò thu ngân, quản lý ca, khách hàng | Chờ TV1 (@thangvn0987) duyệt | Chờ review PR #50 |
| POS-01 đến POS-05 và kết quả thực thi VND (Session 9–13) | Chờ TV1 (@thangvn0987) duyệt | Chờ review PR #50 |
| Điều kiện hủy, hoàn, quyền và xử lý chênh lệch | Chờ TV1 (@thangvn0987) duyệt | Chờ review PR #50 |
| Đối chiếu SRS ERP-05 và phạm vi Odoo thực tế | Chờ TV1 (@thangvn0987) duyệt | Chờ review PR #50 |

**Trạng thái hiện tại:** Đã hoàn tất tài liệu và kiểm thử thực tế VND (5/5 PASS); chỉ còn chờ TV1 (@thangvn0987) review và approve PR #50 để chuyển Done trên KAN-146.

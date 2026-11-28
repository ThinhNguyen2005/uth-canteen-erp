# KAN-147 — Đối chiếu giá POS và yêu cầu review

Trạng thái: **Đã hoàn tất đối chiếu 20/20 SKU và kiểm thử bán đủ 20 món trên Odoo 20 bằng tiền tệ VND; chỉ còn chờ TV2 xác nhận catalog/đơn vị bán và TV1 chốt người duyệt giá, thuế và quyền**. Dùng chung catalog TV2; không tạo bản ghi sản phẩm thứ hai.

## Đối chiếu catalog

Catalog [products.csv](../purchase_inventory/products.csv) trên develop gồm 20 SKU. Đối chiếu với bảng tham khảo kèm theo: 20 SKU duy nhất, tên, giá và đơn vị khớp; ID trong catalog có tiền tố `__import__.` còn cột `external_id` trong bảng chỉ chứa phần tên. Không nhập cột ID trần vào Odoo; đối chiếu ID đầy đủ với database đích trước.

## Kết quả kiểm thử thực tế trên Odoo 20 (VND — 28/11/2026)

- **Môi trường:** Odoo Community 20.0, DB thử `uth_kan151_152_test_20261126`, công ty thử riêng `KAN147 Test VND` (tiền tệ `VND`), quầy `KAN147 Test VND POS` (ID 4).
- **Xác minh 20/20 SKU:** Cả 20 sản phẩm đều tồn tại duy nhất trong công ty thử, khớp `default_code` (SKU), `name`, `uom_id` (`uom.product_uom_unit`), `available_in_pos = True` và `list_price` (VND) theo `kan147-bang-gia-tham-khao.csv`.
- **Phiên kiểm thử:** `KAN147 Test VND POS/00014` (ID 14, trạng thái `closed`, tiền đầu ca `100.000 VND`):
  - **Đơn ID `44` (Tiền mặt — 13 SKU nhóm `TV3_REUSE_AGREED`):** 13 dòng sản phẩm, tổng `340.000 VND`, thanh toán `KAN147 Test VND Cash`, trạng thái `done`.
  - **Đơn ID `45` (Chuyển khoản giả lập — 7 SKU nhóm `PENDING_TV3_REVIEW`):** 7 dòng sản phẩm, tổng `191.000 VND`, thanh toán `KAN147 Test VND Transfer Sim`, trạng thái `done`.
  - **Tổng doanh thu 20 SKU:** `531.000 VND`; chốt két tiền mặt `440.000 VND` (`100.000 + 340.000`), chênh lệch `0`.
- **Script tái kiểm read-only:** `functional/pos_reporting/kan147-vnd-20sku-regression.py`.

## Phần còn chờ duyệt (Review Gate)

| Người review | Nội dung cần xác nhận | Trạng thái |
| --- | --- | --- |
| **TV2 (`@TN-Kieran` — Trọng Nghĩa)** | Xác nhận catalog thực tế 20 SKU, đơn vị bán (`uom.product_uom_unit`) và quy đổi/tồn kho dùng chung. | Chờ review PR #51 |
| **TV1 (`@thangvn0987` — Minh Thắng)** | Xác định người có thẩm quyền duyệt giá, thuế (bao gồm hay cộng thêm), quyền thu ngân sửa giá và chính sách ưu đãi/combo. | Chờ review PR #51 |

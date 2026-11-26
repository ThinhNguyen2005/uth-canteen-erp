# KAN-150 — Đối chiếu catalog dùng chung và POS

Trạng thái: **chưa đồng bộ hoặc kiểm thử trên Odoo**. Phụ thuộc KAN-149, ERP-16 và ERP-20. Jira ghi nhận KAN-138 / ERP-16 Done và KAN-142 / ERP-20 In Review tại thời điểm kiểm tra; cần TV2 xác nhận catalog và tồn trên database thử trước khi chạy.

## Quy tắc đối chiếu

1. Dùng catalog gốc do TV2 bàn giao làm nguồn chuẩn; xác nhận phiên bản, database, công ty, SKU, external ID, tên, đơn vị bán, giá, thuế và tình trạng theo dõi tồn. Không tạo catalog hoặc bản ghi sản phẩm thứ hai cho POS.
2. Đọc cấu hình các sản phẩm hiện có và đối chiếu SKU/external ID với nguồn. Nếu thiếu, trùng hoặc đơn vị/giá khác, ghi khác biệt và chuyển TV2 xác minh trước khi thay đổi.
3. Với các bản ghi được TV2 xác nhận, kiểm tra thiết lập bán POS và nhóm POS theo quầy thử; không tự suy ra đơn vị bán từ tên sản phẩm hoặc tự sửa giá/kho thuộc TV2.
4. Đối chiếu tồn trước và sau cùng sản phẩm, đơn vị và vị trí kho. Ghi các biến động khác trong khoảng kiểm thử; với sản phẩm không quản lý tồn hoặc cấu hình BoM phải xác nhận kỳ vọng riêng với TV2.

## Ca nghiệm thu

| ID | Kiểm tra | Kết quả cần đối chiếu | Trạng thái |
| --- | --- | --- | --- |
| SP-01 | So danh sách SKU/external ID trong catalog đã xác nhận với bản ghi Odoo | Mỗi SKU thử có đúng bản ghi được xác nhận; sai lệch/trùng được ghi rõ | Chưa chạy |
| SP-02 | Mở POS và kiểm tra toàn bộ sản phẩm thử | Tất cả xuất hiện đúng tên, đơn vị và giá đã duyệt | Chưa chạy |
| SP-03 | Bán sản phẩm theo dõi tồn, số lượng biết trước | Lưu mã đơn/phiếu kho; tồn thay đổi theo cấu hình và quy đổi đã xác nhận | Chưa chạy |
| SP-04 | Kiểm tra sản phẩm không theo dõi tồn hoặc có BoM nếu thuộc phạm vi thử | Kết quả phù hợp chính sách tồn/BoM do TV2 xác nhận; không giả định trừ thành phẩm | Chưa chạy |

Ghi ngày giờ, người thực hiện, phiên bản catalog/Odoo, database, SKU, đơn vị, vị trí kho, tồn trước/sau, biến động khác, mã đơn/phiếu và ảnh/log cho từng ca. Dùng `product-mapping.csv` để ghi kết quả đối chiếu nếu phù hợp; CSV là bằng chứng tham chiếu, không phải catalog mới hoặc chỉ dẫn import. Chỉ đánh dấu Pass sau khi so với kết quả thực tế và review.

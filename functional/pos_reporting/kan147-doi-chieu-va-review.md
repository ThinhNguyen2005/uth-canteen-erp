# KAN-147 — Đối chiếu giá POS và yêu cầu review

Trạng thái: dự thảo, chưa duyệt giá/thuế, chưa chạy POS. Dùng chung catalog TV2; không tạo bản ghi sản phẩm thứ hai.

Catalog [products.csv](../purchase_inventory/products.csv) trên develop gồm 20 SKU. Đối chiếu với bảng tham khảo kèm theo: 20 SKU duy nhất, tên, giá và đơn vị khớp; ID trong catalog có tiền tố `__import__.` còn cột external_id trong bảng chỉ chứa phần tên. Không nhập cột ID trần vào Odoo; đối chiếu ID đầy đủ với database đích trước.

TV2 (Trọng Nghĩa) xác nhận catalog thực tế, đơn vị bán và quy đổi/tồn. Người có thẩm quyền duyệt giá và thuế xác nhận giá, thời hạn, thuế đã bao gồm hay chưa; TV1 xác nhận người có quyền duyệt, quyền thu ngân và chính sách ưu đãi. Ưu đãi/combo chưa được cấu hình hoặc duyệt.

Trước Done, kiểm tra database thử, sản phẩm POS và phép tính giá/thuế trên đơn thực tế; lưu mã đơn, kết quả và bằng chứng. TV1 và TV2 review; chưa khẳng định có tồn hoặc giá được duyệt.

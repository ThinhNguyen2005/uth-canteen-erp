# Đối chiếu KAN-146 với ERP-05

Ngày 26/11/2026: Jira ghi nhận [KAN-127 / ERP-05](https://nguyenthinhk52005.atlassian.net/browse/KAN-127) đã Done; [PR 3](https://github.com/ThinhNguyen2005/uth-canteen-erp/pull/3) được merge vào develop. Tài liệu đối chiếu: bản `docs/srs.md` trong bản sao ERP tại thời điểm kiểm tra, các use case UC03, UC08 và UC09. Cần xác nhận tài liệu này trùng bản đang được TV1 áp dụng trước khi nghiệm thu.

| Nội dung | Yêu cầu trong SRS | Điểm cần kiểm tra cho KAN-146 |
| --- | --- | --- |
| Bán tại quầy | UC03: phiên mở, chọn món, hình thức phục vụ, ghi chú, thanh toán, xác nhận và in bill | Kiểm thử luồng trên và lưu bằng chứng trên môi trường thử. |
| Thanh toán | UC03/UC09: tiền mặt hoặc chuyển khoản; thu ngân xác nhận; đóng ca đối chiếu tiền mặt và chuyển khoản | Xác nhận quy trình chuyển khoản mô phỏng trong môi trường thử; không suy ra đã có tích hợp ngân hàng tự động. |
| Hủy trước thanh toán | UC03 nêu hủy đơn nháp khi khách đổi ý | Đối chiếu trạng thái đơn và việc giải phóng bàn theo cấu hình thực tế. |
| Hết món sau thanh toán | UC08 nêu cảnh báo hoàn tiền, thu ngân trả tiền và ghi nhận trên POS | Cần TV1 xác nhận quyền và cách hoàn tiền; thử riêng trước khi kết luận. |
| Bếp và kho | UC03 nêu đẩy bếp và trừ nguyên liệu nếu cấu hình BoM | Xác minh cấu hình và tính khả dụng thực tế; không xem SRS là bằng chứng tính năng đã chạy. |

Đây là đối chiếu yêu cầu tĩnh, chưa phải kết quả chạy Odoo và chưa thay thế phê duyệt TV1 đối với sơ đồ, vai trò và 5 kịch bản của KAN-146.

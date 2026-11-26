# Hướng dẫn chạy Human UAT — ERP-57

Trước buổi UAT, điều phối viên ghi SHA đã tích hợp, phiên bản Odoo, URL và database riêng. Cấp tài khoản thử Manager, Cashier và Booking User theo ma trận đã duyệt qua kênh riêng. Chuẩn bị một người dùng khác để kiểm tra phạm vi đọc, món mẫu, một ca còn chỗ, một ca đầy và phiếu confirmed còn trong giờ phục vụ. Dùng dữ liệu giả lập. Đặt thời gian ca theo timezone người dùng.

1. Người nghiệm thu đăng nhập đúng role, thực hiện theo uat-checklist.csv và ghi Actual, Tester, Date và Evidence ngay sau mỗi ca.
2. Trường hợp sai expected, dừng tại điểm sai và ghi Bug ID, SHA, bước tái hiện, severity và ảnh đã che thông tin nhạy cảm. Phân công TV4 cho model/guards, TV5 cho views/security, TV1 cho manifest và phối hợp tích hợp.
3. Sau khi có fix, ghi revision mới và chạy lại ca lỗi cùng luồng liền kề. Cập nhật cột Retest của bug-register.csv bằng expected, actual, kết quả và link evidence. Chỉ đóng sau khi kiểm tra đạt.
4. Người nghiệp vụ ghi quyết định nghiệm thu thật trong acceptance-signoff.md. Giữ Pending UAT trước khi có người chạy và Pending Sign-off cho tới khi có quyết định.

## Retest report

| Bug ID | Fix SHA | Scope | Actual | Status | Evidence |
|---|---|---|---|---|---|
| TV5-01 | Chưa có revision tích hợp | Full addon install/upgrade | Chưa chạy sau patch manifest chính thức | Pending | Fixture có log riêng |
| TV5-02 | Chưa có fix TV4 | Slot state/capacity | Chưa retest sau fix | Pending | PR #25 |

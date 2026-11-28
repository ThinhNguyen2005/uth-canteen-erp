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
| TV5-02 | ed18146 | Slot state/capacity | System ORM fixture từ chối open với capacity 0 | PASS fixture | tv5-backend-alignment-install.log |
## Workflow theo PR #40

Kiểm tra phiếu thường tạo confirmed với 1–3 suất và Manager tạo draft nội bộ không giữ suất. Manager confirm hoặc cancel draft. Cashier giao phiếu confirmed; sau served/cancelled không chuyển tiếp. Dùng hai tài khoản Booking User để kiểm tra phạm vi own-record. Chuẩn bị ba ca có cutoff hủy 31, 30, 29 phút; 31/30 hợp lệ và 29 bị từ chối nếu các điều kiện khác đủ. Manager được xử lý ngoại lệ. Chờ ERP-42/43 trước Human UAT các ca ghi trực tiếp và cạnh tranh suất cuối.

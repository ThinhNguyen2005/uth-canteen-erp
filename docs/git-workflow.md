# Git workflow

- `main`: bản ổn định; nhận PR đã review từ `develop`.
- `develop`: tích hợp; tạo `feature/ERP-xx-mo-ta` từ develop.
- PR ghi Jira, phạm vi, kiểm thử, rủi ro; ít nhất một thành viên khác review, mời owner khi chạm vùng của họ.
- Không commit secrets, database hoặc filestore. Không tự sửa vùng sở hữu khác khi chưa có yêu cầu hoặc review.
- Bảo vệ nhánh và quyền merge phải được quản trị viên cấu hình trên GitHub; tài liệu không tự bật chúng. Tạo develop từ commit nền tảng sau khi kiểm tra.

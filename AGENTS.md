# Quy ước dự án

Odoo Community 20; ưu tiên tính năng chuẩn; không đưa secrets hoặc dữ liệu thật vào Git. Không tự sửa file của thành viên khác nếu không có yêu cầu hoặc review của owner.

| Người | Quyền sở hữu |
| --- | --- |
| TV1 | Docker, config, manifest, README, docs, scripts, tích hợp |
| TV2 | functional/purchase_inventory/ |
| TV3 | functional/pos_reporting/ |
| TV4 | addons/canteen_management/models/ |
| TV5 | addons/canteen_management/views/, security/, tests/ |

Scaffold ban đầu theo yêu cầu khởi tạo. Thay đổi liên vùng cần owner review. TV1 phối hợp manifest với TV4–TV5. Nhánh main ổn định, develop tích hợp, feature từ develop; PR và review trước merge. Xem docs/git-workflow.md. Không tự push hay sửa Jira khi chưa được yêu cầu.

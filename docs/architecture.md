# Kiến trúc dự thảo

```mermaid
flowchart TD
 U[Trình duyệt local] -->|127.0.0.1:8069| O[Odoo Community 20]
 O -->|mạng nội bộ| P[PostgreSQL 16]
 O --> A[Custom addons]
 O --> F[Volume filestore]
 P --> D[Volume database]
```

Ưu tiên ứng dụng chuẩn mua hàng, kho, POS, báo cáo sau khi kiểm chứng phù hợp Community; addon chỉ mở rộng nghiệp vụ còn thiếu. Database không publish cổng. Tag image có thể thay đổi; nhóm cần chốt digest sau kiểm thử thực tế.

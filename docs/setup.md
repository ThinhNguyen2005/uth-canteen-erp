# Thiết lập trên Windows

Cài Docker Desktop, bật Linux containers và chạy Docker Engine. Tại PowerShell trong thư mục repo, chạy `./scripts/doctor.ps1` để kiểm tra cổng và môi trường. Không dừng container dự án khác.

```powershell
Copy-Item .env.example .env
Copy-Item config/odoo.conf.example config/odoo.conf
notepad .env
notepad config/odoo.conf
docker compose config --quiet
docker compose up -d
docker compose ps
./scripts/verify.ps1
```

Đặt mật khẩu PostgreSQL và database manager riêng, mạnh; dùng chữ và số cho mật khẩu PostgreSQL để tránh ký tự đặc biệt trong `.env`. Không commit các file local. Nếu cổng 8069 bận, giải quyết xung đột trước. Mở http://localhost:8069, tạo database thử nghiệm bằng mật khẩu database manager. Bật developer mode, cập nhật Apps List, bỏ bộ lọc Apps và tìm UTH Canteen Management.

Chỉ dùng lệnh sau trên database thử nghiệm riêng, không chạy trên database thật:

```powershell
docker compose run --rm --no-deps odoo odoo -d TEN_DB_THU_NGHIEM -i canteen_management --stop-after-init --without-demo=True
docker compose run --rm --no-deps odoo odoo -d TEN_DB_THU_NGHIEM -u canteen_management --stop-after-init --without-demo=True
```

Thay cả hai tên bằng cùng tên database thử nghiệm và kiểm tra mã thoát/log. Dừng bằng `docker compose stop`; không dùng `down -v` hay volume prune. Đổi `POSTGRES_PASSWORD` trong `.env` sau khi tạo volume không đổi mật khẩu database đã có. Cần sao lưu cả database và filestore; đây không phải cấu hình production, không mở Internet.

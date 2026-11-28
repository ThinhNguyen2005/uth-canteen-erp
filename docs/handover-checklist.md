# BIÊN BẢN BÀN GIAO & CHECKLIST NGHIỆM THU DỰ ÁN
## HỆ THỐNG HOẠCH ĐỊNH & VẬN HÀNH CĂN TIN ĐẠI HỌC (UTH CANTEEN ERP)
**Mã nhiệm vụ Jira:** [KAN-134](https://nguyenthinhk52005.atlassian.net/browse/KAN-134) ([ERP-12][TV1] Hoàn thiện README, slide, tài liệu bàn giao)  
**Thuộc Epic:** [KAN-118](https://nguyenthinhk52005.atlassian.net/browse/KAN-118) ([UTH Canteen ERP] DevOps và tích hợp)  
**Phiên bản bàn giao:** `v1.0.0-mvp` (Semantic Versioning 2.0.0)  
**Ngày lập biên bản:** 23/11/2026 *(Hiệu đính danh sách đội ngũ & liên kết: 28/11/2026)*  
**Địa điểm thực hiện:** Trường Đại học Giao thông vận tải TP.HCM (UTH)

---

## 1. THÔNG TIN CÁC BÊN THAM GIA BÀN GIAO

### 1.1. Bên Bàn Giao (Ban Phát Triển Dự Án — Nhóm N2)
* **Trưởng nhóm / Kỹ sư DevOps & Tích hợp (TV1):** Thắng Nguyễn Minh (`thangnm7509@ut.edu.vn` / `thangvn0987`) — Phụ trách Kiến trúc, DevOps, Tích hợp E2E & Đóng gói phát hành (`KAN-118`).
* **Kỹ sư Mua hàng & Tồn kho (TV2):** Trọng Nghĩa (`TN-Kieran`) — Phụ trách phân hệ Mua hàng (`purchase`) & Tồn kho (`stock`) (`KAN-119`).
* **Kỹ sư Bán lẻ POS & Báo cáo (TV3):** Văn Tạ Huy Thiên (`TaHuyThienVan`) — Phụ trách Điểm bán lẻ POS Restaurant, sơ đồ bàn ăn & Báo cáo đối soát (`KAN-120`).
* **Kỹ sư Backend Odoo & Đặt suất ăn (TV4):** Dịch Viết Đức (`dichvietduc2005`) — Phụ trách mô hình dữ liệu `addons/canteen_management/models/`, ca ăn, đặt suất ăn & concurrency locking (`KAN-121`).
* **Kỹ sư UI, Bảo mật & Kiểm thử QA (TV5):** Huỳnh Anh Phú (`AnhPhu2306`) — Phụ trách giao diện Views/Menus, ma trận phân quyền Odoo 20 (`security/`), kiểm thử tự động & UAT (`KAN-122`).
* **Quản trị Repository & Điều phối dự án:** Nguyễn Hoàng Gia Thịnh (`ThinhNguyen2005` / `nguyenthinhk52005@gmail.com`) — Repository Owner (`ThinhNguyen2005/uth-canteen-erp`) & Quản trị Jira dự án `KAN`.

### 1.2. Bên Tiếp Nhận (Hội Đồng Đánh Giá & Quản Trị Vận Hành)
* **Đơn vị tiếp nhận:** Ban Quản trị Cơ sở vật chất & Căn tin UTH.
* **Hội đồng chuyên môn:** Giảng viên hướng dẫn & Hội đồng đánh giá Đồ án Chuyên ngành Công nghệ Thông tin UTH.

---

## 2. BẢNG CHECKLIST HẠNG MỤC BÀN GIAO (DELIVERABLES CHECKLIST)

### 2.1. Mã Nguồn & Hạ Tầng Triển Khai (Source Code & Infrastructure)

| STT | Tên Hạng Mục Bàn Giao | Vị Trí Lưu Trữ / Đường Dẫn | Trạng Thái | Ghi Chú Kỹ Thuật |
|:---:|:---|:---|:---:|:---|
| 1 | Kho mã nguồn Git chính thức | [GitHub Repository](https://github.com/ThinhNguyen2005/uth-canteen-erp) | **ĐÃ TÍCH HỢP (`develop`)** | Nhánh `develop` đã tích hợp nền tảng MVP v1.0.0 cùng các PR đã duyệt; đồng bộ hiệu đính đội ngũ & tài liệu theo GitFlow |
| 2 | Phân hệ Căn tin Odoo 20 | [addons/canteen_management/](../addons/canteen_management/) | **ĐÃ BÀN GIAO** | Version `20.0.1.0.0`, License LGPL-3, 6 dependencies Odoo 20 |
| 3 | Khai báo hạ tầng Docker Compose | [docker-compose.yml](../docker-compose.yml) | **ĐÃ BÀN GIAO** | Image `postgres:16` & `odoo:20.0`, port host `8069`, healthcheck tự động |
| 4 | Cấu hình biến môi trường mẫu | [.env.example](../.env.example) | **ĐÃ BÀN GIAO** | Biến an toàn, không chứa mật khẩu thực tế |
| 5 | Cấu hình máy chủ Odoo mẫu | [config/odoo.conf.example](../config/odoo.conf.example) | **ĐÃ BÀN GIAO** | Đầy đủ `addons_path` core và extra-addons, `db_host = db` |
| 6 | Quy tắc an toàn mã nguồn Git | [.gitignore](../.gitignore) | **ĐÃ BÀN GIAO** | Chặn triệt để tệp `.env`, `odoo.conf`, tệp tạm `backups/temp_*` |

### 2.2. Gói Phát Hành CSDL & Công Cụ Tự Động Hóa (Release & Test Suites)

| STT | Tên Hạng Mục Bàn Giao | Vị Trí Lưu Trữ / Đường Dẫn | Trạng Thái | Ghi Chú Kỹ Thuật |
|:---:|:---|:---|:---:|:---|
| 7 | Gói sao lưu CSDL chuẩn MVP | [backups/uth_canteen_db_v1.0.0_mvp.zip](../backups/uth_canteen_db_v1.0.0_mvp.zip) | **ĐÃ BÀN GIAO** | Kích thước 3.79 KB; đủ `manifest.json`, `dump.sql`, `filestore/` |
| 8 | Mã băm mật mã SHA-256 | [backups/uth_canteen_db_v1.0.0_mvp.sha256](../backups/uth_canteen_db_v1.0.0_mvp.sha256) | **ĐÃ BÀN GIAO** | Mã băm cố định: `e0db1a08f36e38b89378dbe657b0b56de252073936e77e8084ed4b82c468da94` |
| 9 | Script sao lưu Windows (PS1) | [scripts/backup_db.ps1](../scripts/backup_db.ps1) | **ĐÃ BÀN GIAO** | Tự động đọc `.env`, hỗ trợ chế độ container live và `-ForceOffline` |
| 10 | Script phục hồi Windows (PS1) | [scripts/restore_db.ps1](../scripts/restore_db.ps1) | **ĐÃ BÀN GIAO** | Xác thực SHA-256, tự động ngắt lock session và khôi phục CSDL |
| 11 | Script sao lưu POSIX (Bash) | [scripts/backup_db.sh](../scripts/backup_db.sh) | **ĐÃ BÀN GIAO** | Chạy trên Linux/macOS/Docker CI |
| 12 | Script phục hồi POSIX (Bash) | [scripts/restore_db.sh](../scripts/restore_db.sh) | **ĐÃ BÀN GIAO** | Hỗ trợ nạp CSDL tự động trên Linux container |
| 13 | Suite Kiểm thử Tích hợp E2E | [scripts/test_integration_suite.py](../scripts/test_integration_suite.py) | **ĐÃ BÀN GIAO** | 29 kịch bản kiểm thử tự động đạt PASS 100% |
| 14 | Suite Kiểm toán Release MVP | [scripts/verify_release_mvp.py](../scripts/verify_release_mvp.py) | **ĐÃ BÀN GIAO** | 18 kịch bản kiểm toán đóng gói đạt PASS 100% |
| 15 | Suite Thẩm định Bàn giao | [scripts/verify_handover_suite.py](../scripts/verify_handover_suite.py) | **ĐÃ BÀN GIAO** | 15 kịch bản kiểm toán bàn giao đạt PASS 100% |

### 2.3. Hồ Sơ Tài Liệu Kỹ Thuật & Cẩm Nang Vận Hành (Documentation)

| STT | Tên Tài Liệu Bàn Giao | Vị Trí Lưu Trữ / Đường Dẫn | Trạng Thái | Quy Mô / Nội Dung Chính |
|:---:|:---|:---|:---:|:---|
| 16 | Cẩm nang hướng dẫn tổng thể | [README.md](../README.md) | **ĐÃ BÀN GIAO** | Hướng dẫn cài đặt nhanh, kiến trúc, tài khoản demo, troubleshooting |
| 17 | Đặc tả yêu cầu phần mềm (SRS) | [docs/srs.md](srs.md) | **ĐÃ BÀN GIAO** | 62 trang theo IEEE 830, mô tả 100% Use Cases 5 phân hệ |
| 18 | Đặc tả kiến trúc hệ thống | [docs/architecture.md](architecture.md) | **ĐÃ BÀN GIAO** | Sơ đồ phân tầng, thành phần Docker, luồng dữ liệu, NFR |
| 19 | Hợp đồng kỹ thuật dữ liệu v2.0 | [docs/data-contract.md](data-contract.md) | **ĐÃ BÀN GIAO** | Chuẩn hóa 100% schema trường, model names, khóa ngoại |
| 20 | Quy chuẩn phân nhánh & Review | [docs/git-workflow.md](git-workflow.md) | **ĐÃ BÀN GIAO** | Quy định GitFlow, branch naming, PR checklist và review rule |
| 21 | Cẩm nang dữ liệu hạt giống | [docs/demo-dataset-guide.md](demo-dataset-guide.md) | **ĐÃ BÀN GIAO** | Catalog 13 món, 8 bàn, 5 NCC, 10 NVL, 3 ca ăn |
| 22 | Hướng dẫn tích hợp E2E | [docs/integration-e2e-guide.md](integration-e2e-guide.md) | **ĐÃ BÀN GIAO** | Quy trình phối hợp vận hành thực tế giữa 5 thành viên |
| 23 | Báo cáo kiểm thử tích hợp E2E | [docs/integration-test-report.md](integration-test-report.md) | **ĐÃ BÀN GIAO** | Kết quả 29 ca kiểm thử tự động đạt PASS 100% |
| 24 | Cẩm nang phát hành & phục hồi | [docs/release-mvp-guide.md](release-mvp-guide.md) | **ĐÃ BÀN GIAO** | Hướng dẫn khôi phục máy chủ sạch, 18 kịch bản verify |
| 25 | Slide thuyết trình tổng kết 3 tuần | [docs/presentation-slide-deck.md](presentation-slide-deck.md) | **ĐÃ BÀN GIAO** | Bộ slide 16 trang chuẩn Marp Presentation |
| 26 | Biên bản bàn giao và checklist | [docs/handover-checklist.md](handover-checklist.md) | **ĐÃ BÀN GIAO** | Bản nghiệm thu hoàn chỉnh và ký duyệt |

---

## 3. CHECKLIST ĐỐI SOÁT TIÊU CHÍ NGHIỆM THU TỪNG PHÂN HỆ

### 3.1. Phân hệ Mua Hàng & Quản Trị Kho (SCM & Stock — TV2)
- [x] Đã nạp danh mục 5 nhà cung cấp uy tín tại TP.HCM và Lâm Đồng (`supplier_rank=1`).
- [x] Đã nạp danh mục 10 nguyên vật liệu thiết yếu với định lượng rõ ràng (`detailed_type=consu`, `purchase_ok=True`).
- [x] Luồng Mua hàng ➔ Nhập kho liên kết tự động giữa Purchase Order (`PO/2026/0001`) và Stock Picking (`WH/IN/0001`).
- [x] Xác thực trừ kho nguyên vật liệu tương ứng khi bếp xác nhận nấu món ăn.

### 3.2. Phân hệ Điểm Bán Lẻ POS & Sơ Đồ Bàn Ăn (POS Restaurant — TV3)
- [x] Khởi tạo và quản lý phiên bán hàng POS thu ngân (`pos.session`) đầy đủ số dư đầu ca và tổng kết cuối ca.
- [x] Thiết lập sơ đồ 8 bàn ăn vật lý phân bổ trên 3 sảnh/tầng (`floor_sanh_chinh`, `floor_tang_lung`, `floor_san_vuon`).
- [x] **Triệt tiêu 100% bàn ảo Takeaway:** Đơn mang về bắt buộc gán `table_id=None` và `floor_id=None`.
- [x] Hỗ trợ in hóa đơn, hiển thị địa điểm phục vụ rõ ràng và tích hợp máy quét mã vạch.

### 3.3. Phân hệ Backend Odoo, Điều Phối Bếp & Đặt Suất Ăn (Backend Models — TV4)
- [x] Đã tích hợp 3 mô hình cốt lõi vào nhánh `develop`: ca ăn (`canteen.meal.slot`), đặt suất ăn (`canteen.meal.booking`) và mở rộng hồ sơ đối tác sinh viên (`res.partner`) tại `addons/canteen_management/models/`.
- [x] Đã chuẩn hóa hợp đồng vòng đời trạng thái món ăn (`draft` $\rightarrow$ `confirmed` $\rightarrow$ `serving` $\rightarrow$ `done`), cờ báo hết món tức thời (`canteen_is_out_of_stock=True`) và kiểm định **An ninh Zero-Trust** chống giả mạo giá (`Price Tampering`) trong bộ kiểm thử tích hợp.
- [ ] Hoàn tất merge workflow actions (`KAN-163`), guard ràng buộc (`KAN-164`) và khóa đồng thời `SELECT FOR UPDATE` (`KAN-165`) vào `develop` *(đang rà soát tại các PR `#40`, `#44`–`#47` của TV4)*.

### 3.4. Giao Diện UI, Phân Quyền Bảo Mật & Kiểm Thử (UI, Security & QA — TV5)
- [x] Đã nạp danh mục 13 món ăn thành phẩm và 3 ca ăn (Ca Trưa 1: 11h-12h, Ca Trưa 2: 12h-13h, Ca Chiều: 17h-18h30) trong dữ liệu mẫu (`demo/canteen_demo_data.xml`) cùng khung thư mục `views/`, `security/`, `tests/`.
- [x] Đã khởi tạo khung phân quyền Odoo 20 (`security/canteen_security.xml`, `security/ir.model.access.csv`, `security/canteen_rules.xml`) và kiểm định luồng đặt món QR/PIN, chống IDOR qua bộ kiểm thử tích hợp tự động (`scripts/test_integration_suite.py`).
- [ ] Hoàn tất merge bộ giao diện Views/Menus chi tiết, kích hoạt bảng ACL/Record Rules thực thi trên `develop` và bộ test trong `addons/canteen_management/tests/` *(đang triển khai tại các nhánh feature của TV5)*.

### 3.5. DevOps, Tích Hợp & Đóng Gói Hệ Thống (DevOps & Integration — TV1)
- [x] Toàn bộ 12 nhiệm vụ Jira của TV1 ([KAN-123](https://nguyenthinhk52005.atlassian.net/browse/KAN-123) đến [KAN-134](https://nguyenthinhk52005.atlassian.net/browse/KAN-134)) hoàn thành 100%.
- [x] Xây dựng bộ script sao lưu và phục hồi CSDL tự động đa nền tảng (`.ps1` và `.sh`).
- [x] Đóng gói thành công bản phát hành CSDL MVP `uth_canteen_db_v1.0.0_mvp.zip` tất định (Deterministic Build).
- [x] Vượt qua quy trình kiểm định Zero Defect Review Loop khắt khe, đạt **0 khuyết tật**.

---

## 4. TỔNG KẾT BẰNG CHỨNG KIỂM ĐỊNH TỰ ĐỘNG (TEST SUITE MATRIX)

```text
================================================================================
 BẢNG TỔNG HỢP KẾT QUẢ KIỂM THỬ TỰ ĐỘNG HỆ THỐNG UTH CANTEEN ERP
================================================================================
 1. E2E Integration Suite (test_integration_suite.py) : 29 / 29 PASS (100%)
 2. Release MVP Suite     (verify_release_mvp.py)     : 18 / 18 PASS (100%)
 3. Handover Suite        (verify_handover_suite.py)  : 15 / 15 PASS (100%)
--------------------------------------------------------------------------------
 TỔNG CỘNG KIỂM ĐỊNH     : 62 KỊCH BẢN THỬ NGHIỆM ĐẠT 100% (0 LỖI / ZERO DEFECT)
================================================================================
```

---

## 5. DANH MỤC TÀI KHOẢN VẬN HÀNH & HƯỚNG DẪN BẢO MẬT BÀN GIAO

### 5.1. Danh Sách Tài Khoản Mặc Định
#### A. Tài khoản Đăng nhập Hệ thống Odoo (Internal Users)
| Nhóm Người Dùng | Tên Tài Khoản (Login) | Mật Khẩu Khởi Tạo | Vai Trò & Nhóm Quyền Odoo |
|:---|:---|:---:|:---|
| **Quản trị viên Tối cao** | `admin` | `admin` (hoặc `uth@2026`) | Toàn quyền cấu hình, tài chính, phân quyền (`group_canteen_manager`) |
| **Bếp trưởng (Kitchen)** | `kitchen@uth.edu.vn` | `uth@2026` | Quản trị KDS, điều phối nấu món, báo hết món (`group_canteen_kitchen`) |
| **Thu ngân (Cashier)** | `cashier@uth.edu.vn` | `uth@2026` | Bán lẻ POS, nhận tiền, in hóa đơn, đóng mở phiên (`group_canteen_cashier`) |

#### B. Hồ sơ Khách hàng Demo Mẫu (Demo Customers / End-Users)
*Lưu ý: Khách hàng sinh viên và giảng viên đặt món trực tiếp qua Web QR Portal không cần đăng nhập backend Odoo:*
| Tên Khách Hàng | Email Đối Tác (`res.partner`) | Đối Tượng | Hành Vi Thử Nghiệm Nghiệm Thu |
|:---|:---|:---:|:---|
| **Nguyễn Văn An** | `an.nguyen.k21@uth.edu.vn` | Sinh viên K21 CNTT | Đặt suất ăn trước Ca trưa 1, nhận mã QR/PIN nhận món |
| **Trần Thị Mai** | `mai.tran.k22@uth.edu.vn` | Sinh viên K22 Kinh tế | Đặt suất ăn trước Ca trưa 2, kiểm tra lịch sử đặt món |
| **TS. Lê Hoàng Nam** | `nam.lehoang@uth.edu.vn` | Giảng viên Viện Hàng hải | Đặt cơm trưa giảng viên, ưu tiên chọn bàn tại sảnh |

### 5.2. Khuyến Nghị Bảo Mật Khi Đưa Vào Vận Hành Thực Tế (Go-Live Security)
1. **Đổi mật khẩu Master Password của Odoo:** Chỉnh sửa giá trị `admin_passwd` trong `config/odoo.conf` từ `change_this_master_password` thành mật khẩu phức tạp ($\ge 16$ ký tự gồm chữ hoa, chữ thường, số và ký tự đặc biệt).
2. **Đổi mật khẩu CSDL PostgreSQL:** Cập nhật biến `POSTGRES_PASSWORD` trong tệp `.env` môi trường thực tế.
3. **Cấu hình Reverse Proxy & HTTPS:** Khuyến nghị đặt Nginx hoặc Traefik phía trước Odoo container và kích hoạt chứng chỉ SSL/TLS miễn phí từ Let's Encrypt.
4. **Phân quyền truy cập tệp:** Đảm bảo thư mục `config/` và `.env` chỉ người dùng root hoặc docker group mới có quyền đọc (`chmod 600 .env config/odoo.conf`).

---

## 6. KÝ DUYỆT & XÁC NHẬN BÀN GIAO (SIGN-OFF)

Biên bản bàn giao này được lập thành 02 bản có giá trị pháp lý và kỹ thuật tương đương nhau, mỗi bên giữ 01 bản để làm căn cứ bảo hành và vận hành hệ thống.

<br/>

| ĐẠI DIỆN BÊN TIẾP NHẬN BÀN GIAO | ĐẠI DIỆN BÊN BÀN GIAO (PROJECT LEAD) |
|:---:|:---:|
| *(Ký, ghi rõ họ tên và đóng dấu)* | *(Ký và ghi rõ họ tên)* |
| <br/><br/><br/><br/> | <br/><br/><br/><br/> |
| **HỘI ĐỒNG NGHIỆM THU UTH** | **THẮNG NGUYỄN MINH** |
| Ngày: ..... / ..... / 2026 | Ngày: 28 / 11 / 2026 |

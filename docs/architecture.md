# Kiến trúc Hệ thống & Hạ tầng Kỹ thuật — UTH Canteen ERP

> **Dự án:** UTH Canteen ERP — Hệ thống Quản trị Căn tin Đại học Giao thông vận tải TP.HCM  
> **Nền tảng:** Odoo Community 20.0 & PostgreSQL 16 trên Docker Engine (Môi trường Windows Workstation Hybrid)  
> **Chủ sở hữu:** TV1 (DevOps & Infrastructure Architect / Project Lead)  
> **Tài liệu tham chiếu:** [docs/srs.md](file:///G:/0duanmobile/uth-canteen-erp/docs/srs.md), [docs/data-contract.md](file:///G:/0duanmobile/uth-canteen-erp/docs/data-contract.md), [docker-compose.yml](file:///G:/0duanmobile/uth-canteen-erp/docker-compose.yml), [config/odoo.conf](file:///G:/0duanmobile/uth-canteen-erp/config/odoo.conf)  
> **Tiêu chuẩn thiết kế:** 12-Factor App, Multi-tier Containerized Architecture, Zero Data-Loss Strategy, Least Privilege Network Isolation  

---

## 1. Tổng quan và Mục tiêu Kiến trúc (Architectural Goals & Principles)

### 1.1. Bối cảnh Vận hành Đặc thù
Hệ thống **UTH Canteen ERP** phục vụ lưu lượng sinh viên, giảng viên và nhân viên với mô hình tải biến thiên mạnh:
* **Tải đỉnh tập trung (Spike Traffic):** Giờ giải lao (9:00 - 9:30, 15:00 - 15:30) và ca ăn trưa (11:00 - 12:45) với mật độ truy cập cao điểm từ máy quét mã QR di động và các quầy POS thu ngân hoạt động liên tục.
* **Đặc tính dữ liệu:** Đòi hỏi tính nhất quán cao độ (Strict ACID), giao dịch kho nguyên liệu và khóa dòng suất ăn theo ca (`canteen.meal.slot`) nhằm chống hiện tượng bán vượt định mức (Overbooking).
* **Môi trường hạ tầng triển khai:** Máy trạm Windows vật lý cấu hình lai (Hybrid Storage): Ổ đĩa thể rắn `Intel SSD C: 128GB` (tốc độ I/O cao nhưng dung lượng giới hạn) và Ổ cứng cơ `HDD G: 1TB` (dung lượng lưu trữ lớn).

### 1.2. Mục tiêu Kỹ thuật Cốt lõi
* **Tính sẵn sàng (High Availability):** RPO (Recovery Point Objective) $\le$ 24 giờ (hoặc sau mỗi ca bán hàng); RTO (Recovery Time Objective) $\le$ 15 phút khi phát sinh thảm họa phần cứng.
* **Hiệu năng & Độ trễ (Performance & Latency):** Phản hồi giao dịch POS bán lẻ $< 200\text{ms}$; truy vấn danh mục thực đơn QR $< 500\text{ms}$.
* **Bảo mật Đa lớp (Defense-in-Depth):** Cô lập triệt để tầng cơ sở dữ liệu bên trong mạng container nội bộ; chặn toàn bộ truy cập quản trị database từ môi trường mạng ngoài.
* **Nguyên tắc Không Khuyết tật (Zero Defect Infrastructure):** Mọi tham số cấu hình bộ nhớ, worker, disk space, log rotation và backup runbook đều phải được đặc tả tường minh, có thể kiểm chứng độc lập.

---

## 2. Mô hình Kiến trúc Phân tầng Toàn diện (Multi-tier Architecture Overview)

### 2.1. Sơ đồ Kiến trúc Tổng thể (Comprehensive System Architecture)

```mermaid
flowchart TD
    subgraph ClientTier["TẦNG 1: THIẾT BỊ ĐẦU CUỐI (CLIENT LAYER)"]
        POS["Thiết bị POS / Màn hình cảm ứng thu ngân\n(Browser / Touchscreen)"]
        MobileQR["Điện thoại thông minh Khách hàng\n(Web-responsive QR Portal)"]
        AdminWeb["Trình duyệt Máy tính Quản trị\n(Odoo Backend Web Client)"]
        EscPrinter["Máy in Hóa đơn Nhiệt\n(Thermal ESC/POS TCP 9100)"]
    end

    subgraph IngressTier["TẦNG 2: ĐIỀU PHỐI & AN NINH MẠNG (INGRESS & REVERSE PROXY)"]
        Nginx["Nginx Reverse Proxy & SSL Termination\n(Cổng 80/443 -> 8069, Rate Limit, Static Cache)"]
    end

    subgraph AppTier["TẦNG 3: MÁY CHỦ ỨNG DỤNG (APPLICATION SERVER - ODOO 20.0)"]
        direction TB
        MasterProc["Odoo Master Process\n(Container: uth-canteen-erp-odoo-1)"]
        WSGIWorker1["WSGI HTTP Worker #1\n(Xử lý POS & Admin Requests)"]
        WSGIWorker2["WSGI HTTP Worker #2\n(Xử lý QR Khách & Đơn hàng)"]
        GeventWorker["Gevent Longpolling/Websocket\n(Cổng 8072 - Real-time Bus)"]
        CronWorker["Cron Thread (1 thread)\n(Quét tự động hết hạn ca đặt ăn)"]

        MasterProc --> WSGIWorker1
        MasterProc --> WSGIWorker2
        MasterProc --> GeventWorker
        MasterProc --> CronWorker
    end

    subgraph AddonsTier["TẦNG 4: MÔ-ĐUN NGHIỆP VỤ (BUSINESS LOGIC LAYER)"]
        StandardAddons["Odoo Standard Addons:\nbase, web, purchase, stock, point_of_sale, pos_restaurant"]
        CustomAddon["Custom Business Addon:\naddons/canteen_management"]
    end

    subgraph DatabaseTier["TẦNG 5: CƠ SỞ DỮ LIỆU & LƯU TRỮ VĨNH VIỄN (PERSISTENCE LAYER)"]
        PG["PostgreSQL 16 Engine\n(Container: uth-canteen-erp-db-1)\nCổng nội bộ: 5432 (Isolated)"]
        subgraph StorageLayer["LƯU TRỮ VĨNH VIỄN (STORAGE VOLUMES & RUNTIME MOUNTS)"]
            DBVol[("postgres_data\n(/var/lib/postgresql/data)\nSSD C: [WSL2]")]
            OdooVol[("odoo_data\n(/var/lib/odoo - Filestore/Sessions)\nSSD C: [WSL2]")]
            AddonsMount["Bind Mount: ./addons\n(/mnt/extra-addons:ro)\nHDD G: [Mã nguồn dự án]"]
            ConfigMount["Bind Mount: ./config/odoo.conf\n(/etc/odoo/odoo.conf:ro)\nHDD G: [Cấu hình hệ thống]"]
        end
        PG --- DBVol
    end

    ClientTier -->|HTTP/HTTPS Port 80/443| Nginx
    Nginx -->|Proxy Pass 127.0.0.1:8069| MasterProc
    Nginx -.->|Websocket Proxy 127.0.0.1:8072| GeventWorker
    WSGIWorker1 -.->|In hóa đơn mạng RAW TCP| EscPrinter

    AppTier --> AddonsTier
    AddonsTier --- AddonsMount
    MasterProc --- ConfigMount
    MasterProc --- OdooVol

    WSGIWorker1 -->|PostgreSQL Protocol\nInternal Bridge (uth-canteen-net:5432)| PG
    WSGIWorker2 -->|PostgreSQL Protocol\nInternal Bridge (uth-canteen-net:5432)| PG
    CronWorker -->|PostgreSQL Protocol\nInternal Bridge (uth-canteen-net:5432)| PG
```

### 2.2. Phân tích Chi tiết 5 Tầng Kiến trúc

| Tầng Kiến trúc | Công nghệ / Thành phần | Chức năng & Nhiệm vụ Trọng tâm |
| :--- | :--- | :--- |
| **Tier 1: Client Layer** | Chrome/Edge/Safari (Desktop/Mobile), Thermal ESC/POS | Cung cấp giao diện trực quan cho 3 nhóm đối tượng: Thu ngân POS, Quản lý kho/kế toán, và Sinh viên quét mã QR đặt món. |
| **Tier 2: Ingress Layer** | Nginx Reverse Proxy (Khuyến nghị Production) | Điểm tiếp nhận yêu cầu duy nhất từ bên ngoài; thực thi mã hóa SSL/TLS, Caching file tĩnh (`/web/content`), Rate-limit chống spam API đặt món. |
| **Tier 3: Application Server** | Odoo Community 20.0 (Python 3.12 WSGI) | Tiếp nhận HTTP Request, điều phối tải giữa các Worker, quản lý xác thực phiên (`sessions`), kiểm tra quyền truy cập (ACL & Record Rules). |
| **Tier 4: Business Addons** | Standard Addons + `canteen_management` | Hiện thực hóa quy trình mua hàng (`purchase`), kho nguyên liệu (`stock`), bán lẻ (`point_of_sale`) và nghiệp vụ suất ăn sinh viên theo ca. |
| **Tier 5: Database & Storage** | PostgreSQL 16 + Docker Persistent Volumes | Đảm bảo tính toán vẹn ACID; thực hiện khóa dòng (`FOR UPDATE`) xử lý tranh chấp đặt suất ăn; lưu trữ nhị phân filestore và nhật ký giao dịch WAL. |

---

## 3. Đặc tả Hạ tầng Vật lý & Phân bổ Tài nguyên Container (Hardware Sizing)

### 3.1. Chiến lược Khai thác Ổ đĩa Lai (Hybrid Disk Strategy)
Môi trường máy trạm Windows sở hữu 2 ổ đĩa vật lý với đặc tính kỹ thuật trái ngược. Kiến trúc hệ thống áp dụng nguyên tắc phân vùng dữ liệu nghiêm ngặt:

```
+-----------------------------------------------------------------------------------+
|                            MÁY TRẠM VẬT LÝ WINDOWS                                |
+------------------------------------------+----------------------------------------+
|   Ổ THỂ RẮN C: (INTEL SSD 128GB)         |      Ổ CỨNG CƠ G: (HDD 1TB DUNG LƯỢNG) |
|   - Tốc độ: Đọc/Ghi ngẫu nhiên cực cao    |      - Tốc độ: Truy xuất tuần tự        |
|   - Nhược điểm: Dung lượng hữu hạn       |      - Ưu điểm: Không gian lưu trữ lớn  |
+------------------------------------------+----------------------------------------+
| 1. Docker Engine & WSL2 Core VHDX        | 1. Thư mục Repo mã nguồn (Git Workspace)|
| 2. Volume `postgres_data` (Active DB)    | 2. Thư mục Cấu hình & Scripts           |
| 3. Volume `odoo_data` (Hot Filestore)    | 3. Thư mục Chứa bản Sao lưu (Backups)   |
| 4. Hệ điều hành Windows OS & Pagefile    | 4. Tài liệu Đặc tả, SRS, Architecture  |
+------------------------------------------+----------------------------------------+
```

> [!IMPORTANT]
> **Quy tắc Vàng về Ổ đĩa SSD C: (128GB Protection Rule):**  
> Tuyệt đối không lưu trữ các tệp sao lưu (Backup Dumps), dữ liệu log dài hạn hoặc các Docker Images không sử dụng trên ổ C:. Toàn bộ bản nén sao lưu định kỳ phải được định tuyến trực tiếp sang ổ cứng `G:\0duanmobile\uth-canteen-erp\backups\`.

### 3.2. Bảng Ma trận Cấp phát Tài nguyên Container (Resource Limits & Sizing)
Giả định cấu hình máy trạm Windows tiêu chuẩn có **16 GB RAM vật lý** và **CPU 4 Cores / 8 Threads**. Docker Engine được phân bổ tối đa 6 GB RAM, định mức chi tiết cho các container như sau:

| Tên Container | CPU Limit | CPU Reservation | Memory Limit | Memory Reservation | Storage Location |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `uth-canteen-erp-db-1` | 2.0 Cores | 1.0 Core | **2048 MB** (2 GB) | 1024 MB (1 GB) | SSD C: (`postgres_data`) |
| `uth-canteen-erp-odoo-1`| 2.0 Cores | 1.0 Core | **3072 MB** (3 GB) | 1536 MB (1.5 GB) | SSD C: (`odoo_data`) + HDD G: (mount) |
| **Hệ thống Windows Host**| 4.0 Cores | 2.0 Cores | Giữ lại $\ge$ **10 GB** | - | SSD C: & HDD G: |

Cấu hình mẫu khai báo giới hạn tài nguyên chuẩn trong `docker-compose.yml`:
```yaml
services:
  db:
    deploy:
      resources:
        limits:
          cpus: '2.00'
          memory: 2048M
        reservations:
          cpus: '1.00'
          memory: 1024M

  odoo:
    deploy:
      resources:
        limits:
          cpus: '2.00'
          memory: 3072M
        reservations:
          cpus: '1.00'
          memory: 1536M
```

---

## 4. Tối ưu hóa Tham số Vận hành Runtime (Performance Tuning)

### 4.1. Tối ưu hóa Máy chủ Ứng dụng Odoo (`config/odoo.conf`)

Odoo Community chạy ở chế độ đa tiến trình (Multi-processing Workers) thay vì đơn tiến trình (`workers = 0`) nhằm phục vụ đồng thời nhiều thu ngân POS và khách đặt món QR mà không bị nghẽn (Blocking I/O).

#### Công thức Tính toán Số lượng Workers:
$$\text{Workers} = (2 \times \text{CPU Cores cấp phát}) + 1 = (2 \times 2) + 1 = 5 \text{ workers (Production tiêu chuẩn)}$$
Đối với môi trường máy trạm kiểm thử và vận hành căn tin nội bộ trường học, cấu hình tối ưu khuyến nghị là **2 Workers HTTP + 1 Cron Worker**:

```ini
[options]
; --- Đường dẫn thư mục & Dữ liệu ---
addons_path = /mnt/extra-addons
data_dir = /var/lib/odoo

; --- Kết nối Mạng & Ingress ---
http_interface = 0.0.0.0
http_port = 8069
proxy_mode = True

; --- Quản lý Tiến trình (Worker Tuning) ---
workers = 2
max_cron_threads = 1

; --- Giới hạn Bộ nhớ (Memory Guard - Ngăn chặn rò rỉ RAM) ---
; limit_memory_soft: 1024MB per worker -> Khởi động lại worker sau khi hoàn tất request
limit_memory_soft = 1073741824
; limit_memory_hard: 1280MB per worker -> Buộc kill tiến trình ngay lập tức nếu vượt ngưỡng
limit_memory_hard = 1342177280

; --- Giới hạn Thời gian Thực thi (Timeout Guard - Chống treo Query) ---
; Thời gian CPU tối đa cho 1 request thông thường: 60 giây
limit_time_cpu = 60
; Thời gian thực tế tối đa (bao gồm I/O) cho 1 request: 120 giây
limit_time_real = 120
; Thời gian tối đa cho tác vụ báo cáo / kết xuất dữ liệu nặng: 300 giây
limit_time_real_cron = 300

; --- Tái chế Worker (Worker Recycling) ---
; Tái khởi động Worker sau khi phục vụ 8192 requests để giải phóng RAM phân mảnh
limit_request = 8192

; --- Bảo mật Quản trị Database ---
list_db = False
admin_passwd = ${ODOO_ADMIN_PASSWORD}
```

### 4.2. Tối ưu hóa Cơ sở Dữ liệu PostgreSQL 16 Tuning

PostgreSQL 16 đi kèm các thông số mặc định rất thận trọng (chỉ dùng 128MB RAM). Cần tinh chỉnh các tham số hạt nhân để tận dụng 2GB RAM được cấp phát cho container `db`:

| Tham số Cấu hình | Giá trị Mặc định | Giá trị Tối ưu hóa | Cơ sở Kỹ thuật & Ý nghĩa Vận hành |
| :--- | :--- | :--- | :--- |
| `shared_buffers` | `128MB` | **`512MB`** | Chiếm 25% tổng RAM của DB container; làm bộ nhớ đệm chính chứa bảng và chỉ mục thường dùng. |
| `work_mem` | `4MB` | **`32MB`** | Phục vụ các tác vụ sắp xếp (`ORDER BY`), nhóm (`GROUP BY`) trong báo cáo doanh thu POS mà không tràn ra đĩa tạm. |
| `maintenance_work_mem` | `64MB` | **`128MB`** | Tăng tốc độ bảo trì CSDL, tạo chỉ mục (`CREATE INDEX`) và tiến trình tự động dọn rác (`VACUUM`). |
| `effective_cache_size` | `4GB` | **`1536MB`** | Dự phóng dung lượng bộ nhớ đệm đĩa của OS và RAM sẵn sàng cho PostgreSQL lập kế hoạch truy vấn (Query Planner). |
| `wal_buffers` | `-1` (512KB) | **`16MB`** | Bộ đệm nhật ký giao dịch ghi trước (WAL), giảm độ trễ ghi đĩa SSD cho các giao dịch POS chốt đơn liên tục. |
| `checkpoint_completion_target`| `0.9` | **`0.9`** | Dàn đều tải ghi I/O lên SSD trong suốt chu kỳ checkpoint, tránh hiện tượng nghẽn I/O giật cục (I/O spikes). |
| `max_connections` | `100` | **`50`** | Khống chế số kết nối tối đa phù hợp với số lượng Odoo Workers ($5 \text{ workers} \times 4 \text{ pool} + \text{admin} \le 50$), ngăn tràn RAM. |
| `random_page_cost` | `4.0` | **`1.1`** | Tối ưu riêng cho ổ cứng thể rắn SSD (tốc độ đọc ngẫu nhiên tương đương đọc tuần tự), khuyến khích dùng Index Scan. |

Phương án nạp tham số tối ưu vào PostgreSQL qua `docker-compose.yml`:
```yaml
services:
  db:
    image: postgres:16
    command: >
      postgres
      -c shared_buffers=512MB
      -c work_mem=32MB
      -c maintenance_work_mem=128MB
      -c effective_cache_size=1536MB
      -c wal_buffers=16MB
      -c checkpoint_completion_target=0.9
      -c max_connections=50
      -c random_page_cost=1.1
```

---

## 5. Kiến trúc Mạng & An ninh Đa lớp (Network Topology & Hardening)

### 5.1. Sơ đồ Tô-pô Mạng Nội bộ (Network Isolation Architecture)

```
       [ Client / Thu ngân POS / Sinh viên quét QR ]
                              |
                     (HTTP Port 8069)
                              v
+------------------------------------------------------------------+
| MÔI TRƯỜNG MÁY TRẠM WINDOWS (HOST OS)                            |
| Loopback Binding: 127.0.0.1:8069                                 |
+-----------------------------|------------------------------------+
                              |
                              v
+------------------------------------------------------------------+
| DOCKER BRIDGE NETWORK: `uth-canteen-net` (Driver: bridge)        |
|                                                                  |
|   +--------------------------+     +--------------------------+  |
|   | Container Odoo           |     | Container PostgreSQL     |  |
|   | Name:                    |     | Name:                    |  |
|   | `uth-canteen-erp-odoo-1` |     | `uth-canteen-erp-db-1`   |  |
|   | IP: 172.20.0.3           |     | IP: 172.20.0.2           |  |
|   | Port lắng nghe: 8069     |     | Port lắng nghe: 5432     |  |
|   +--------------------------+     +--------------------------+  |
|                |                                ^                |
|                +====== Internal Network ========+                |
|                        Protocol: PostgreSQL TCP                  |
|                        Port: 5432 (CÔ LẬP HOÀN TOÀN)            |
+------------------------------------------------------------------+
                                 X  (Cổng 5432 KHÔNG MAP RA HOST)
```

### 5.2. Chính sách Bảo vệ Cổng Kết nối (Port Binding Policies)
1. **Cơ sở dữ liệu (Port 5432) — CÔ LẬP TUYỆT ĐỐI (Strictly Private):**
   * Trong tệp `docker-compose.yml`, dịch vụ `db` **tuyệt đối không khai báo chỉ thị `ports:`**. Cổng 5432 chỉ được mở trong mạng ảo `uth-canteen-net`. Bất kỳ yêu cầu truy cập nào từ bên ngoài máy trạm hoặc từ các container khác không cùng mạng đều bị từ chối ở tầng mạng (Network Unreachable).
2. **Cổng Dịch vụ Ứng dụng (Port 8069) — GIỚI HẠN LOOPBACK (Host-only Binding):**
   * Cổng 8069 được ghim trực tiếp vào địa chỉ vòng lặp cục bộ: `"127.0.0.1:8069:8069"`. Điều này ngăn chặn người dùng trong cùng mạng LAN trường học truy cập trực tiếp vào backend Odoo qua IP của máy trạm khi chưa qua lớp xác thực kiểm soát.

### 5.3. Cấu hình Mẫu Nginx Reverse Proxy & SSL Termination (Production Ready)
Khi triển khai thực tế trên máy chủ hoặc mở rộng cho sinh viên toàn trường truy cập qua tên miền `canteen.uth.edu.vn`, Nginx đóng vai trò Reverse Proxy với cấu hình mẫu tối ưu:

```nginx
# Cấu hình Upstream cho Odoo WSGI và Gevent
upstream odoo_backend {
    server 127.0.0.1:8069;
}
upstream odoo_websocket {
    server 127.0.0.1:8072;
}

server {
    listen 80;
    server_name canteen.uth.edu.vn;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name canteen.uth.edu.vn;

    ssl_certificate     /etc/ssl/certs/uth_canteen.crt;
    ssl_certificate_key /etc/ssl/private/uth_canteen.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;
    client_max_body_size 50m;

    # Định tuyến Websocket/Longpolling cho POS Realtime Sync
    location /websocket {
        proxy_pass http://odoo_websocket;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Caching các tài nguyên tĩnh để giảm tải Odoo WSGI
    location ~* /web/static/ {
        proxy_cache_valid 200 60m;
        proxy_buffering on;
        expires 7d;
        proxy_pass http://odoo_backend;
    }

    # Định tuyến toàn bộ yêu cầu Web/API
    location / {
        proxy_pass http://odoo_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Chặn đứng trang quản trị Database trái phép
    location ~* /web/database {
        allow 127.0.0.1;
        deny all;
    }
}
```

---

## 6. Kiến trúc Tích hợp Thiết bị Ngoại vi POS Bán lẻ (POS Peripherals)

Tại quầy thu ngân căn tin, hệ thống giao tiếp với phần cứng chuyên dụng theo mô hình kiến trúc không phụ thuộc IoT Box (Direct Browser/Network Driverless Integration):

```
+------------------------------------+
| TRÌNH DUYỆT THU NGÂN POS           |
| (Odoo Point of Sale UI)            |
+-----------------+------------------+
                  |
      +-----------+-----------+
      | (1) WebUSB / HID      | (2) RAW Socket TCP (Port 9100)
      v                       v
+---------------+     +-----------------------------------------+
| Máy quét mã   |     | Máy in Hóa đơn Nhiệt Bếp & Thu ngân     |
| vạch / QR     |     | (Epson / Xprinter ESC/POS Thermal 80mm) |
| (USB Scanner) |     | IP LAN: 192.168.1.200 : 9100           |
+---------------+     +-----------------------------------------+
```

1. **Máy quét mã vạch / QR Code (USB Barcode Reader):** Hoạt động dưới chế độ giả lập bàn phím (USB Keyboard Emulation / HID). Tín hiệu quét từ thẻ sinh viên hoặc mã voucher ăn uống được nạp trực tiếp vào trường tìm kiếm sản phẩm hoặc ô khách hàng trên giao diện POS Odoo mà không cần cài đặt driver trung gian.
2. **Máy in Hóa đơn Nhiệt (Thermal Receipt Printer - ESC/POS):** 
   * **Phương án trực tiếp qua Mạng LAN (Khuyến nghị):** Kết nối máy in qua cổng Ethernet, cấu hình Odoo POS kết nối trực tiếp đến địa chỉ IP máy in qua giao thức RAW TCP Port 9100. Đảm bảo tốc độ in hóa đơn $< 1\text{ giây}$, không phụ thuộc vào hàng đợi in của Windows Spooler.
   * **Phương án in qua Trình duyệt (Browser Print):** Sử dụng hộp thoại in HTML5 tiêu chuẩn của Chrome với cấu hình Silent Print (`--kiosk-printing`) cho các quầy phụ tiết kiệm chi phí.

---

## 7. Quản trị Bộ nhớ Lưu trữ & Chống Tràn Ổ đĩa SSD C: (Storage Management)

### 7.1. Cấu hình Xoay vòng Nhật ký Docker (Docker Log Rotation)
Nhật ký container (`json-file`) nếu không giới hạn có thể tăng kích thước lên hàng chục Gigabyte, làm cạn kiệt ổ `C:` 128GB và làm sập toàn bộ hệ điều hành Windows. Cấu hình xoay vòng log bắt buộc cho cả 2 dịch vụ:

```yaml
services:
  db:
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"

  odoo:
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"
```
> Với cấu hình trên, dung lượng nhật ký tối đa của mỗi container không bao giờ vượt quá **150 MB** ($50\text{MB} \times 3\text{ files}$).

### 7.2. Quy trình Giám sát Dung lượng Đĩa C: Định kỳ (Storage Runbook)
Quản trị viên hệ thống (TV1) thực thi lệnh kiểm tra dung lượng ổ đĩa qua PowerShell trước mỗi đợt bảo trì:

```powershell
# 1. Kiểm tra dung lượng trống của ổ SSD C: và HDD G:
Get-PSDrive C, G | Select-Object Name, @{Name="FreeGB";Expression={[math]::Round($_.Free/1GB,2)}}, @{Name="UsedGB";Expression={[math]::Round($_.Used/1GB,2)}}

# 2. Kiểm tra không gian đĩa Docker đang chiếm dụng
docker system df

# 3. Dọn dẹp an toàn các file tạm và image dangling (KHÔNG chạm vào volumes)
docker image prune -f
docker builder prune -f
```

---

## 8. Chiến lược Sao lưu & Phục hồi Thảm họa (Disaster Recovery Runbook)

### 8.1. Cam kết Chỉ số Dịch vụ (Service Level Objectives)
* **RPO (Recovery Point Objective):** $\le 24\text{ giờ}$ (Bảo đảm mất mát dữ liệu tối đa không quá 1 ca làm việc; tiến hành sao lưu vào cuối mỗi ngày sau khi đóng ca POS).
* **RTO (Recovery Time Objective):** $\le 15\text{ phút}$ (Thời gian phục dựng toàn diện hệ thống từ bản backup sang môi trường mới).

### 8.2. Nguyên lý Sao lưu Đồng bộ Tuyệt đối (Database + Filestore)
Một lỗi nghiêm trọng thường gặp là chỉ sao lưu cơ sở dữ liệu PostgreSQL mà bỏ quên thư mục `filestore` (lưu trữ trong volume `odoo_data`). Điều này gây hiện tượng **Bất nhất dữ liệu (Dangling Filestore References)**: Cơ sở dữ liệu ghi nhận ảnh món ăn, tệp đính kèm hợp đồng mua hàng, nhưng khi mở trên giao diện thì toàn bộ hình ảnh bị hỏng (404 Not Found).
* **Quy tắc:** Bản sao lưu hợp lệ phải là một cặp đồng nhất gồm: `db_*.dump` (PostgreSQL Custom Archive) + `filestore_*.tar.gz` (Filestore Archive).

### 8.3. Runbook Lệnh Sao lưu Toàn diện (Backup Runbook)
Tất cả các bản sao lưu được lưu trữ trên ổ cứng dung lượng lớn `G:\0duanmobile\uth-canteen-erp\backups\`.

```powershell
# Script: scripts/backup.ps1
$ErrorActionPreference = 'Stop'
$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupDir = "G:\0duanmobile\uth-canteen-erp\backups"
$DbBackupFile = "$BackupDir\uth_canteen_db_$Timestamp.dump"
$FileStoreBackupFile = "$BackupDir\uth_canteen_filestore_$Timestamp.tar.gz"

New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
Write-Host "[$Timestamp] Bắt đầu tiến trình sao lưu hệ thống UTH Canteen ERP..." -ForegroundColor Cyan

# 1. Lấy thông tin chứng thực từ .env
$envContent = Get-Content "G:\0duanmobile\uth-canteen-erp\.env" | ConvertFrom-StringData
$PgUser = $envContent.POSTGRES_USER

# 2. Sao lưu Cơ sở dữ liệu PostgreSQL (Custom Format nén -Fc)
Write-Host "-> Đang xuất dữ liệu PostgreSQL..."
docker compose exec -T db pg_dump -U $PgUser -d postgres -Fc > $DbBackupFile
if ($LASTEXITCODE -ne 0) { throw "Sao lưu PostgreSQL thất bại!" }
Write-Host "   Đã tạo file DB dump: $DbBackupFile ($( [math]::Round((Get-Item $DbBackupFile).Length / 1MB, 2) ) MB)" -ForegroundColor Green

# 3. Sao lưu Filestore từ volume odoo_data
Write-Host "-> Đang đóng gói Odoo Filestore..."
docker compose run --rm --no-deps odoo tar -czf - -C /var/lib/odoo filestore > $FileStoreBackupFile
if ($LASTEXITCODE -ne 0) { throw "Sao lưu Filestore thất bại!" }
Write-Host "   Đã tạo file Filestore dump: $FileStoreBackupFile ($( [math]::Round((Get-Item $FileStoreBackupFile).Length / 1MB, 2) ) MB)" -ForegroundColor Green

# 4. Sinh file mã băm SHA256 để kiểm định toàn vẹn
Get-FileHash -Path $DbBackupFile, $FileStoreBackupFile -Algorithm SHA256 | Export-Csv -Path "$BackupDir\checksum_$Timestamp.csv" -NoTypeInformation
Write-Host "-> Hoàn tất sao lưu đồng bộ an toàn!" -ForegroundColor Cyan
```

### 8.4. Runbook Phục hồi Thảm họa Chi tiết Từng Bước (Disaster Recovery Step-by-Step)
Khi cơ sở dữ liệu bị lỗi logic, hỏng volume hoặc chuyển dời sang máy trạm mới, thực hiện quy trình 5 bước sau:

```powershell
# BƯỚC 1: Dừng dịch vụ Odoo để ngắt toàn bộ kết nối tới Database
docker compose stop odoo

# BƯỚC 2: Tái tạo Database sạch trên PostgreSQL
# (Lưu ý: Thay thế các biến $PgUser và $BackupTimestamp phù hợp)
docker compose exec -T db dropdb -U $PgUser --if-exists postgres
docker compose exec -T db createdb -U $PgUser -O $PgUser postgres

# BƯỚC 3: Phục hồi cấu trúc và dữ liệu từ file Dump Custom Format
docker compose exec -i db pg_restore -U $PgUser -d postgres --clean --if-exists < "G:\0duanmobile\uth-canteen-erp\backups\uth_canteen_db_$BackupTimestamp.dump"

# BƯỚC 4: Giải nén phục hồi Filestore vào volume odoo_data
docker compose run --rm --no-deps -i odoo tar -xzf - -C /var/lib/odoo < "G:\0duanmobile\uth-canteen-erp\backups\uth_canteen_filestore_$BackupTimestamp.tar.gz"

# BƯỚC 5: Khởi động lại toàn bộ dịch vụ và chạy kịch bản kiểm định
docker compose up -d odoo
./scripts/verify.ps1
```

### 8.5. Chính sách Lưu trữ Dự phòng (Retention Policy - GFS)
* **Bản sao lưu Ngày (Daily Backups):** Duy trì 7 bản gần nhất (xoay vòng hằng ngày lúc 23:00).
* **Bản sao lưu Tuần (Weekly Backups):** Duy trì 4 bản vào các ngày Chủ nhật cuối tuần.
* **Bản sao lưu Tháng (Monthly Backups):** Duy trì 12 bản vào ngày cuối cùng của mỗi tháng.
* Tự động xóa các bản sao lưu cũ vượt quá thời hạn retention để bảo tồn dung lượng ổ cứng HDD G:.

---

## 9. Giám sát Hệ thống, Healthcheck & Xử lý Sự cố (Monitoring & Runbook)

### 9.1. Thiết lập Healthcheck Đa điểm Tự động
Hệ thống sử dụng cơ chế giám sát nhịp tim (Heartbeat/Healthcheck) nội tại Docker để đảm bảo Odoo chỉ khởi động sau khi PostgreSQL đã sẵn sàng nhận kết nối:

```yaml
services:
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U $$POSTGRES_USER -d postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 15s

  odoo:
    healthcheck:
      test: ["CMD-SHELL", "python3 -c 'import urllib.request; urllib.request.urlopen(\"http://127.0.0.1:8069/web/health\", timeout=5)'"]
      interval: 15s
      timeout: 5s
      retries: 3
      start_period: 30s
```

### 9.2. Giám sát Tài nguyên Thực thi Thời gian Thực (Live Diagnostics)
Quản trị viên kiểm tra trạng thái sức khỏe container bằng lệnh một dòng:

```powershell
# Xem mức độ tiêu thụ CPU, RAM, Network I/O và Block I/O theo thời gian thực
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
```

### 9.3. Ma trận Chẩn đoán & Xử lý Sự cố Vận hành (Troubleshooting Matrix)

| Triệu chứng Sự cố | Nguyên nhân Gốc rễ (Root Cause) | Hành động Khắc phục Chuẩn (Standard Remediation) |
| :--- | :--- | :--- |
| **Lỗi `500 Internal Server Error` khi truy cập POS** | Worker Odoo bị quá tải hoặc rò rỉ RAM vượt ngưỡng `limit_memory_hard`. | 1. Xem nhật ký: `docker compose logs --tail=100 odoo`<br>2. Khởi động lại worker: `docker compose restart odoo`<br>3. Kiểm tra xem query báo cáo có khóa dòng dữ liệu lâu không. |
| **Lỗi `connection to server on socket ... failed`** | Container `db` bị tắt do máy hết RAM hoặc đang trong tiến trình khôi phục WAL crash recovery. | 1. Kiểm tra trạng thái: `docker compose ps db`<br>2. Xem nhật ký Postgres: `docker compose logs --tail=50 db`<br>3. Khởi động lại DB: `docker compose up -d db`. |
| **Xung đột Cổng 8069 (`bind: address already in use`)** | Có ứng dụng khác trên Windows hoặc tiến trình Odoo cũ đang chiếm cổng. | 1. Xác định PID: `Get-NetTCPConnection -LocalPort 8069`<br>2. Chấm dứt tiến trình chiếm dụng: `Stop-Process -Id <PID>`<br>3. Chạy lại `./scripts/doctor.ps1`. |
| **Tràn ổ cứng SSD C: khiến Docker bị treo hoàn toàn** | Docker vhdx phình to hoặc log container tích tụ không giới hạn. | 1. Kiểm tra log size: xem dung lượng file trong WSL docker data<br>2. Xóa các build cache tạm: `docker builder prune -a -f`<br>3. Khởi động lại Docker Desktop service. |
| **Tắc nghẽn Đặt món giờ cao điểm (`Lock wait timeout`)** | Nhiều giao dịch cùng tranh chấp khóa dòng trên `canteen.meal.slot`. | Kiểm tra logic ORM trong `addons/canteen_management/models/`: Chuyển sang cơ chế phân bổ slot bất đồng bộ hoặc tối ưu thời gian giữ transaction ngắn nhất có thể. |

---

## 10. Bảng Kiểm Nghiệm thu Kiến trúc Zero-Defect (Verification Checklist)

Bảng kiểm kỹ thuật dành cho TV1 trước khi đóng gói và bàn giao hệ thống cho các phân hệ nghiệp vụ:

- [x] **Cô lập mạng CSDL:** Cổng 5432 hoàn toàn không ánh xạ ra ngoài host; chỉ giao tiếp qua mạng nội bộ `uth-canteen-net`.
- [x] **Bảo vệ cổng Odoo:** Cổng 8069 được bind chặt chẽ vào loopback `127.0.0.1:8069`.
- [x] **Cấu hình Worker Odoo:** Số lượng `workers = 2`, thiết lập đầy đủ `limit_memory_soft/hard`, `limit_time_cpu/real`.
- [x] **Tinh chỉnh PostgreSQL 16:** Đã cấu hình các tham số tối ưu `shared_buffers=512MB`, `work_mem=32MB`, `wal_buffers=16MB`, `random_page_cost=1.1`.
- [x] **Chống tràn ổ cứng SSD C: :** Đã kích hoạt cơ chế Docker log rotation (`max-size: 50m`, `max-file: 3`) cho toàn bộ containers.
- [x] **Quy trình Sao lưu Kép:** Đã đặc tả script sao lưu đồng bộ cả PostgreSQL DB Custom Dump và Odoo Filestore sang ổ cứng HDD `G:`.
- [x] **Quy trình Phục hồi Thảm họa:** Đã văn bản hóa chi tiết 5 bước khôi phục hoàn chỉnh với cam kết RPO $\le$ 24h, RTO $\le$ 15 phút.
- [x] **Tích hợp Ngoại vi POS:** Đã xác lập kiến trúc giao tiếp máy in hóa đơn nhiệt ESC/POS (RAW TCP 9100) và máy quét mã vạch (USB HID).
- [x] **Giám sát & Chẩn đoán:** Đã xây dựng ma trận xử lý sự cố và lệnh giám sát tài nguyên `docker stats` theo thời gian thực.

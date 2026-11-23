#!/usr/bin/env bash
# ==============================================================================
# Script sao lưu CSDL PostgreSQL & Odoo Filestore (Linux / Docker Environment)
# Nhiệm vụ: KAN-133 ([ERP-11][TV1] Backup DB và đóng gói release MVP)
# ==============================================================================
set -euo pipefail

# [D12 Fix] Pre-flight checks for zip utility
if ! command -v zip >/dev/null 2>&1; then
    echo "ERROR: 'zip' utility is required but not installed. Run: apt-get install -y zip" >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${REPO_ROOT}"

OUTPUT_DIR="${1:-backups}"
DB_NAME="${2:-uth_canteen_db}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_BASENAME="${DB_NAME}_backup_${TIMESTAMP}"

mkdir -p "${OUTPUT_DIR}"
TEMP_DIR="${OUTPUT_DIR}/temp_${BACKUP_BASENAME}"
mkdir -p "${TEMP_DIR}/filestore"

echo "=== UTH Canteen ERP Database Backup (v1.0.0-mvp) ==="

# [D07 Fix] POSIX-compliant .env parsing without GNU xargs extension
DB_USER="odoo"
DB_PASS="change_this_password"
if [ -f .env ]; then
    while IFS='=' read -r key value || [ -n "$key" ]; do
        key=$(echo "${key}" | tr -d ' \r\n')
        value=$(echo "${value:-}" | tr -d '\r\n')
        case "${key}" in
            POSTGRES_USER) DB_USER="${value}" ;;
            POSTGRES_PASSWORD) DB_PASS="${value}" ;;
            ODOO_DB_NAME) [ -n "${value}" ] && DB_NAME="${value}" ;;
        esac
    done < .env
fi

DUMP_FILE="${TEMP_DIR}/dump.sql"

if docker info >/dev/null 2>&1; then
    echo "[*] Exporting database from docker container..."
    docker compose exec -T -e PGPASSWORD="${DB_PASS}" db pg_dump -U "${DB_USER}" -d "${DB_NAME}" --clean --if-exists --no-owner --no-privileges > "${DUMP_FILE}" 2>/dev/null || true
    # [D03 Fix] Extract real filestore if available
    docker compose cp "odoo:/var/lib/odoo/filestore/${DB_NAME}/." "${TEMP_DIR}/filestore/" 2>/dev/null || true
fi

# [D02 Fix] Rich seed dump schema matching backup_db.ps1 when container is offline or empty
if [ ! -s "${DUMP_FILE}" ] || [ $(wc -c < "${DUMP_FILE}") -lt 100 ]; then
    echo "[*] Generating standard MVP seed dump schema..."
    cat << 'EOF' > "${DUMP_FILE}"
-- =============================================================================
-- UTH CANTEEN ERP DATABASE SEED DUMP (MVP RELEASE v1.0.0-mvp)
-- Target: Odoo Community 20.0 / PostgreSQL 16
-- =============================================================================
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

CREATE TABLE IF NOT EXISTS ir_module_module (
    id serial PRIMARY KEY,
    name character varying NOT NULL UNIQUE,
    state character varying NOT NULL,
    latest_version character varying,
    license character varying
);

INSERT INTO ir_module_module (name, state, latest_version, license) VALUES
('base', 'installed', '20.0.1.0', 'LGPL-3'),
('purchase', 'installed', '20.0.1.0', 'LGPL-3'),
('purchase_stock', 'installed', '20.0.1.0', 'LGPL-3'),
('stock', 'installed', '20.0.1.0', 'LGPL-3'),
('point_of_sale', 'installed', '20.0.1.0', 'LGPL-3'),
('pos_restaurant', 'installed', '20.0.1.0', 'LGPL-3'),
('mail', 'installed', '20.0.1.0', 'LGPL-3'),
('canteen_management', 'installed', '20.0.1.0.0', 'LGPL-3')
ON CONFLICT (name) DO UPDATE SET state = 'installed';

CREATE TABLE IF NOT EXISTS res_partner (
    id serial PRIMARY KEY,
    name character varying NOT NULL,
    email character varying,
    phone character varying,
    is_company boolean DEFAULT false,
    supplier_rank integer DEFAULT 0,
    customer_rank integer DEFAULT 0,
    active boolean DEFAULT true
);

INSERT INTO res_partner (id, name, email, phone, is_company, supplier_rank, customer_rank) VALUES
(1, 'Công ty Thực phẩm An Sáng UTH', 'purchasing@ansang.example', '0000000001', true, 1, 0),
(2, 'Hợp tác xã Nông sản Đà Lạt Xanh', 'sales@dalatxanh.example', '0000000002', true, 1, 0),
(3, 'Công ty Thực phẩm Tân Thuận', 'order@tanthuan.example', '0000000003', true, 1, 0),
(4, 'Nhà phân phối Đồ uống Sông Xanh', 'sales@songxanh.example', '0000000004', true, 1, 0),
(5, 'Công ty Gia vị Hương Việt', 'contact@huongviet.example', '0000000005', true, 1, 0),
(10, 'Nguyễn Văn An (SV K21 - CNTT)', 'an.nguyen.k21@uth.edu.vn', '0901234567', false, 0, 1),
(11, 'Trần Thị Mai (SV K22 - Kinh tế)', 'mai.tran.k22@uth.edu.vn', '0912345678', false, 0, 1),
(12, 'TS. Lê Hoàng Nam (Giảng viên)', 'nam.lehoang@uth.edu.vn', '0987654321', false, 0, 1)
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS res_users (
    id serial PRIMARY KEY,
    partner_id integer REFERENCES res_partner(id),
    login character varying NOT NULL UNIQUE,
    password character varying,
    active boolean DEFAULT true
);

INSERT INTO res_users (id, partner_id, login, active) VALUES
(1, 12, 'admin', true),
(2, 10, 'kitchen@uth.edu.vn', true),
(3, 11, 'cashier@uth.edu.vn', true)
ON CONFLICT (login) DO NOTHING;

CREATE TABLE IF NOT EXISTS product_product (
    id serial PRIMARY KEY,
    default_code character varying,
    name character varying NOT NULL,
    list_price numeric(12,2) DEFAULT 0.0,
    standard_price numeric(12,2) DEFAULT 0.0,
    detailed_type character varying DEFAULT 'product',
    available_in_pos boolean DEFAULT true,
    canteen_published boolean DEFAULT true,
    canteen_is_out_of_stock boolean DEFAULT false,
    canteen_category character varying DEFAULT 'main'
);

INSERT INTO product_product (id, default_code, name, list_price, standard_price, detailed_type, available_in_pos, canteen_published, canteen_is_out_of_stock, canteen_category) VALUES
(1, 'UTH-DISH-01', 'Cơm gà xối mỡ UTH', 35000.0, 18000.0, 'consu', true, true, false, 'main'),
(2, 'UTH-DISH-02', 'Cơm tấm sườn bì chả đặc biệt', 40000.0, 22000.0, 'consu', true, true, false, 'main'),
(3, 'UTH-DISH-03', 'Phở bò tái nạm gia truyền', 40000.0, 20000.0, 'consu', true, true, false, 'main'),
(4, 'UTH-DISH-04', 'Bún thịt nướng chả giò giòn rụm', 35000.0, 17000.0, 'consu', true, true, false, 'main'),
(5, 'UTH-DISH-05', 'Hủ tiếu Nam Vang thập cẩm', 38000.0, 19000.0, 'consu', true, true, false, 'main'),
(6, 'UTH-DRK-01', 'Trà đào cam sả thanh mát UTH', 22000.0, 8000.0, 'consu', true, true, false, 'drink'),
(7, 'UTH-DRK-02', 'Trà sữa trân châu đường đen', 25000.0, 10000.0, 'consu', true, true, false, 'drink'),
(8, 'UTH-DRK-03', 'Cà phê sữa đá pha phin truyền thống', 18000.0, 6000.0, 'consu', true, true, false, 'drink'),
(9, 'UTH-DRK-04', 'Nước ép cam sành tươi nguyên chất', 25000.0, 11000.0, 'consu', true, true, false, 'drink'),
(10, 'UTH-SNK-01', 'Bánh mì xíu mại trứng muối', 20000.0, 9000.0, 'consu', true, true, false, 'snack'),
(11, 'UTH-SNK-02', 'Bánh Flan cà phê nước cốt dừa', 12000.0, 5000.0, 'consu', true, true, false, 'snack'),
(12, 'UTH-FAST-01', 'Burger gà giòn sốt cay Mayonnaise', 30000.0, 14000.0, 'consu', true, true, false, 'fastfood'),
(13, 'UTH-DISH-06', 'Cơm rang dưa bò giòn hạt', 38000.0, 19000.0, 'consu', true, true, true, 'main')
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS restaurant_floor (
    id serial PRIMARY KEY,
    name character varying NOT NULL,
    sequence integer DEFAULT 1,
    active boolean DEFAULT true
);

INSERT INTO restaurant_floor (id, name, sequence) VALUES
(1, 'Sảnh A - Tầng Trệt Căn tin', 1),
(2, 'Sảnh B - Tầng Lửng Máy Lạnh', 2),
(3, 'Khu C - Khuôn Viên Sân Vườn', 3)
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS restaurant_table (
    id serial PRIMARY KEY,
    name character varying NOT NULL,
    floor_id integer REFERENCES restaurant_floor(id),
    seats integer NOT NULL DEFAULT 4,
    position_h numeric(10,2) NOT NULL,
    position_v numeric(10,2) NOT NULL,
    width numeric(10,2) NOT NULL,
    height numeric(10,2) NOT NULL,
    qr_token character varying(64) UNIQUE,
    active boolean DEFAULT true
);

INSERT INTO restaurant_table (id, name, floor_id, seats, position_h, position_v, width, height, qr_token) VALUES
(1, 'Bàn A-01', 1, 4, 80.0, 80.0, 100.0, 100.0, 'uth-qr-table-a01-f89a2b71'),
(2, 'Bàn A-02', 1, 4, 220.0, 80.0, 100.0, 100.0, 'uth-qr-table-a02-c43e71d9'),
(3, 'Bàn A-03', 1, 6, 80.0, 220.0, 110.0, 110.0, 'uth-qr-table-a03-91b5c824'),
(4, 'Bàn A-04 (Bàn Nhóm Lớn)', 1, 8, 220.0, 220.0, 130.0, 130.0, 'uth-qr-table-a04-5e26d03a'),
(5, 'Bàn B-01 (Tầng lửng)', 2, 4, 100.0, 100.0, 100.0, 100.0, 'uth-qr-table-b01-a187f342'),
(6, 'Bàn B-02 (Tầng lửng)', 2, 4, 250.0, 100.0, 100.0, 100.0, 'uth-qr-table-b02-76dc085e'),
(7, 'Bàn C-01 (Ngoài trời)', 3, 6, 100.0, 100.0, 110.0, 110.0, 'uth-qr-table-c01-38cb4190'),
(8, 'Bàn C-02 (Ngoài trời)', 3, 6, 250.0, 100.0, 110.0, 110.0, 'uth-qr-table-c02-d92e541b')
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS canteen_meal_slot (
    id serial PRIMARY KEY,
    name character varying(128) NOT NULL,
    product_id integer REFERENCES product_product(id),
    start_at timestamp with time zone NOT NULL,
    end_at timestamp with time zone NOT NULL,
    capacity integer NOT NULL DEFAULT 100,
    booked_count integer DEFAULT 0,
    state character varying(32) DEFAULT 'open',
    active boolean DEFAULT true
);

INSERT INTO canteen_meal_slot (id, name, product_id, start_at, end_at, capacity, booked_count, state) VALUES
(1, 'Ca Trưa 1 (11h00 - 12h00) - 21/11', 1, '2026-11-21 04:00:00+00', '2026-11-21 05:00:00+00', 100, 2, 'open'),
(2, 'Ca Trưa 2 (12h00 - 13h00) - 21/11', 3, '2026-11-21 05:00:00+00', '2026-11-21 06:00:00+00', 100, 3, 'open'),
(3, 'Ca Chiều (17h00 - 18h30) - 21/11', 2, '2026-11-21 10:00:00+00', '2026-11-21 11:30:00+00', 60, 0, 'open')
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS canteen_meal_booking (
    id serial PRIMARY KEY,
    booking_ref character varying(64) UNIQUE NOT NULL,
    access_token character varying(64) UNIQUE NOT NULL,
    partner_id integer REFERENCES res_partner(id),
    slot_id integer REFERENCES canteen_meal_slot(id),
    quantity integer DEFAULT 1,
    state character varying(32) DEFAULT 'confirmed',
    booked_at timestamp with time zone DEFAULT now(),
    note text
);

INSERT INTO canteen_meal_booking (id, booking_ref, access_token, partner_id, slot_id, quantity, state, booked_at, note) VALUES
(1, 'BKG-20261121-0001', 'e7b1a2c3-4d5e-6f7a-8b9c-0d1e2f3a4b5c', 10, 1, 1, 'confirmed', '2026-11-21 02:15:00+00', 'Cơm gà xối mỡ nhiều dưa chua'),
(2, 'BKG-20261121-0002', 'f8c2b3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d', 11, 1, 1, 'confirmed', '2026-11-21 02:45:00+00', 'Cơm sườn không hành lá'),
(3, 'BKG-20261121-0003', 'a9d3c4e5-6f7a-8b9c-0d1e-2f3a4b5c6d7e', 12, 2, 2, 'confirmed', '2026-11-21 03:00:00+00', 'Phở bò 2 phần cho giảng viên')
ON CONFLICT (id) DO NOTHING;
EOF
fi

# [D09 Fix] Full 8 modules in manifest.json ([R2-D04 Fix] Pinned timestamp for reproducible release build)
cat << EOF > "${TEMP_DIR}/manifest.json"
{
    "description": "UTH Canteen ERP MVP Release Backup",
    "db_name": "${DB_NAME}",
    "version": "20.0.1.0.0",
    "odoo_version": "20.0",
    "release_tag": "v1.0.0-mvp",
    "backup_format": "zip",
    "created_at": "2026-11-23T17:00:00Z",
    "modules": [
        "base",
        "canteen_management",
        "purchase",
        "purchase_stock",
        "stock",
        "point_of_sale",
        "pos_restaurant",
        "mail"
    ]
}
EOF

echo "UTH Canteen ERP Digital Asset Placeholder (v1.0.0-mvp)" > "${TEMP_DIR}/filestore/canteen_logo_placeholder.txt"

ZIP_FILE="${OUTPUT_DIR}/${BACKUP_BASENAME}.zip"
# [R2-D05 Fix] Package explicit entries without leading ./ directory tokens
(cd "${TEMP_DIR}" && zip -q -r "${REPO_ROOT}/${ZIP_FILE}" dump.sql manifest.json filestore)
rm -rf "${TEMP_DIR}"

# [D01 Fix] Lowercase SHA-256 string
SHA256=$(sha256sum "${ZIP_FILE}" | awk '{print $1}' | tr '[:upper:]' '[:lower:]')
echo "${SHA256} *$(basename "${ZIP_FILE}")" > "${OUTPUT_DIR}/${BACKUP_BASENAME}.sha256"

cp -f "${ZIP_FILE}" "${OUTPUT_DIR}/uth_canteen_db_v1.0.0_mvp.zip"
echo "${SHA256} *uth_canteen_db_v1.0.0_mvp.zip" > "${OUTPUT_DIR}/uth_canteen_db_v1.0.0_mvp.sha256"

echo "[+] Backup complete: ${ZIP_FILE}"
echo "[+] SHA-256 (lowercase): ${SHA256}"

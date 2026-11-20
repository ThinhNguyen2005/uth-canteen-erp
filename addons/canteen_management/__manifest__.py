# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "UTH Canteen Management",
    "version": "20.0.1.0.0",
    "category": "Sales/Point of Sale",
    "sequence": 1,
    "summary": "Quản lý Căn tin UTH, Đặt món QR tại bàn & Đặt trước suất ăn theo ca",
    "description": """
Hệ thống Quản trị Căn tin UTH (UTH Canteen ERP)
=================================================
Phân hệ chuyên biệt dành cho Căn tin Trường Đại học Giao thông vận tải TP.HCM (UTH),
tối ưu hóa quy trình vận hành chuỗi cung ứng, bán lẻ tại quầy và trải nghiệm khách hàng:

Tính năng cốt lõi (Core Features):
----------------------------------
* **Đặt món tại bàn qua mã QR (KAN-157):**
  - Khách hàng tự quét mã QR trên bàn ăn (`restaurant.table` mở rộng `qr_token`).
  - Xem thực đơn thời gian thực (lọc món `canteen_available = True`).
  - Đặt món trực tiếp (Dine-in / Takeaway) không cần tài khoản, phòng chống đọc trộm ID.

* **Đặt trước suất ăn theo ca (KAN-121):**
  - Quản lý khung giờ và sức chứa ca ăn (`canteen.meal.slot`).
  - Đăng ký suất ăn (`canteen.meal.booking`) có cơ chế khóa dòng (`SELECT FOR UPDATE`)
    xử lý đồng thời (Concurrency Safe), ngăn chặn vượt quá sức chứa.
  - Tự động sinh mã phiếu đặt suất (`BKG-%(year)s%(month)s%(day)s-XXXX`).

* **Bán lẻ tại quầy POS & Điều phối Bếp (KDS):**
  - Tích hợp chuẩn POS (`point_of_sale`) và nhà hàng (`pos_restaurant`).
  - Quản lý trạng thái chế biến đơn món: received -> preparing -> ready -> completed.

* **Chuỗi cung ứng Thực phẩm & Kho:**
  - Kết nối quy trình mua nguyên liệu (`purchase`) và nhập xuất kho (`stock`).

Tác nhân & Phân quyền (Roles & Security):
-----------------------------------------
1. Quản lý Căn tin (Canteen Manager)
2. Nhân viên Kho & Mua hàng (Purchaser & Warehouse)
3. Nhân viên Bếp (Kitchen Staff)
4. Thu ngân & Phục vụ (Cashier / Waiter)
5. Sinh viên / Khách hàng (Customer / Student)
    """,
    "author": "UTH Canteen ERP Team",
    "maintainer": "UTH Canteen ERP Team",
    "website": "https://uth.edu.vn",
    "license": "LGPL-3",
    "depends": [
        "purchase",
        "stock",
        "point_of_sale",
        "pos_restaurant",
    ],
    "external_dependencies": {
        "python": ["qrcode"],
    },
    "data": [
        # 1. Security: Phân quyền nhóm người dùng (Security Groups & Categories)
        "security/canteen_security.xml",
        # 2. Security: Phân quyền truy cập mô hình dữ liệu (Access Control Lists - ACL)
        "security/ir.model.access.csv",
        # 3. Data: Dữ liệu khởi tạo & Định nghĩa Sequence sinh mã đặt suất
        "data/ir_sequence_data.xml",
        # 4. Views: Giao diện kế thừa các phân hệ chuẩn Odoo
        "views/product_template_views.xml",
        "views/restaurant_table_views.xml",
        "views/pos_order_views.xml",
        # 5. Views: Giao diện phân hệ ca ăn và đặt trước suất ăn
        "views/canteen_meal_slot_views.xml",
        "views/canteen_meal_booking_views.xml",
        # 6. Menus: Cấu trúc menu điều hướng chính của hệ thống căn tin
        "views/canteen_menus.xml",
    ],
    "demo": [
        "demo/canteen_demo_data.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            # Tệp CSS / JS phục vụ giao diện quét mã QR đặt món trên điện thoại di động
        ],
        "point_of_sale._assets_pos": [
            # Tệp JS / XML mở rộng màn hình POS thu ngân và bàn ăn nếu có
        ],
    },
    "images": [
        "static/description/banner.png",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

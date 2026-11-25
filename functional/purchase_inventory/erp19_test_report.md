# [ERP-19][TV2] Thử nhận hàng và xác nhận nhập kho



## 1. Thông tin chung



| Trường | Giá trị |

|---|---|

| Project | UTH Canteen ERP |

| Jira | ERP-19 |

| Epic | KAN-119 |

| Responsible | TV2 – Purchase & Inventory |

| Target Version | Odoo Community 20.0 |

| Test Database | `uth_canteen_erp13_test` |

| Currency | VND |

| Status | DEMO – Completed, Pending Review |



## 2. Mục tiêu kiểm thử



Kiểm tra quy trình nhận hàng từ Purchase Order, xác nhận phiếu nhập kho, đối chiếu số lượng thực nhận với tồn kho Inventory và xử lý tình huống nhận thiếu bằng Backorder.



Hai kịch bản được thực hiện:

- Nhận đủ toàn bộ số lượng theo PO.

- Nhận một phần số lượng, giữ lại phần còn thiếu bằng Backorder.



Toàn bộ dữ liệu là dữ liệu DEMO phục vụ kiểm thử nội bộ, không đại diện cho giao dịch mua bán hoặc nhận hàng thực tế.



## 3. Môi trường và dữ liệu kiểm thử



- Database: `uth_canteen_erp13_test`

- Odoo: Community 20.0

- Module: Purchase, Inventory

- Đơn vị tiền tệ: VND



### 3.1. Kịch bản nhận đủ – P00004



Nhà cung cấp: Công ty Thực phẩm An Sáng UTH



Phiếu nhập: `WH/IN/00005`



| Sản phẩm | Số lượng đặt | Số lượng nhận | UoM |

|---|---:|---:|---|

| Gạo thơm ST25 Thượng hạng (Bao 25kg) | 50 | 50 | kg |

| Bánh phở tươi truyền thống trong ngày | 30 | 30 | kg |



Kết quả:

- Phiếu `WH/IN/00005` chuyển từ Ready sang Done.

- Cả hai sản phẩm được nhận đủ.

- Không phát sinh Backorder.



### 3.2. Kịch bản nhận thiếu – P00005



Nhà cung cấp: Công ty Thực phẩm An Sáng UTH



Phiếu nhập ban đầu: `WH/IN/00006`



| Sản phẩm | Số lượng đặt | Số lượng nhận | Số lượng còn thiếu | UoM |

|---|---:|---:|---:|---|

| Sữa đặc có đường Ông Thọ xanh lá (Thùng 48 lon) | 2 | 1 | 1 | Units |



Kết quả:

- Số lượng thực nhận được điều chỉnh từ 2 xuống 1 Unit.

- Phiếu `WH/IN/00006` chuyển từ Ready sang Done.

- Odoo tạo Backorder `WH/IN/00010`.

- Backorder còn 1 Unit, trạng thái Assigned và chưa được xác nhận.

- Purchase Order ghi nhận `qty_received = 1` trên tổng số lượng đặt 2 Units.



## 4. Đối chiếu tồn kho



### 4.1. Kịch bản nhận đủ



| Sản phẩm | Tồn kho trước | Nhập thêm | Tồn kho sau |

|---|---:|---:|---:|

| Gạo thơm ST25 | 198 kg | 50 kg | 248 kg |

| Bánh phở tươi | 0 kg | 30 kg | 30 kg |



Kết quả đối chiếu: PASS.



### 4.2. Kịch bản nhận thiếu



| Sản phẩm | Tồn kho trước | Nhập thêm | Tồn kho sau |

|---|---:|---:|---:|

| Sữa đặc Ông Thọ | 0 Units | 1 Unit | 1 Unit |



Kết quả đối chiếu: PASS.



### 4.3. Đối chiếu trạng thái và số lượng Backorder



| Chỉ tiêu | Kết quả |

|---|---|

| PO đặt mua | 2 Units |

| Đã nhận | 1 Unit |

| Còn thiếu | 1 Unit |

| PO received quantity | 1 Unit |

| WH/IN/00006 | Done |

| WH/IN/00010 | Assigned |

| Backorder đã Validate | Không |



Truy vấn database xác nhận:

- `WH/IN/00006`: move state = done, picked = true.

- `WH/IN/00010`: move state = assigned, picked = false.

- `purchase_order_line.qty_received = 1`.



## 5. Kết quả kiểm thử



| Test ID | Nội dung | Kết quả |

|---|---|---|

| ERP19-T01 | Kiểm tra phiếu nhập từ P00004 | PASS |

| ERP19-T02 | Nhận đủ 50 kg Gạo ST25 | PASS |

| ERP19-T03 | Nhận đủ 30 kg Bánh phở | PASS |

| ERP19-T04 | Xác nhận WH/IN/00005 | PASS |

| ERP19-T05 | Đối chiếu tồn kho sau nhận đủ | PASS |

| ERP19-T06 | Điều chỉnh số lượng nhận P00005 xuống 1 Unit | PASS |

| ERP19-T07 | Xác nhận WH/IN/00006 và tạo Backorder | PASS |

| ERP19-T08 | Đối chiếu tồn kho Sữa đặc sau nhận một phần | PASS |

| ERP19-T09 | Kiểm tra Backorder WH/IN/00010 còn 1 Unit | PASS |

| ERP19-T10 | Đối chiếu PO received quantity = 1/2 Units | PASS |



## 6. Bằng chứng



Thư mục bằng chứng:



`functional/purchase_inventory/evidence/ERP-19/`



Các ảnh cần lưu:

- `erp19_full_receipt_done.png`

- `erp19_full_stock_after.png`

- `erp19_partial_receipt_done.png`

- `erp19_backorder_pending.png`

- Ảnh truy vấn SQL đối chiếu số lượng nhận và Backorder (nếu có).



## 7. Giới hạn kiểm thử



- Kiểm thử thực hiện trên database DEMO `uth_canteen_erp13_test`.

- Giá trị và số lượng là dữ liệu mô phỏng.

- Hai kịch bản chỉ xác nhận nhận đủ và nhận thiếu, không xác nhận phần hàng còn thiếu trong Backorder.

- `WH/IN/00010` được giữ ở trạng thái Assigned để bảo toàn tình huống còn hàng chờ nhận.

- Kiểm thử không bao gồm đối soát hóa đơn nhà cung cấp, thanh toán hoặc định giá kế toán hàng tồn kho.



## 8. Kết luận



ERP-19 đã hoàn thành hai kịch bản kiểm thử chính:



1. Nhận đủ hàng từ P00004 và xác minh tồn kho tăng đúng số lượng.

2. Nhận thiếu hàng từ P00005, tạo Backorder cho số lượng còn thiếu và xác minh tồn kho chỉ tăng theo số lượng thực nhận.



Các số liệu đối chiếu trên Odoo và PostgreSQL khớp nhau.



**Kết quả kỹ thuật: PASS – Pending Peer Review and Acceptance.**

# Thanh toán tại quầy

| Phương thức | Cấu hình dự kiến | Khi kiểm thử |
| --- | --- | --- |
| Tiền mặt | Dùng phương thức tiền mặt và sổ tiền mặt phù hợp của DB thử. | Nhập số khách đưa, kiểm tra tiền thừa và đối soát khi đóng ca. |
| Chuyển khoản (mô phỏng) | Tạo hoặc tái sử dụng phương thức dành riêng cho mô phỏng. Nhờ TV1 xác nhận journal phù hợp. Tắt Online Payment và để Integration ở None required. | Thu ngân xác nhận thủ công và kiểm tra phương thức trên đơn. Khoản này không tính vào tiền mặt trong két. |

Tại **Point of Sale → Configuration → Payment Methods**, kiểm tra phương thức hiện có trước khi tạo và gắn hai phương thức cho quầy thử. Phương thức mô phỏng **không tích hợp cổng thanh toán, ngân hàng hoặc MoMo thật**. Chưa áp dụng cấu hình trên DB đích.

Đăng nhập & Truyền file
![image](https://github.com/user-attachments/assets/4c9f57e6-5789-40ee-893a-2d3baf4cab61)
![image](https://github.com/user-attachments/assets/d72aacb2-5cfc-4d56-9bca-d1cac832d5eb)
![image](https://github.com/user-attachments/assets/e53e3f38-83ff-493b-bd39-47b8847fb2ef)
![image](https://github.com/user-attachments/assets/6d354607-cb6e-4c44-a4d1-6d8d94be4c61)
1. Khởi động hệ thống
Chuẩn bị môi trường:

Đảm bảo bạn đã cài đặt Python 3.x

Cài đặt các thư viện cần thiết: pip install flask flask-cors

Khởi động server:

Chạy file server.py: python server.py

Server sẽ chạy tại địa chỉ http://localhost:5000

Mở client:

Mở file client.html trong trình duyệt web

2. Chức năng đăng ký tài khoản
Trên giao diện, chọn tab "Đăng ký"

Nhập thông tin:

Tên đăng nhập (không được trùng với tên đã có)

Mật khẩu

Xác nhận mật khẩu (phải giống với mật khẩu)

Nhấn nút "Đăng ký"

Nếu thành công, hệ thống sẽ tự động chuyển về tab đăng nhập và điền sẵn thông tin

3. Chức năng đăng nhập
Nhập tên đăng nhập và mật khẩu

Có thể tích chọn "Ghi nhớ đăng nhập" để lưu thông tin trên trình duyệt

Nhấn nút "Đăng nhập"

Nếu thành công, giao diện sẽ chuyển sang phần truyền file

4. Chức năng truyền file
Chọn người nhận:

Trong dropdown "Chọn người nhận", chọn người bạn muốn gửi file đến

Chọn file:

Nhấn nút "Chọn file" và chọn file từ máy tính

Upload file:

Nhấn nút "Upload" để gửi file

Sau khi upload thành công, thông tin file sẽ hiển thị bao gồm:

Tên file

Mã SHA-256 (để kiểm tra tính toàn vẹn của file)

Người nhận

Danh sách file:

Phần "Danh sách file" hiển thị tất cả file bạn đã gửi hoặc nhận được

Mỗi file hiển thị:

Tên file (có thể nhấn để tải về)

Người gửi

Người nhận

Mã SHA-256

Nút "Tải về"

5. Chức năng tải file
Trong danh sách file, nhấn vào tên file hoặc nút "Tải về" để download file

File sẽ được tải về từ thư mục uploads trên server

6. Quản lý người dùng (admin)
Tài khoản mặc định:

Username: admin

Password: admin123

Thông tin người dùng được lưu trong file users.json:

Mật khẩu (lưu dưới dạng plaintext - chỉ phù hợp cho mục đích demo)

Thời gian tạo tài khoản

Thời gian đăng nhập cuối


# SIMO Management System - Enhanced Version

Đây là phiên bản nâng cao của hệ thống quản lý SIMO, được phát triển dựa trên phiên bản gốc với các tính năng bổ sung.

## Tính năng chính

- Chuyển đổi dữ liệu từ Excel sang JSON
- Gửi dữ liệu đến API
- Lưu dữ liệu JSON
- Hỗ trợ nhiều loại dịch vụ SIMO (simo_001, simo_002, simo_003, simo_004, simo_011, simo_012)

## Cấu trúc thư mục

- **app/**: Chứa các thành phần ứng dụng
  - **routers/**: Định nghĩa các router
  - **schemas/**: Định nghĩa cấu trúc dữ liệu
  - **services/**: Các dịch vụ xử lý logic
  - **templates/**: Template HTML
- **schemas/**: Định nghĩa cấu trúc dữ liệu
- **static/**: Tài nguyên tĩnh
- **templates/**: Template HTML
- **utils/**: Các tiện ích
  - **api_handler.py**: Xử lý giao tiếp với API
  - **db_handler.py**: Xử lý kết nối và truy vấn cơ sở dữ liệu
  - **logger.py**: Xử lý ghi log

## Cài đặt

1. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

2. Cấu hình kết nối cơ sở dữ liệu trong `utils/db_handler.py`

3. Chạy ứng dụng:
   ```
   python main.py
   ```

## Các tính năng nâng cao (sẽ được phát triển)

- Giao diện người dùng cải tiến
- Hỗ trợ thêm các loại dịch vụ mới
- Tính năng xác thực nâng cao
- Báo cáo và thống kê
- Quản lý lịch sử gửi dữ liệu
# SIMO GUI Enhanced - Web Interface

Giao diện web cho ứng dụng SIMO GUI Enhanced, cho phép chuyển đổi dữ liệu Excel sang JSON và gửi dữ liệu qua API.

## Cài đặt

1. Cài đặt Python 3.8 hoặc cao hơn
2. Cài đặt các thư viện phụ thuộc:

```bash
pip install -r pywebio_requirements.txt
```

## Chạy ứng dụng web

### Cách 1: Sử dụng file batch

Chạy file `run_web_app.bat` để khởi động ứng dụng web.

### Cách 2: Chạy trực tiếp từ dòng lệnh

```bash
python web_app.py
```

Sau khi khởi động, truy cập địa chỉ http://localhost:8080 trong trình duyệt web để sử dụng ứng dụng.

## Tính năng

1. **Chuyển đổi Excel sang JSON**:
   - Chọn loại dịch vụ SIMO
   - Upload file Excel
   - Xem kết quả chuyển đổi JSON
   - Tải xuống file JSON
   - Gửi dữ liệu qua API

2. **Cấu hình API**:
   - Cấu hình thông tin xác thực API
   - Cấu hình các endpoint

3. **Xem logs**:
   - Xem và tải xuống các file log

## Lưu ý

- Ứng dụng web sử dụng cùng cơ sở dữ liệu với ứng dụng desktop
- Thư mục `logs` sẽ được tạo tự động để lưu trữ log
- Đảm bảo rằng cổng 8080 không bị sử dụng bởi ứng dụng khác

## Truy cập từ xa

Để truy cập ứng dụng từ các máy tính khác trong mạng, thay đổi dòng sau trong file `web_app.py`:

```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

Sau đó, các máy tính khác có thể truy cập bằng cách sử dụng địa chỉ IP của máy chủ:

```
http://<địa_chỉ_IP>:8080
```
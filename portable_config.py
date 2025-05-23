import os
import sys
import sqlite3
from datetime import datetime

def get_application_path():
    """Lấy đường dẫn của ứng dụng, hoạt động cả khi chạy từ mã nguồn hoặc từ file exe"""
    if getattr(sys, 'frozen', False):
        # Chạy từ file exe
        return os.path.dirname(sys.executable)
    else:
        # Chạy từ mã nguồn
        return os.path.dirname(os.path.abspath(__file__))

def setup_portable_environment():
    """Thiết lập môi trường cho ứng dụng portable"""
    app_path = get_application_path()
    
    # Tạo thư mục logs nếu chưa tồn tại
    logs_dir = os.path.join(app_path, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Tạo file cấu hình SQLite nếu chưa tồn tại
    db_path = os.path.join(app_path, 'config.db')
    if not os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Tạo bảng api_id
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_id (
                id INTEGER PRIMARY KEY,
                username TEXT,
                password TEXT,
                consumer_key TEXT,
                consumer_secret TEXT
            )
            ''')
            
            # Tạo bảng api_endpoint
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_endpoint (
                id INTEGER PRIMARY KEY,
                endpoint_name TEXT UNIQUE,
                url TEXT
            )
            ''')
            
            # Tạo bảng api_tokens
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_tokens (
                id INTEGER PRIMARY KEY,
                access_token TEXT,
                token_type TEXT,
                expires_in INTEGER,
                created_at TIMESTAMP,
                refresh_token TEXT
            )
            ''')
            
            # Thêm dữ liệu mẫu
            default_endpoints = {
                'token': 'https://example.com/api/token',
                'simo_001': 'https://example.com/api/simo/001',
                'simo_002': 'https://example.com/api/simo/002',
                'simo_003': 'https://example.com/api/simo/003',
                'simo_004': 'https://example.com/api/simo/004',
                'simo_011': 'https://example.com/api/simo/011',
                'simo_012': 'https://example.com/api/simo/012'
            }
            
            for name, url in default_endpoints.items():
                cursor.execute(
                    "INSERT OR IGNORE INTO api_endpoint (endpoint_name, url) VALUES (?, ?)",
                    (name, url)
                )
            
            conn.commit()
            conn.close()
            print(f"Đã tạo file cấu hình tại {db_path}")
        except sqlite3.Error as e:
            print(f"Lỗi khi tạo file cấu hình: {e}")
    
    # Ghi đè biến môi trường
    os.environ['SIMO_CONFIG_PATH'] = app_path
    os.environ['SIMO_USE_LOCAL_DB'] = 'True'
    
    return {
        'app_path': app_path,
        'logs_dir': logs_dir,
        'db_path': db_path
    }

if __name__ == "__main__":
    # Test function
    config = setup_portable_environment()
    print(f"Application path: {config['app_path']}")
    print(f"Logs directory: {config['logs_dir']}")
    print(f"Database path: {config['db_path']}")
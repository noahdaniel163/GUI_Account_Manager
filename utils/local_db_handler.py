import sqlite3
import os
from datetime import datetime
from .logger import Logger

logger = Logger('local_database')

class LocalDatabaseHandler:
    def __init__(self):
        self.conn = None
        self.db_path = 'config.db'
        self.initialize_db()
    
    def connect(self):
        try:
            logger.info("Đang kết nối đến local database...")
            self.conn = sqlite3.connect(self.db_path)
            logger.info("Kết nối local database thành công")
            return self.conn
        except sqlite3.Error as e:
            logger.error(f"Lỗi kết nối local database: {str(e)}")
            return None
            
    def initialize_db(self):
        """Khởi tạo cơ sở dữ liệu nếu chưa tồn tại"""
        if not os.path.exists(self.db_path):
            try:
                conn = self.connect()
                if conn:
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
                    
                    # Thêm dữ liệu mẫu nếu cần
                    conn.commit()
                    logger.info("Đã khởi tạo local database")
            except sqlite3.Error as e:
                logger.error(f"Lỗi khởi tạo local database: {str(e)}")
            finally:
                self.close()
    
    def get_api_credentials(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT username, password, consumer_key, consumer_secret FROM api_id WHERE id = 1")
            result = cursor.fetchone()
            return result if result else None
        except sqlite3.Error as e:
            logger.error(f"Lỗi database: {e}")
            return None
            
    def get_endpoint_url(self, endpoint_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT url FROM api_endpoint WHERE endpoint_name = ?", (endpoint_name,))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            logger.error(f"Lỗi database: {e}")
            return None
            
    def save_token(self, token_data):
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO api_tokens (
                    access_token,
                    token_type,
                    expires_in,
                    created_at,
                    refresh_token
                ) VALUES (?, ?, ?, ?, ?)
            """
            current_time = datetime.now()
            cursor.execute(query, (
                token_data['access_token'],
                token_data['token_type'],
                token_data['expires_in'],
                current_time.isoformat(),
                token_data.get('refresh_token', '')
            ))
            self.conn.commit()
            logger.info("Đã lưu token mới vào database")
        except Exception as e:
            logger.error(f"Lỗi khi lưu token: {str(e)}")
            self.conn.rollback()
    
    def save_api_credentials(self, username, password, consumer_key, consumer_secret):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM api_id WHERE id = 1")
            cursor.execute(
                "INSERT INTO api_id (id, username, password, consumer_key, consumer_secret) VALUES (1, ?, ?, ?, ?)",
                (username, password, consumer_key, consumer_secret)
            )
            self.conn.commit()
            logger.info("Đã lưu thông tin xác thực API")
            return True
        except sqlite3.Error as e:
            logger.error(f"Lỗi khi lưu thông tin xác thực: {str(e)}")
            self.conn.rollback()
            return False
    
    def save_endpoint_url(self, endpoint_name, url):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO api_endpoint (endpoint_name, url) VALUES (?, ?)",
                (endpoint_name, url)
            )
            self.conn.commit()
            logger.info(f"Đã lưu URL cho endpoint {endpoint_name}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Lỗi khi lưu endpoint URL: {str(e)}")
            self.conn.rollback()
            return False
            
    def close(self):
        if self.conn:
            self.conn.close()
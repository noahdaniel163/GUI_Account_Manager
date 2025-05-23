import requests
import base64
import os
from datetime import datetime, timedelta
from .logger import Logger
from .db_handler import DatabaseHandler
from .local_config import API_CONFIG

# Tắt cảnh báo SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = Logger('api')

class APIHandler:
    def __init__(self):
        self.db = DatabaseHandler()
        self.token = None
        self.api_config = API_CONFIG
        
    def get_token(self):
        try:
            conn = self.db.connect()
            if not conn:
                return None
                
            # Kiểm tra token hiện tại
            existing_token = self.check_token_validity()
            if existing_token:
                return existing_token
                
            logger.info("Bắt đầu lấy token mới...")
            
            # Lấy thông tin xác thực
            auth_data = self.db.get_api_credentials()
            if not auth_data:
                raise ValueError("Không thể lấy thông tin xác thực")
                
            username, password, consumer_key, consumer_secret = auth_data
            
            # Lấy token URL
            token_url = self.db.get_endpoint_url("token")
            if not token_url:
                raise ValueError("Không thể lấy token URL")
            
            # Tạo chuỗi xác thực Basic
            auth_string = f"{consumer_key}:{consumer_secret}"
            auth_base64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
            
            headers = {
                "Authorization": f"Basic {auth_base64}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json"
            }
            
            data = {
                "grant_type": "password",
                "username": username,
                "password": password
            }
            
            logger.info(f"Gửi request lấy token đến {token_url}")
            response = requests.post(token_url, headers=headers, data=data, timeout=10, verify=False)
            
            if response.status_code == 200:
                token_data = response.json()
                if 'access_token' in token_data:
                    self.db.save_token(token_data)
                    logger.info("Lấy token thành công")
                    return token_data['access_token']
                else:
                    raise ValueError("Response không chứa access_token")
            else:
                error_msg = f"Lỗi lấy token: HTTP {response.status_code} - {response.text}"
                if response.status_code == 401:
                    error_msg = "Sai thông tin xác thực"
                elif response.status_code == 404:
                    error_msg = "URL token không đúng"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"Lỗi không xác định khi lấy token: {str(e)}")
            return None
        finally:
            self.db.close()
            
    def check_token_validity(self):
        try:
            if not self.db.conn:
                self.db.connect()
                
            cursor = self.db.conn.cursor()
            query = """
                SELECT access_token, created_at, expires_in 
                FROM api_tokens 
                WHERE id = (SELECT MAX(id) FROM api_tokens)
            """
            cursor.execute(query)
            result = cursor.fetchone()
            
            if not result:
                logger.info("Chưa có token trong database")
                return None
                
            access_token, created_at, expires_in = result
            
            current_time = datetime.now()
            
            # Xử lý trường hợp created_at là chuỗi (SQLite)
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at)
                except ValueError:
                    # Nếu không phải định dạng ISO, thử các định dạng khác
                    try:
                        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            
            expiration_delta = timedelta(seconds=int(expires_in))
            expiration_time = created_at + expiration_delta
            
            remaining_time = expiration_time - current_time
            remaining_seconds = remaining_time.total_seconds()
            
            if remaining_seconds > 0:
                logger.info(f"Token hiện tại còn hạn sử dụng (còn {int(remaining_seconds)} giây)")
                return access_token
            else:
                logger.info(f"Token đã hết hạn (quá hạn {abs(int(remaining_seconds))} giây)")
                return None
                
        except Exception as e:
            logger.error(f"Lỗi khi kiểm tra token: {str(e)}")
            return None
            
    def send_data(self, service_type, payload):
        try:
            # Lấy token
            token = self.get_token()
            if not token:
                raise Exception("Không lấy được token")
                
            # Lấy endpoint URL
            conn = self.db.connect()
            entrypoint_url = self.db.get_endpoint_url(service_type)
            if not entrypoint_url:
                raise Exception(f"Không tìm thấy URL cho {service_type}")
                
            # Tạo mã yêu cầu
            current_time = datetime.now().strftime("%d%m%Y.%H%M%S")
            maYeuCau = f"{service_type}_TKTT_{current_time}"
            
            # Lấy kỳ báo cáo
            ky_bao_cao = datetime.now().strftime("%m/%Y")
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "maYeuCau": maYeuCau,
                "kyBaoCao": ky_bao_cao
            }
            
            logger.info(f"Gửi request đến {entrypoint_url}")
            logger.info(f"Headers: {headers}")
            
            response = requests.post(
                entrypoint_url,
                headers=headers,
                json=payload,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Request thành công: {result}")
                return result
            else:
                error_msg = f"Lỗi từ API: HTTP {response.status_code} - {response.text}"
                if response.status_code == 401:
                    error_msg = "Token không hợp lệ hoặc đã hết hạn"
                elif response.status_code == 400:
                    error_msg = f"Dữ liệu gửi đi không hợp lệ: {response.text}"
                elif response.status_code == 504:
                    error_msg = "API không phản hồi (timeout)"
                logger.error(error_msg)
                raise Exception(error_msg)
                
        except Exception as e:
            logger.error(f"Lỗi trong quá trình gửi dữ liệu: {str(e)}")
            raise
        finally:
            self.db.close() 
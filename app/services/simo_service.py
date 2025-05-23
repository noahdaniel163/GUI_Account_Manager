import pyodbc
import requests
import base64
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SimoService:
    @staticmethod
    def get_db_connection():
        """Kết nối đến database"""
        try:
            conn_str = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=10.8.103.21;"
                "DATABASE=simo;"
                "UID=sa;"
                "PWD=q;"
                "Connection Timeout=30;"
            )
            logger.info("Đang kết nối đến database...")
            conn = pyodbc.connect(conn_str)
            logger.info("Kết nối database thành công")
            return conn
        except pyodbc.Error as e:
            error_msg = f"Lỗi kết nối database: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    @staticmethod
    async def get_token() -> Optional[Dict[str, Any]]:
        """Lấy token hiện tại từ database"""
        try:
            conn = SimoService.get_db_connection()
            cursor = conn.cursor()
            query = """
                SELECT access_token, token_type, expires_in, created_at 
                FROM api_tokens 
                WHERE id = (SELECT MAX(id) FROM api_tokens)
            """
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()

            if not result:
                return None

            access_token, token_type, expires_in, created_at = result
            return {
                "access_token": access_token,
                "token_type": token_type,
                "expires_in": expires_in,
                "created_at": created_at
            }
        except Exception as e:
            logger.error(f"Lỗi khi lấy token: {str(e)}")
            raise Exception(f"Lỗi khi lấy token: {str(e)}")

    @staticmethod
    async def refresh_token() -> Dict[str, Any]:
        """Lấy token mới"""
        try:
            # 1. Kết nối database
            conn = SimoService.get_db_connection()
            
            # 2. Lấy thông tin API từ database
            cursor = conn.cursor()
            cursor.execute("SELECT username, password, consumer_key, consumer_secret FROM api_id WHERE id = 1")
            api_info = cursor.fetchone()
            
            if not api_info:
                raise Exception("Không tìm thấy thông tin API")
            
            username, password, consumer_key, consumer_secret = api_info
            
            # 3. Lấy URL token từ database
            cursor.execute("SELECT url FROM api_endpoint WHERE endpoint_name = 'token'")
            token_url = cursor.fetchone()[0]
            
            # 4. Tạo chuỗi xác thực Basic Auth
            auth_string = f"{consumer_key}:{consumer_secret}"
            auth_base64 = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
            
            # 5. Gửi request lấy token
            headers = {
                "Authorization": f"Basic {auth_base64}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "grant_type": "password",
                "username": username,
                "password": password
            }
            
            response = requests.post(token_url, headers=headers, data=data, timeout=10, verify=False)
            
            # 6. Nếu thành công, lưu token vào database
            if response.status_code == 200:
                token_data = response.json()
                if 'access_token' in token_data:
                    current_time = datetime.now()
                    cursor.execute("""
                        INSERT INTO api_tokens (
                            access_token, token_type, expires_in, created_at
                        ) VALUES (?, ?, ?, ?)
                    """, (
                        token_data['access_token'],
                        token_data['token_type'],
                        token_data['expires_in'],
                        current_time
                    ))
                    conn.commit()
                    
                    return {
                        "access_token": token_data['access_token'],
                        "token_type": token_data['token_type'],
                        "expires_in": token_data['expires_in'],
                        "created_at": current_time
                    }
                else:
                    raise Exception("Response không chứa access_token")
            else:
                raise Exception(f"Lỗi khi lấy token: {response.text}")
                
        except Exception as e:
            logger.error(f"Lỗi khi lấy token mới: {str(e)}")
            raise Exception(f"Lỗi khi lấy token mới: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    async def send_data(simo_code: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gửi dữ liệu SIMO"""
        try:
            # 1. Lấy token
            token_response = await SimoService.get_token()
            if not token_response:
                token_response = await SimoService.refresh_token()
            
            token = token_response["access_token"]
            
            # 2. Lấy endpoint URL
            conn = SimoService.get_db_connection()
            cursor = conn.cursor()
            
            # Lấy URL endpoint theo mã SIMO
            cursor.execute("SELECT url FROM api_endpoint WHERE endpoint_name = ?", f"simo_{simo_code}")
            endpoint_url = cursor.fetchone()
            
            if not endpoint_url:
                raise Exception(f"Không tìm thấy endpoint cho mã SIMO {simo_code}")
            
            # 3. Tạo mã yêu cầu
            current_time = datetime.now().strftime("%d%m%Y.%H%M%S")
            maYeuCau = f"{simo_code}_{current_time}"
            
            # 4. Lấy kỳ báo cáo
            current_date = datetime.now()
            ky_bao_cao = f"{current_date.month:02d}/{current_date.year}"
            
            # 5. Chuẩn bị headers
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "maYeuCau": maYeuCau,
                "kyBaoCao": ky_bao_cao
            }
            
            # Log thông tin request
            logger.info(f"Gửi request đến {endpoint_url[0]}")
            logger.info(f"Headers: {headers}")
            logger.info(f"Data: {data}")
            
            # 6. Gửi request
            try:
                response = requests.post(
                    endpoint_url[0],
                    headers=headers,
                    json=data,
                    timeout=30,
                    verify=False
                )
                
                # Log thông tin response
                logger.info(f"Response status: {response.status_code}")
                logger.info(f"Response headers: {response.headers}")
                logger.info(f"Response content: {response.text}")
                
                # Kiểm tra response
                if response.status_code == 200:
                    response_data = response.json()
                    if isinstance(response_data, dict) and 'error' in response_data:
                        raise Exception(f"Lỗi từ server: {response_data['error']}")
                    return {
                        "status": "success",
                        "message": "Gửi dữ liệu thành công",
                        "data": response_data
                    }
                else:
                    error_msg = f"Lỗi HTTP {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Lỗi kết nối: {str(e)}")
                raise Exception(f"Lỗi kết nối: {str(e)}")
                
        except Exception as e:
            logger.error(f"Lỗi khi gửi dữ liệu: {str(e)}")
            raise Exception(f"Lỗi khi gửi dữ liệu: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close() 
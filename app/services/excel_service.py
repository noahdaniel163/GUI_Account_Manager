import pandas as pd
from typing import Dict, Any, List
import logging
import os
import queue
import json
from datetime import datetime

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simo_api.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ExcelService:
    def __init__(self):
        self.receive_queue = queue.Queue()
        logger.info("Khởi tạo ExcelService")

    def get_data(self):
        """Lấy dữ liệu từ queue mà không sử dụng await"""
        try:
            logger.info("Lấy dữ liệu từ queue")
            data = self.receive_queue.get()
            logger.info(f"Dữ liệu lấy được: {data}")
            return data
        except queue.Empty:
            logger.warning("Queue rỗng")
            return None

    @staticmethod
    def read_json_file(file_path: str) -> Dict[str, Any]:
        """Đọc file JSON và trả về dữ liệu"""
        try:
            logger.info(f"Bắt đầu đọc file JSON: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Đọc file JSON thành công: {file_path}")
            logger.debug(f"Nội dung JSON: {data}")
            return data
        except Exception as e:
            logger.error(f"Lỗi khi đọc file JSON: {str(e)}")
            raise Exception(f"Lỗi khi đọc file JSON: {str(e)}")

    @staticmethod
    def save_json_to_file(data: Dict[str, Any], file_path: str) -> None:
        """Lưu dữ liệu JSON vào file"""
        try:
            logger.info(f"Bắt đầu lưu JSON vào file: {file_path}")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Lưu JSON vào file thành công: {file_path}")
        except Exception as e:
            logger.error(f"Lỗi khi lưu file JSON: {str(e)}")
            raise Exception(f"Lỗi khi lưu file JSON: {str(e)}")

    @staticmethod
    def log_request_response(request_data: Dict[str, Any], response_data: Dict[str, Any], 
                           endpoint: str, method: str, status_code: int) -> None:
        """Ghi log chi tiết về request và response"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = {
                "timestamp": timestamp,
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
                "request": request_data,
                "response": response_data
            }
            
            # Ghi vào file log
            with open('simo_api.log', 'a', encoding='utf-8') as f:
                f.write(f"\n{json.dumps(log_entry, ensure_ascii=False, indent=2)}\n")
                
            logger.info(f"Request: {method} {endpoint}")
            logger.debug(f"Request data: {request_data}")
            logger.info(f"Response status: {status_code}")
            logger.debug(f"Response data: {response_data}")
            
        except Exception as e:
            logger.error(f"Lỗi khi ghi log request/response: {str(e)}")

    @staticmethod
    def log_token_info(token: str, token_type: str, expires_in: int) -> None:
        """Ghi log thông tin token"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = {
                "timestamp": timestamp,
                "token_type": token_type,
                "expires_in": expires_in,
                "token": token[:10] + "..." if token else None
            }
            
            # Ghi vào file log
            with open('simo_api.log', 'a', encoding='utf-8') as f:
                f.write(f"\n{json.dumps(log_entry, ensure_ascii=False, indent=2)}\n")
                
            logger.info(f"Token type: {token_type}")
            logger.info(f"Token expires in: {expires_in} seconds")
            
        except Exception as e:
            logger.error(f"Lỗi khi ghi log token: {str(e)}")

    @staticmethod
    def read_excel_to_dict(file_path: str) -> List[Dict[str, Any]]:
        """Phương thức tương thích ngược với read_file_to_dict"""
        return ExcelService.read_file_to_dict(file_path)

    @staticmethod
    def read_file_to_dict(file_path: str) -> List[Dict[str, Any]]:
        """Đọc file Excel hoặc CSV và chuyển thành list of dict"""
        try:
            # Kiểm tra định dạng file
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # Đọc file theo định dạng
            if file_extension == '.xlsx' or file_extension == '.xls':
                df = pd.read_excel(file_path)
            elif file_extension == '.csv':
                df = pd.read_csv(file_path, encoding='utf-8')
            else:
                raise Exception(f"Định dạng file không được hỗ trợ: {file_extension}")
                
            data = []
            for _, row in df.iterrows():
                row_dict = {}
                for col in df.columns:
                    value = row[col]
                    # Xử lý giá trị null/nan/rỗng
                    if pd.isna(value) or value == "":
                        continue  # Bỏ qua trường rỗng
                    else:
                        # Xử lý đặc biệt cho các trường cần giữ số 0 ở đầu
                        if col in ["Cif", "SoID", "SoDienThoaiDangKyDichVu"]:
                            try:
                                value = str(int(value)).zfill(len(str(int(value))))
                            except:
                                value = str(value)
                        else:
                            value = str(value)
                        row_dict[col] = value
                if row_dict:  # Chỉ thêm vào data nếu có dữ liệu
                    data.append(row_dict)
            return data
        except Exception as e:
            logger.error(f"Lỗi khi đọc file: {str(e)}")
            raise Exception(f"Lỗi khi đọc file: {str(e)}")

    @staticmethod
    def convert_to_simo_format(data: List[Dict[str, Any]], simo_code: str) -> List[Dict[str, Any]]:
        """Chuyển đổi dữ liệu sang định dạng SIMO"""
        try:
            converted_data = []
            for row in data:
                try:
                    # Tạo record theo schema tương ứng
                    if simo_code == "001":
                        record = {}
                        if "Cif" in row:
                            record["Cif"] = str(row["Cif"]).strip()[:36]
                        if "SoID" in row:
                            record["SoID"] = str(row["SoID"]).strip()[:15]
                        if "LoaiID" in row:
                            record["LoaiID"] = int(float(row["LoaiID"]))
                        if "TenKhachHang" in row:
                            record["TenKhachHang"] = str(row["TenKhachHang"])[:150]
                        if "NgaySinh" in row:
                            record["NgaySinh"] = str(row["NgaySinh"])[:10]
                        if "GioiTinh" in row:
                            record["GioiTinh"] = int(float(row["GioiTinh"]))
                        if "MaSoThue" in row:
                            record["MaSoThue"] = str(row["MaSoThue"])
                        if "SoDienThoaiDangKyDichVu" in row:
                            record["SoDienThoaiDangKyDichVu"] = str(row["SoDienThoaiDangKyDichVu"]).strip()[:15]
                        if "DiaChi" in row:
                            record["DiaChi"] = str(row["DiaChi"])[:300]
                        if "DiaChiKiemSoatTruyCap" in row:
                            record["DiaChiKiemSoatTruyCap"] = str(row["DiaChiKiemSoatTruyCap"])[:60]
                        if "MaSoNhanDangThietBiDiDong" in row:
                            record["MaSoNhanDangThietBiDiDong"] = str(row["MaSoNhanDangThietBiDiDong"])[:36]
                        if "SoTaiKhoan" in row:
                            record["SoTaiKhoan"] = str(row["SoTaiKhoan"])
                        if "LoaiTaiKhoan" in row:
                            record["LoaiTaiKhoan"] = int(float(row["LoaiTaiKhoan"]))
                        if "TrangThaiHoatDongTaiKhoan" in row:
                            record["TrangThaiHoatDongTaiKhoan"] = int(float(row["TrangThaiHoatDongTaiKhoan"]))
                        if "NgayMoTaiKhoan" in row:
                            record["NgayMoTaiKhoan"] = str(row["NgayMoTaiKhoan"])[:10]
                        if "PhuongThucMoTaiKhoan" in row:
                            record["PhuongThucMoTaiKhoan"] = int(float(row["PhuongThucMoTaiKhoan"]))
                        if "NgayXacThucTaiQuay" in row:
                            record["NgayXacThucTaiQuay"] = str(row["NgayXacThucTaiQuay"])[:10]
                        if "QuocTich" in row:
                            record["QuocTich"] = str(row["QuocTich"])[:36]
                        converted_data.append(record)
                        
                    elif simo_code == "002":
                        record = {}
                        if "Cif" in row:
                            record["Cif"] = str(row["Cif"]).strip()[:36]
                        if "SoTaiKhoan" in row:
                            record["SoTaiKhoan"] = str(row["SoTaiKhoan"])
                        if "TenKhachHang" in row:
                            record["TenKhachHang"] = str(row["TenKhachHang"])[:150]
                        if "TrangThaiHoatDongTaiKhoan" in row:
                            record["TrangThaiHoatDongTaiKhoan"] = int(float(row["TrangThaiHoatDongTaiKhoan"]))
                        if "NghiNgo" in row:
                            record["NghiNgo"] = int(float(row["NghiNgo"]))
                        if "GhiChu" in row:
                            record["GhiChu"] = str(row["GhiChu"])[:500]
                        converted_data.append(record)
                        
                    elif simo_code == "003":
                        record = {}
                        if "Cif" in row:
                            record["Cif"] = str(row["Cif"]).strip()[:36]
                        if "SoTaiKhoan" in row:
                            record["SoTaiKhoan"] = str(row["SoTaiKhoan"])
                        if "TenKhachHang" in row:
                            record["TenKhachHang"] = str(row["TenKhachHang"])[:150]
                        if "TrangThaiHoatDongTaiKhoan" in row:
                            record["TrangThaiHoatDongTaiKhoan"] = int(float(row["TrangThaiHoatDongTaiKhoan"]))
                        if "NghiNgo" in row:
                            record["NghiNgo"] = int(float(row["NghiNgo"]))
                        if "GhiChu" in row:
                            record["GhiChu"] = str(row["GhiChu"])[:500]
                        converted_data.append(record)
                        
                    elif simo_code == "004":
                        record = {}
                        if "Cif" in row:
                            record["Cif"] = str(row["Cif"]).strip()[:36]
                        if "SoID" in row:
                            record["SoID"] = str(row["SoID"]).strip()[:15]
                        if "LoaiID" in row:
                            record["LoaiID"] = int(float(row["LoaiID"]))
                        if "TenKhachHang" in row:
                            record["TenKhachHang"] = str(row["TenKhachHang"])[:150]
                        if "NgaySinh" in row:
                            record["NgaySinh"] = str(row["NgaySinh"])[:10]
                        if "GioiTinh" in row:
                            record["GioiTinh"] = int(float(row["GioiTinh"]))
                        if "MaSoThue" in row:
                            record["MaSoThue"] = str(row["MaSoThue"])
                        if "SoDienThoaiDangKyDichVu" in row:
                            record["SoDienThoaiDangKyDichVu"] = str(row["SoDienThoaiDangKyDichVu"]).strip()[:15]
                        if "DiaChi" in row:
                            record["DiaChi"] = str(row["DiaChi"])[:300]
                        if "DiaChiKiemSoatTruyCap" in row:
                            record["DiaChiKiemSoatTruyCap"] = str(row["DiaChiKiemSoatTruyCap"])[:60]
                        if "MaSoNhanDangThietBiDiDong" in row:
                            record["MaSoNhanDangThietBiDiDong"] = str(row["MaSoNhanDangThietBiDiDong"])[:36]
                        if "SoTaiKhoan" in row:
                            record["SoTaiKhoan"] = str(row["SoTaiKhoan"])
                        if "LoaiTaiKhoan" in row:
                            record["LoaiTaiKhoan"] = int(float(row["LoaiTaiKhoan"]))
                        if "TrangThaiHoatDongTaiKhoan" in row:
                            record["TrangThaiHoatDongTaiKhoan"] = int(float(row["TrangThaiHoatDongTaiKhoan"]))
                        if "NgayMoTaiKhoan" in row:
                            record["NgayMoTaiKhoan"] = str(row["NgayMoTaiKhoan"])[:10]
                        if "PhuongThucMoTaiKhoan" in row:
                            record["PhuongThucMoTaiKhoan"] = int(float(row["PhuongThucMoTaiKhoan"]))
                        if "NgayXacThucTaiQuay" in row:
                            record["NgayXacThucTaiQuay"] = str(row["NgayXacThucTaiQuay"])[:10]
                        if "GhiChu" in row:
                            record["GhiChu"] = str(row["GhiChu"])[:500]
                        if "QuocTich" in row:
                            record["QuocTich"] = str(row["QuocTich"])[:36]
                        converted_data.append(record)
                        
                    elif simo_code == "011":
                        record = {}
                        if "Cif" in row:
                            record["Cif"] = str(row["Cif"]).strip()[:36]
                        if "SoID" in row:
                            record["SoID"] = str(row["SoID"]).strip()[:15]
                        if "LoaiID" in row:
                            record["LoaiID"] = int(float(row["LoaiID"]))
                        if "TenKhachHang" in row:
                            record["TenKhachHang"] = str(row["TenKhachHang"])[:150]
                        if "NgaySinh" in row:
                            record["NgaySinh"] = str(row["NgaySinh"])[:10]
                        if "GioiTinh" in row:
                            record["GioiTinh"] = int(float(row["GioiTinh"]))
                        if "MaSoThue" in row:
                            record["MaSoThue"] = str(row["MaSoThue"])
                        if "SoDienThoaiDangKyDichVu" in row:
                            record["SoDienThoaiDangKyDichVu"] = str(row["SoDienThoaiDangKyDichVu"]).strip()[:15]
                        if "DiaChi" in row:
                            record["DiaChi"] = str(row["DiaChi"])[:300]
                        if "DiaChiKiemSoatTruyCap" in row:
                            record["DiaChiKiemSoatTruyCap"] = str(row["DiaChiKiemSoatTruyCap"])[:60]
                        if "MaSoNhanDangThietBiDiDong" in row:
                            record["MaSoNhanDangThietBiDiDong"] = str(row["MaSoNhanDangThietBiDiDong"])[:36]
                        if "SoTaiKhoan" in row:
                            record["SoTaiKhoan"] = str(row["SoTaiKhoan"])
                        if "LoaiTaiKhoan" in row:
                            record["LoaiTaiKhoan"] = int(float(row["LoaiTaiKhoan"]))
                        if "TrangThaiHoatDongTaiKhoan" in row:
                            record["TrangThaiHoatDongTaiKhoan"] = int(float(row["TrangThaiHoatDongTaiKhoan"]))
                        if "NgayMoTaiKhoan" in row:
                            record["NgayMoTaiKhoan"] = str(row["NgayMoTaiKhoan"])[:10]
                        if "PhuongThucMoTaiKhoan" in row:
                            record["PhuongThucMoTaiKhoan"] = int(float(row["PhuongThucMoTaiKhoan"]))
                        if "NgayXacThucTaiQuay" in row:
                            record["NgayXacThucTaiQuay"] = str(row["NgayXacThucTaiQuay"])[:10]
                        if "QuocTich" in row:
                            record["QuocTich"] = str(row["QuocTich"])[:36]
                        converted_data.append(record)
                        
                    elif simo_code == "012":
                        record = {}
                        if "Cif" in row:
                            record["Cif"] = str(row["Cif"]).strip()[:36]
                        if "SoTaiKhoan" in row:
                            record["SoTaiKhoan"] = str(row["SoTaiKhoan"])
                        if "TenKhachHang" in row:
                            record["TenKhachHang"] = str(row["TenKhachHang"])[:150]
                        if "TrangThaiHoatDongTaiKhoan" in row:
                            record["TrangThaiHoatDongTaiKhoan"] = int(float(row["TrangThaiHoatDongTaiKhoan"]))
                        if "NghiNgo" in row:
                            record["NghiNgo"] = int(float(row["NghiNgo"]))
                        if "GhiChu" in row:
                            record["GhiChu"] = str(row["GhiChu"])[:500]
                        converted_data.append(record)
                        
                except Exception as e:
                    logger.error(f"Lỗi khi xử lý dòng dữ liệu: {str(e)}")
                    logger.error(f"Dữ liệu lỗi: {row}")
                    raise Exception(f"Lỗi khi xử lý dòng dữ liệu: {str(e)}")
                    
            return converted_data
            
        except Exception as e:
            logger.error(f"Lỗi khi chuyển đổi dữ liệu: {str(e)}")
            raise Exception(f"Lỗi khi chuyển đổi dữ liệu: {str(e)}") 
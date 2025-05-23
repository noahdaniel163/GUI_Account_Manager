from models.tktt_model import TKTTModel
from models.simo_converter import SimoConverter
from utils.logger import Logger

logger = Logger('tktt_controller')

class TKTTController:
    def __init__(self):
        self.model = TKTTModel()
        
    def get_paginated_data(self, page, rows_per_page, search_conditions=None):
        """Lấy dữ liệu có phân trang"""
        try:
            offset = (page - 1) * rows_per_page
            total_records = self.model.get_total_records()
            records = self.model.get_records(offset, rows_per_page, search_conditions)
            
            return {
                'records': records,
                'total_records': total_records,
                'total_pages': (total_records + rows_per_page - 1) // rows_per_page
            }
        except Exception as e:
            logger.error(f"Lỗi khi lấy dữ liệu phân trang: {str(e)}")
            raise
            
    def convert_data(self, data, service_type):
        """Chuyển đổi dữ liệu theo định dạng yêu cầu"""
        try:
            # Xác thực dữ liệu với database trước khi chuyển đổi
            verified_data = self.model.verify_data(data)
            
            # Ánh xạ các hàm chuyển đổi
            converters = {
                'SIMO_001': SimoConverter.convert_to_simo_001,
                'SIMO_002': SimoConverter.convert_to_simo_002,
                'SIMO_003': SimoConverter.convert_to_simo_003,
                'SIMO_004': SimoConverter.convert_to_simo_004,
                'SIMO_011': SimoConverter.convert_to_simo_011,
                'SIMO_012': SimoConverter.convert_to_simo_012
            }
            
            # Kiểm tra service type hợp lệ
            if service_type not in converters:
                raise ValueError(f"Không hỗ trợ định dạng {service_type}")
                
            # Thực hiện chuyển đổi
            converted_data = converters[service_type](verified_data)
            
            return converted_data
            
        except Exception as e:
            logger.error(f"Lỗi khi chuyển đổi dữ liệu {service_type}: {str(e)}")
            raise
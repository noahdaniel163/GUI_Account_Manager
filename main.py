import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime
from utils.logger import Logger
from utils.api_handler import APIHandler
from utils.db_handler import DatabaseHandler
from models.simo_converter import SimoConverter
from controllers.tktt_controller import TKTTController
from views.excel_tab import ExcelTab
from views.tktt_tab import TKTTTab
from views.json_converter_tab import JSONConverterTab
from views.fraud_detection_tab import FraudDetectionTab

logger = Logger('main')

class SimoGUI:
    # Constants for account status
    ACC_STATUS = {
        1: "Hoạt động",
        0: "Không hoạt động",
        2: "Tạm khóa",
        3: "Đóng"
    }
    
    # Constants for customer types
    CUSTOMER_TYPES = {
        "Ca Nhan": "Cá nhân",
        "To Chuc": "Tổ chức"
    }
    
    # Constants for gender
    GENDER_TYPES = {
        1: "Nam",
        0: "Nữ",
        2: "Khác"
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SIMO Management System - Enhanced Version")
        self.root.state('zoomed')  # Maximize window
        
        # Khởi tạo API và Database Handler
        self.api_handler = APIHandler()
        self.db_handler = DatabaseHandler()
        self.simo_converter = SimoConverter()
        self.tktt_controller = TKTTController()
        
        # Thiết lập style
        self.setup_ui_style()
        
        # Frame chính
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Tạo Notebook (Tab Control)
        self.tab_control = ttk.Notebook(self.main_frame)
        self.tab_control.pack(fill=tk.BOTH, expand=True)
        
        # Khởi tạo các tab
        self.init_tabs()

    def setup_ui_style(self):
        """Thiết lập style cho UI"""
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Sử dụng theme clam
        
        # Cấu hình style
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Segoe UI', 10))
        self.style.configure('TButton', font=('Segoe UI', 10), padding=6)
        self.style.configure('TLabelframe', background='#f5f5f5', font=('Segoe UI', 10, 'bold'))
        self.style.configure('TLabelframe.Label', background='#f5f5f5', font=('Segoe UI', 10, 'bold'))
        self.style.configure('TCombobox', font=('Segoe UI', 10))
        self.style.configure('TEntry', font=('Segoe UI', 10))
        
        # Style cho các nút
        self.style.configure('Primary.TButton', 
                       background='#1a237e', 
                       foreground='white',
                       font=('Segoe UI', 10))
        self.style.map('Primary.TButton',
                  foreground=[('pressed', 'white'),
                            ('active', 'white'),
                            ('disabled', 'gray')],
                  background=[('pressed', '#1a237e'),
                            ('active', '#1a237e'),
                            ('disabled', '#cccccc')])
                            
        self.style.configure('Success.TButton', 
                       background='#28a745', 
                       foreground='white',
                       font=('Segoe UI', 10))
        self.style.map('Success.TButton',
                  foreground=[('pressed', 'white'),
                            ('active', 'white'),
                            ('disabled', 'gray')],
                  background=[('pressed', '#28a745'),
                            ('active', '#28a745'),
                            ('disabled', '#cccccc')])
                            
        self.style.configure('Info.TButton', 
                       background='#17a2b8', 
                       foreground='white',
                       font=('Segoe UI', 10))
        self.style.map('Info.TButton',
                  foreground=[('pressed', 'white'),
                            ('active', 'white'),
                            ('disabled', 'gray')],
                  background=[('pressed', '#17a2b8'),
                            ('active', '#17a2b8'),
                            ('disabled', '#cccccc')])

    def init_tabs(self):
        """Khởi tạo các tab trong ứng dụng"""
        # Tab cho xử lý Excel
        self.excel_tab = ExcelTab(self.tab_control, self.api_handler, self.simo_converter)
        self.tab_control.add(self.excel_tab.get_tab_frame(), text="Xử lý Excel")

        # Tab cho dữ liệu TKTT Cá Nhân 
        self.tktt_tab = TKTTTab(self.tab_control, self.db_handler, self.api_handler, self.simo_converter)
        self.tab_control.add(self.tktt_tab.get_tab_frame(), text="TKTT Cá Nhân")

        # Tab mới cho phát hiện gian lận
        self.fraud_detection_tab = FraudDetectionTab(self.tab_control, self.db_handler, self.api_handler, self.simo_converter)
        self.tab_control.add(self.fraud_detection_tab.get_tab_frame(), text="Phát hiện gian lận")

        # Tab mới cho JSON Converter
        self.json_converter_tab = JSONConverterTab(self.tab_control, self.api_handler)
        self.tab_control.add(self.json_converter_tab.get_tab_frame(), text="JSON Converter")

    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()

# Kiểm tra và thiết lập môi trường portable nếu cần
def check_portable_mode():
    try:
        import portable_config
        # Thiết lập môi trường portable
        config = portable_config.setup_portable_environment()
        print(f"Chạy ở chế độ portable. Thư mục ứng dụng: {config['app_path']}")
        return True
    except ImportError:
        # Không phải chế độ portable
        return False

if __name__ == "__main__":
    # Kiểm tra chế độ portable
    is_portable = check_portable_mode()
    
    # Khởi tạo và chạy ứng dụng
    app = SimoGUI()
    app.run()
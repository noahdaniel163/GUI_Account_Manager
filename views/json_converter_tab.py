import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from utils.logger import Logger

logger = Logger('json_converter_tab')

class JSONConverterTab:
    def __init__(self, parent, api_handler):
        self.parent = parent
        self.api_handler = api_handler
        
        # Frame chính
        self.json_converter_tab = ttk.Frame(parent)
        
        # Top frame cho tab
        self.json_converter_top_frame = ttk.Frame(self.json_converter_tab)
        self.json_converter_top_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.create_json_converter_section()
        
    def get_tab_frame(self):
        return self.json_converter_tab
        
    def create_json_converter_section(self):
        """Tạo giao diện cho tab JSON Converter"""
        # Service selection frame
        service_frame = ttk.LabelFrame(self.json_converter_top_frame, text="Chọn loại dịch vụ", padding="10")
        service_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.json_service_var = tk.StringVar(value="simo_001")
        services = ["simo_001", "simo_002", "simo_003", "simo_004", "simo_011", "simo_012"]
        service_combo = ttk.Combobox(service_frame, textvariable=self.json_service_var, 
                                   values=services, state='readonly', width=30)
        service_combo.pack(padx=5, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self.json_converter_top_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        load_json_btn = ttk.Button(button_frame, text="Tải JSON từ file", 
                                 command=self.load_json_file, style='Primary.TButton')
        load_json_btn.pack(side=tk.LEFT, padx=5)
        
        validate_btn = ttk.Button(button_frame, text="Kiểm tra JSON", 
                               command=self.validate_json, style='Info.TButton')
        validate_btn.pack(side=tk.LEFT, padx=5)
        
        send_json_btn = ttk.Button(button_frame, text="Gửi dữ liệu", 
                                command=self.send_json_data, style='Success.TButton')
        send_json_btn.pack(side=tk.LEFT, padx=5)
        
        # Paned window để chia màn hình thành 2 phần
        self.json_paned = ttk.PanedWindow(self.json_converter_tab, orient=tk.HORIZONTAL)
        self.json_paned.pack(fill=tk.BOTH, expand=True)
        
        # JSON Input frame (left side)
        json_input_frame = ttk.LabelFrame(self.json_paned, text="JSON Input", padding="10")
        self.json_paned.add(json_input_frame, weight=1)
        
        # Create JSON Input Text widget with scrollbars
        self.json_input_text = tk.Text(json_input_frame, wrap=tk.NONE, font=('Consolas', 10),
                                    bg='#f8f9fa', fg='#212529')
        
        json_input_scroll_y = ttk.Scrollbar(json_input_frame, orient=tk.VERTICAL,
                                         command=self.json_input_text.yview)
        json_input_scroll_x = ttk.Scrollbar(json_input_frame, orient=tk.HORIZONTAL,
                                         command=self.json_input_text.xview)
        
        self.json_input_text.configure(yscrollcommand=json_input_scroll_y.set,
                                    xscrollcommand=json_input_scroll_x.set)
        
        json_input_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        json_input_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.json_input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Validation Results frame (right side)
        validation_frame = ttk.LabelFrame(self.json_paned, text="Kết quả kiểm tra", padding="10")
        self.json_paned.add(validation_frame, weight=1)
        
        # Create Validation Results Text widget with scrollbars
        self.validation_text = tk.Text(validation_frame, wrap=tk.NONE, font=('Consolas', 10),
                                   bg='#f8f9fa', fg='#212529')
        
        validation_scroll_y = ttk.Scrollbar(validation_frame, orient=tk.VERTICAL,
                                        command=self.validation_text.yview)
        validation_scroll_x = ttk.Scrollbar(validation_frame, orient=tk.HORIZONTAL,
                                        command=self.validation_text.xview)
        
        self.validation_text.configure(yscrollcommand=validation_scroll_y.set,
                                   xscrollcommand=validation_scroll_x.set)
        
        validation_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        validation_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.validation_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                
    def load_json_file(self):
        """Tải dữ liệu từ file JSON"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_content = f.read()
                self.json_input_text.delete(1.0, tk.END)
                self.json_input_text.insert(tk.END, json_content)
                logger.info(f"Đã tải dữ liệu từ file JSON: {file_path}")
                messagebox.showinfo("Thành công", "Đã tải dữ liệu JSON!")
        except Exception as e:
            logger.error(f"Lỗi khi đọc file JSON: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể đọc file JSON: {str(e)}")

    def validate_json(self):
        """Kiểm tra tính hợp lệ của JSON và cấu trúc dữ liệu"""
        try:
            # Lấy nội dung JSON từ text input
            json_content = self.json_input_text.get(1.0, tk.END).strip()
            if not json_content:
                raise ValueError("Vui lòng nhập dữ liệu JSON!")

            # Parse JSON
            data = json.loads(json_content)
            
            # Kiểm tra xem có phải là list không
            if not isinstance(data, list):
                raise ValueError("Dữ liệu JSON phải là một mảng các đối tượng!")

            # Xóa nội dung cũ trong validation text
            self.validation_text.delete(1.0, tk.END)
            
            # Kiểm tra từng record
            service_type = self.json_service_var.get()
            validation_results = []
            
            for i, record in enumerate(data):
                record_result = f"Record {i+1}:\n"
                
                # Kiểm tra các trường bắt buộc theo loại dịch vụ
                required_fields = self.get_required_fields(service_type)
                missing_fields = [field for field in required_fields if field not in record]
                
                if missing_fields:
                    record_result += f"  - Thiếu các trường bắt buộc: {', '.join(missing_fields)}\n"
                
                # Kiểm tra kiểu dữ liệu và độ dài
                for field, value in record.items():
                    field_result = self.validate_field(field, value, service_type)
                    if field_result:
                        record_result += f"  - {field}: {field_result}\n"
                
                if record_result == f"Record {i+1}:\n":
                    record_result += "  - Hợp lệ\n"
                    
                validation_results.append(record_result)

            # Hiển thị kết quả kiểm tra
            summary = f"Tổng số records: {len(data)}\n\n"
            self.validation_text.insert(tk.END, summary + "\n".join(validation_results))
            
            logger.info("Đã kiểm tra dữ liệu JSON")
            messagebox.showinfo("Thành công", "Đã kiểm tra dữ liệu JSON!")
            
        except json.JSONDecodeError as e:
            logger.error(f"Lỗi JSON không hợp lệ: {str(e)}")
            messagebox.showerror("Lỗi", f"JSON không hợp lệ: {str(e)}")
        except Exception as e:
            logger.error(f"Lỗi khi kiểm tra dữ liệu: {str(e)}")
            messagebox.showerror("Lỗi", f"Lỗi khi kiểm tra dữ liệu: {str(e)}")

    def get_required_fields(self, service_type):
        """Lấy danh sách các trường bắt buộc theo loại dịch vụ"""
        required_fields = {
            "simo_001": ["Cif", "TenKhachHang", "SoTaiKhoan"],
            "simo_002": ["Cif", "TenKhachHang", "SoTaiKhoan"],
            "simo_003": ["Cif", "TenKhachHang", "SoTaiKhoan"],
            "simo_004": ["Cif", "TenKhachHang", "SoTaiKhoan"],
            "simo_011": ["Cif", "TenKhachHang", "SoTaiKhoan"],
            "simo_012": ["Cif", "TenKhachHang", "SoTaiKhoan"]
        }
        return required_fields.get(service_type, [])

    def validate_field(self, field, value, service_type):
        """Kiểm tra tính hợp lệ của một trường dữ liệu"""
        # Định nghĩa các ràng buộc cho từng trường
        field_constraints = {
            "Cif": {"type": str, "max_length": 36},
            "SoID": {"type": str, "max_length": 15},
            "TenKhachHang": {"type": str, "max_length": 150},
            "SoDienThoaiDangKyDichVu": {"type": str, "max_length": 15},
            "DiaChi": {"type": str, "max_length": 300},
            "DiaChiKiemSoatTruyCap": {"type": str, "max_length": 60},
            "MaSoNhanDangThietBiDiDong": {"type": str, "max_length": 36},
            "GhiChu": {"type": str, "max_length": 500}
        }
        
        constraints = field_constraints.get(field)
        if not constraints:
            return None
            
        # Kiểm tra kiểu dữ liệu
        if not isinstance(value, constraints["type"]):
            return f"Kiểu dữ liệu không hợp lệ (yêu cầu {constraints['type'].__name__})"
            
        # Kiểm tra độ dài nếu là string
        if constraints["type"] == str and len(value) > constraints["max_length"]:
            return f"Độ dài vượt quá giới hạn ({len(value)}/{constraints['max_length']})"
            
        return None

    def send_json_data(self):
        """Gửi dữ liệu JSON qua API"""
        try:
            json_content = self.json_input_text.get(1.0, tk.END).strip()
            if not json_content:
                messagebox.showwarning("Cảnh báo", "Không có dữ liệu JSON để gửi!")
                return
                
            # Parse JSON và gửi dữ liệu
            data = json.loads(json_content)
            service_type = self.json_service_var.get()
            
            # Gửi dữ liệu qua API
            result = self.api_handler.send_data(service_type, data)
            
            if result:
                logger.info(f"Gửi dữ liệu {service_type} thành công")
                messagebox.showinfo("Thành công", 
                                  f"Đã gửi dữ liệu {service_type} thành công!\n\nKết quả: {result}")
                
        except Exception as e:
            logger.error(f"Lỗi khi gửi dữ liệu: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể gửi dữ liệu: {str(e)}")
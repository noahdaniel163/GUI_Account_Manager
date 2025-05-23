import tkinter as tk
from tkinter import ttk

class DetailDialog:
    def __init__(self, parent, data_dict):
        self.top = tk.Toplevel(parent)
        self.top.title("Chi tiết tài khoản")
        
        # Thiết lập kích thước và vị trí cửa sổ
        window_width = 800
        window_height = 600
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.top.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Frame chính
        main_frame = ttk.Frame(self.top, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tạo canvas và scrollbar
        self.canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        
        # Frame cho nội dung
        self.content_frame = ttk.Frame(self.canvas)
        
        # Cấu hình canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack các widget
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Tạo cửa sổ trong canvas
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        
        # Tạo các section thông tin
        self.create_customer_info_section(data_dict)
        self.create_account_info_section(data_dict)
        self.create_other_info_section(data_dict)
        
        # Cập nhật scrollregion sau khi thêm nội dung
        self.content_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        # Nút đóng
        close_btn = ttk.Button(self.top, text="Đóng", command=self.on_close)
        close_btn.pack(pady=10)
        
        # Bind các sự kiện scroll
        self.bind_scroll_events()
        
        # Bind sự kiện đóng cửa sổ
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_customer_info_section(self, data_dict):
        self.create_info_section("Thông tin khách hàng", [
            ("CIF", str(data_dict["Cif"])),
            ("Số ID", str(data_dict["Soid"])),
            ("Loại ID", str(data_dict["LoaiD"])),
            ("Tên khách hàng", str(data_dict["TenKhachHang"])),
            ("Ngày sinh", str(data_dict["NgaySinh"])),
            ("Giới tính", "Nam" if str(data_dict["GioiTinh"]) == "1" else "Nữ"),
            ("Mã số thuế", str(data_dict["MaSoThue"])),
            ("Số điện thoại", str(data_dict["SoDienThoaiDangKyDichVu"])),
            ("Địa chỉ", str(data_dict["DiaChi"]))
        ])

    def create_account_info_section(self, data_dict):
        self.create_info_section("Thông tin tài khoản", [
            ("Số tài khoản", str(data_dict["SoTaiKhoan"])),
            ("Loại tài khoản", str(data_dict["LoaiTaiKhoan"])),
            ("Trạng thái", "Hoạt động" if str(data_dict["TrangThaiHoatDongTaiKhoan"]) == "1" else "Không hoạt động"),
            ("Ngày mở TK", str(data_dict["NgayMoTaiKhoan"])),
            ("Phương thức mở", str(data_dict["PhuongThucMoTaiKhoan"])),
            ("Ngày xác thực tại quầy", str(data_dict["NgayXacThucTaiQuay"])),
            ("Địa chỉ kiểm soát", str(data_dict["DiaChiKiemSoatTruyCap"])),
            ("Mã thiết bị", str(data_dict["MaSoNhanDangThietBiDong"]))
        ])

    def create_other_info_section(self, data_dict):
        self.create_info_section("Thông tin khác", [
            ("Loại khách hàng", str(data_dict["LoaiKhachHang"])),
            ("Quốc tịch", str(data_dict["QuocTich"])),
            ("Ngày cập nhật", str(data_dict["UpdateDate"])),
            ("Nghị ngờ", "Có" if str(data_dict["NghiNgo"]) == "1" else "Không"),
            ("Ghi chú", str(data_dict["GhiChu"]) if data_dict["GhiChu"] else "")
        ])
        
    def create_info_section(self, title, fields):
        """Tạo một section thông tin với tiêu đề và các trường dữ liệu"""
        section_frame = ttk.LabelFrame(self.content_frame, text=title, padding="10")
        section_frame.pack(fill="x", padx=5, pady=5)
        
        for label, value in fields:
            row = ttk.Frame(section_frame)
            row.pack(fill="x", padx=5, pady=2)
            
            label_widget = ttk.Label(row, text=f"{label}:", width=20, anchor="e")
            label_widget.pack(side="left", padx=(0, 10))
            
            value_widget = ttk.Label(row, text=value if value not in [None, "None", ""] else "N/A", 
                                   wraplength=500, justify="left")
            value_widget.pack(side="left", fill="x", expand=True)
            
    def on_mousewheel(self, event):
        """Xử lý sự kiện scroll chuột"""
        self.canvas.yview_scroll(-1*(event.delta//120), "units")
        
    def bind_scroll_events(self):
        """Bind các sự kiện scroll"""
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
    def unbind_scroll_events(self):
        """Unbind các sự kiện scroll khi đóng dialog"""
        self.canvas.unbind_all("<MouseWheel>")
        
    def on_close(self):
        """Xử lý khi đóng dialog"""
        self.unbind_scroll_events()
        self.top.destroy()
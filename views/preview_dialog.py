import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

class PreviewDialog:
    def __init__(self, parent, converted_data, service_type):
        self.top = tk.Toplevel(parent)
        self.top.title(f"Xem trước kết quả chuyển đổi - {service_type}")
        
        # Thiết lập kích thước và vị trí cửa sổ
        window_width = 1000
        window_height = 700
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.top.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Frame chính
        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Label thông tin
        info_text = f"Định dạng: {service_type}\nSố bản ghi: {len(converted_data)}"
        info_label = ttk.Label(main_frame, text=info_text, justify=tk.LEFT)
        info_label.pack(fill=tk.X, padx=5, pady=5)
        
        # Frame cho Text widget và scrollbar
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Text widget hiển thị JSON
        self.text_widget = tk.Text(text_frame, wrap=tk.NONE, font=('Consolas', 10))
        
        # Scrollbars
        y_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_widget.yview)
        x_scrollbar = ttk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=self.text_widget.xview)
        
        self.text_widget.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        
        # Pack các components
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        x_scrollbar.pack(fill=tk.X)
        
        # Hiển thị JSON được format
        json_str = json.dumps(converted_data, ensure_ascii=False, indent=2)
        self.text_widget.insert(tk.END, json_str)
        self.text_widget.configure(state='disabled')  # Chỉ cho phép đọc
        
        # Frame cho các nút
        button_frame = ttk.Frame(self.top)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Nút Export để xuất file
        export_btn = ttk.Button(button_frame, text="Xuất JSON", 
                              command=lambda: self.export_json(converted_data, service_type))
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Nút đóng
        close_btn = ttk.Button(button_frame, text="Đóng", command=self.top.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)
    
    def export_json(self, data, service_type):
        """Xuất dữ liệu JSON ra file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialfile=f"TKTT_{service_type}.json"
        )
        
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Thành công", f"Đã xuất dữ liệu ra file:\n{file_path}")
import os
import shutil
import subprocess
import sys

def clean_build_folders():
    """Xóa các thư mục build cũ"""
    folders_to_clean = ['build', 'dist', '__pycache__']
    for folder in folders_to_clean:
        if os.path.exists(folder):
            print(f"Đang xóa thư mục {folder}...")
            shutil.rmtree(folder)
    
    # Xóa các file __pycache__ trong các thư mục con
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            print(f"Đang xóa {pycache_path}...")
            shutil.rmtree(pycache_path)

def create_logs_folder():
    """Tạo thư mục logs trong thư mục dist"""
    dist_logs_path = os.path.join('dist', 'logs')
    if not os.path.exists(dist_logs_path):
        os.makedirs(dist_logs_path)
        print(f"Đã tạo thư mục {dist_logs_path}")

def build_executable():
    """Build file thực thi với PyInstaller"""
    print("Đang build file thực thi...")
    result = subprocess.run(['pyinstaller', 'simo_gui.spec'], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Lỗi khi build file thực thi:")
        print(result.stderr)
        return False
    
    print("Build thành công!")
    return True

def main():
    # Xóa các thư mục build cũ
    clean_build_folders()
    
    # Build file thực thi
    if not build_executable():
        sys.exit(1)
    
    # Tạo thư mục logs
    create_logs_folder()
    
    print("\nQuá trình build hoàn tất!")
    print("File thực thi được tạo tại: dist/SIMO_GUI_Enhanced.exe")

if __name__ == "__main__":
    main()
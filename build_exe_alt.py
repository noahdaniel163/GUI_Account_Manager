import PyInstaller.__main__
import os
import shutil

# Xóa các thư mục build cũ
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

# Tạo thư mục logs
if not os.path.exists('dist/logs'):
    os.makedirs('dist/logs', exist_ok=True)

# Cấu hình PyInstaller
PyInstaller.__main__.run([
    'main.py',
    '--name=SIMO_GUI_Enhanced_Alt',
    '--onefile',
    '--windowed',
    '--clean',
    '--add-data=utils;utils',
    '--add-data=schemas;schemas',
    '--hidden-import=pyodbc',
    '--hidden-import=pydantic',
    '--hidden-import=openpyxl',
    '--hidden-import=requests',
    '--hidden-import=json',
    '--hidden-import=base64',
    '--hidden-import=datetime',
    '--hidden-import=logging',
    '--collect-submodules=pyodbc',
    '--collect-submodules=openpyxl',
    '--collect-submodules=pydantic',
])

print("Build completed. Executable is at dist/SIMO_GUI_Enhanced_Alt.exe")
from PyInstaller.utils.hooks import collect_all

# Collect all pyodbc binaries, data files, and dependencies
datas, binaries, hiddenimports = collect_all('pyodbc')

# Add specific DLLs that might be missing
binaries.extend([
    ('C:/Windows/System32/msvcp140.dll', '.'),
    ('C:/Windows/System32/vcruntime140.dll', '.'),
    ('C:/Windows/System32/vcruntime140_1.dll', '.'),
])
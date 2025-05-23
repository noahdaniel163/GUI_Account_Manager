import os

# Mặc định sử dụng SQL Server
USE_LOCAL_DB = False

# Đường dẫn đến file SQLite
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.db')

# Cấu hình API
API_CONFIG = {
    'token_url': 'https://example.com/api/token',
    'base_url': 'https://example.com/api',
    'timeout': 30
}

# Các endpoint mặc định
DEFAULT_ENDPOINTS = {
    'token': 'https://example.com/api/token',
    'simo_001': 'https://example.com/api/simo/001',
    'simo_002': 'https://example.com/api/simo/002',
    'simo_003': 'https://example.com/api/simo/003',
    'simo_004': 'https://example.com/api/simo/004',
    'simo_011': 'https://example.com/api/simo/011',
    'simo_012': 'https://example.com/api/simo/012'
}
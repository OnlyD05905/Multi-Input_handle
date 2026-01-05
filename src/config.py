import os

# --- CẤU HÌNH ĐƯỜNG DẪN (PATHS) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Thư mục dữ liệu
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')

# Đường dẫn cụ thể đến từng file Dataset
AUTH_FILE = os.path.join(DATA_DIR, 'auth.txt.gz')
PROC_FILE = os.path.join(DATA_DIR, 'proc.txt.gz')
FLOWS_FILE = os.path.join(DATA_DIR, 'flows.txt.gz')
DNS_FILE = os.path.join(DATA_DIR, 'dns.txt.gz')
REDTEAM_FILE = os.path.join(DATA_DIR, 'redteam.txt.gz')

# --- CẤU HÌNH HỆ THỐNG (SETTINGS) ---
# Số dòng đọc mỗi lần (Chunk size)
CHUNK_SIZE = 10000

# Ngưỡng cảnh báo (Thresholds) - Dùng cho các Rule sau này
THRESHOLD_PORT_SCAN = 10  # Nếu 1 IP kết nối > 10 cổng lạ trong 1s -> Báo động
THRESHOLD_DATA_EXFIL = 10000000 # Nếu gửi > 10MB dữ liệu ra ngoài -> Báo động
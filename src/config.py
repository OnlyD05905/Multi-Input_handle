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
CHUNK_SIZE = 10000
THRESHOLD_PORT_SCAN = 10 
THRESHOLD_DATA_EXFIL = 10000000 

# --- [MỚI] CẤU HÌNH LIVE CAPTURE (Refactor Day 1) ---
# Chế độ chạy mặc định: 'LIVE' hoặc 'FILE'
DEFAULT_RUN_MODE = 'LIVE'

# Đường dẫn tới Tshark (Lấy chính xác từ máy bạn)
TSHARK_PATH = r"D:\Desktop\Computer_Network\App_hot\Wireshark\tshark.exe"

# Tên Card mạng hoặc Index (Số 5 là Wi-Fi của bạn)
LIVE_INTERFACE = '4'
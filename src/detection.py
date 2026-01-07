from ai_engine import AnomalyDetector 
from interfaces import BaseDetector




# --- 2. Signature Detector (Bộ phát hiện theo luật - Nâng cấp V2) ---
class SignatureBasedDetector(BaseDetector):
    def __init__(self):
        # CẤU HÌNH LUẬT (RULES CONFIGURATION)
        self.rules = {
            # [AUTH] Danh sách user đen
            'suspicious_auth': {'ANONYMOUS LOGON'},
            
            # [PROCESS] Danh sách công cụ Red Team (Hacker hay dùng)
            # Lưu ý: Viết thường toàn bộ để so sánh không phân biệt hoa/thường
            'red_team_tools': {
                'mimikatz', 'powershell', 'psexec', 'remotepsexec', 
                'procdump', 'net', 'dsquery', 'whoami', 'tasklist', 'nmap'
            },
            
            # [NETWORK] Các cổng quản trị nhạy cảm
            'critical_ports': {
                22: 'SSH (Remote Linux)',
                3389: 'RDP (Remote Windows)',
                445: 'SMB (File Share)',
                23: 'Telnet (Insecure Remote)',
                21: 'FTP'
            },
            
            # [NETWORK] Ngưỡng dung lượng nghi ngờ là tuồn dữ liệu (Data Exfiltration)
            # Đặt thấp (10MB) để dễ thấy cảnh báo khi chạy demo. 
            # Thực tế có thể đặt 500MB hoặc 1GB.
            'exfiltration_threshold': 10 * 1024 * 1024 
        }

    def detect(self, log):
        """Điều hướng log tới hàm xử lý riêng biệt"""
        source = log.get('Log_Source')
        
        if source == 'auth':
            return self._check_auth(log)
        elif source == 'proc':
            return self._check_process(log)
        elif source == 'flows':
            return self._check_network(log)
        
        return []

    # --- CÁC HÀM LOGIC CHI TIẾT ---

    def _check_auth(self, log):
        """Rule 01: Phát hiện đăng nhập ẩn danh"""
        alerts = []
        src_user = log.get('Source_User', '')
        
        if src_user in self.rules['suspicious_auth']:
            alerts.append({
                'title': 'Suspicious Auth Pattern',
                'severity': 'HIGH',         # Mức CAO
                'description': f"Blacklisted login detected: {src_user}",
                'log_data': log
            })
        return alerts

    def _check_process(self, log):
        """Rule 04: Phát hiện công cụ hacker (Process)"""
        alerts = []
        proc_name = str(log.get('Process_Name', '')).lower()
        
        # Quét xem tên process có chứa từ khóa nguy hiểm không
        for tool in self.rules['red_team_tools']:
            if tool in proc_name:
                alerts.append({
                    'title': 'Malicious Tool Detected',
                    'severity': 'CRITICAL', # Mức NGUY HIỂM NHẤT
                    'description': f"Known attack tool executed: '{proc_name}' by user {log.get('User')}",
                    'log_data': log
                })
        return alerts

    def _check_network(self, log):
        """Rule 02 & 03: Kiểm tra Mạng (Port & Volume)"""
        alerts = []
        try:
            # Ép kiểu dữ liệu về số nguyên để so sánh toán học
            # (Vì dữ liệu đọc từ file có thể là chuỗi string "445")
            dst_port = int(log.get('Dest_Port', 0))
            byte_count = int(log.get('Byte_Count', 0))
        except ValueError:
            return []

        # [Rule 02] Critical Port Access (Truy cập cổng nhạy cảm)
        if dst_port in self.rules['critical_ports']:
            service_name = self.rules['critical_ports'][dst_port]
            alerts.append({
                'title': 'Sensitive Service Access',
                'severity': 'MEDIUM',   # Mức TRUNG BÌNH (Cảnh báo vàng)
                'description': f"Connection to administrative port {dst_port} ({service_name}) detected.",
                'log_data': log
            })

        # [Rule 03] Data Exfiltration (Truyền tải dữ liệu lớn)
        if byte_count > self.rules['exfiltration_threshold']:
            mb_size = round(byte_count / (1024 * 1024), 2)
            alerts.append({
                'title': 'Potential Data Exfiltration',
                'severity': 'HIGH',     # Mức CAO (Cảnh báo cam/đỏ)
                'description': f"Large file transfer detected: {mb_size} MB sent to {log.get('Dest_Computer')}",
                'log_data': log
            })

        return alerts

# --- 3. Main Engine Wrapper ---
class DetectionEngine:
    def __init__(self):
        # Đăng ký các Detector tại đây
        self.detectors = [
            SignatureBasedDetector(),
            AnomalyDetector()
            # Sau này thêm: AnomalyDetector()
        ]

    def analyze(self, log):
        all_alerts = []
        for detector in self.detectors:
            try:
                # Gọi hàm detect của từng module con
                alerts = detector.detect(log)
                if alerts:
                    all_alerts.extend(alerts)
            except Exception as e:
                # Nếu 1 module lỗi, hệ thống vẫn chạy tiếp (Fault Tolerance)
                # print(f"[Error] Detector failed: {e}")
                pass 
        return all_alerts
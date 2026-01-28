import time
from ai_engine import AnomalyDetector 
from interfaces import BaseDetector

# --- 2. Signature Detector (Bộ phát hiện theo luật - Nâng cấp V3 - TCP Analysis) ---
class SignatureBasedDetector(BaseDetector):
    def __init__(self):
        # CẤU HÌNH LUẬT
        self.rules = {
            'suspicious_auth': {'ANONYMOUS LOGON', 'guest', 'administrator'},
            'red_team_tools': {
                'mimikatz', 'powershell', 'psexec', 'remotepsexec', 
                'procdump', 'net', 'dsquery', 'whoami', 'tasklist', 'nmap'
            },
            'critical_ports': {
                22: 'SSH', 3389: 'RDP', 445: 'SMB', 23: 'Telnet', 21: 'FTP'
            },
            'exfiltration_threshold': 10 * 1024 * 1024,
            
            # [CŨ] Chữ ký Scan
            'scan_signatures': {
                0: 'Null Scan (Stealth Recon)',
                41: 'Xmas Scan (OS Fingerprinting)'
            },

            # [MỚI - NGÀY 5] Cấu hình chống DoS
            'syn_flood_threshold': 100, # Cho phép tối đa 100 gói SYN/giây
        }

        # [MỚI] Bộ nhớ tạm để đếm gói tin (Stateful Memory)
        # Cấu trúc: { 'IP_Source': {'count': 0, 'start_time': 170000...} }
        self.syn_tracker = {}

    def detect(self, log):
        source = log.get('Log_Source')
        if source == 'auth': return self._check_auth(log)
        elif source == 'proc': return self._check_process(log)
        elif source == 'flows': return self._check_network(log)
        return []

    # --- CÁC HÀM LOGIC CHI TIẾT ---

    def _check_auth(self, log):
        alerts = []
        src_user = log.get('Source_User', '')
        if src_user in self.rules['suspicious_auth']:
            alerts.append({'title': 'Suspicious Auth', 'severity': 'HIGH', 'description': f"Blacklist: {src_user}", 'log_data': log})
        return alerts

    def _check_process(self, log):
        alerts = []
        proc_name = str(log.get('Process_Name', '')).lower()
        for tool in self.rules['red_team_tools']:
            if tool in proc_name:
                alerts.append({'title': 'Malicious Tool', 'severity': 'CRITICAL', 'description': f"Tool: {proc_name}", 'log_data': log})
        return alerts

    def _check_network(self, log):
        alerts = []
        try:
            dst_port = int(log.get('Dest_Port', 0))
            byte_count = int(log.get('Byte_Count', 0))
            tcp_flags_hex = log.get('TCP_Flags')
        except ValueError:
            return []

        # 1. Port Security
        if dst_port in self.rules['critical_ports']:
            alerts.append({'title': 'Sensitive Service Access', 'severity': 'MEDIUM', 'description': f"Port {dst_port} accessed", 'log_data': log})

        # 2. Volume Security
        if byte_count > self.rules['exfiltration_threshold']:
            alerts.append({'title': 'Data Exfiltration', 'severity': 'HIGH', 'description': f"Large file sent", 'log_data': log})

        # 3. TCP Flag Analysis
        if tcp_flags_hex:
            try:
                flags_int = int(tcp_flags_hex, 16)
                
                # [A] Phát hiện Scan (Null/Xmas)
                if flags_int in self.rules['scan_signatures']:
                    scan_type = self.rules['scan_signatures'][flags_int]
                    alerts.append({
                        'title': 'Network Scan Activity',
                        'severity': 'HIGH',
                        'description': f"DETECTED: {scan_type}",
                        'log_data': log
                    })

                # [B - MỚI] Phát hiện SYN Flood (DoS)
                # 0x002 là cờ SYN
                if flags_int == 0x002: 
                    flood_alert = self._check_syn_flood(log)
                    if flood_alert:
                        alerts.append(flood_alert)

            except ValueError:
                pass
        return alerts

    # [MỚI - NGÀY 5] Hàm logic đếm gói tin
    def _check_syn_flood(self, log):
        src_ip = log.get('Source_IP')
        current_time = time.time()
        
        # Nếu IP này chưa từng gặp, tạo hồ sơ mới
        if src_ip not in self.syn_tracker:
            self.syn_tracker[src_ip] = {'count': 1, 'start_time': current_time}
            return None
        
        # Lấy hồ sơ cũ ra
        tracker = self.syn_tracker[src_ip]
        
        # Nếu đã qua 1 giây -> Reset đếm lại từ đầu (Sang trang mới)
        if current_time - tracker['start_time'] > 1.0:
            tracker['count'] = 1
            tracker['start_time'] = current_time
        else:
            # Nếu vẫn trong 1 giây -> Tăng biến đếm
            tracker['count'] += 1
            
            # Kiểm tra ngưỡng (Threshold)
            if tracker['count'] == self.rules['syn_flood_threshold']:
                return {
                    'title': 'DoS Attack Detected (SYN Flood)',
                    'severity': 'CRITICAL', # Mức Nguy Hiểm Nhất
                    'description': f"High volume of SYN packets from {src_ip} (> {self.rules['syn_flood_threshold']}/sec)",
                    'log_data': log
                }
        
        return None

# --- 3. Main Engine Wrapper ---
class DetectionEngine:
    def __init__(self):
        self.detectors = [
            SignatureBasedDetector(),
            AnomalyDetector()
        ]

    def analyze(self, log):
        all_alerts = []
        for detector in self.detectors:
            try:
                alerts = detector.detect(log)
                if alerts:
                    all_alerts.extend(alerts)
            except Exception as e:
                pass 
        return all_alerts
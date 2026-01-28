import json
import subprocess
import time
import sys
import config  # Import config đã làm ở Ngày 1

class LiveStreamer:
    def __init__(self, interface=None):
        # Lấy cấu hình từ config.py
        self.interface = interface if interface else config.LIVE_INTERFACE
        self.tshark_path = config.TSHARK_PATH
        print(f"[INFO] Initializing Direct Capture on Interface #{self.interface}")

    def stream(self):
        # Lệnh chạy Tshark (Giữ nguyên)
        cmd = [
            self.tshark_path,
            "-i", self.interface,
            "-l", 
            "-n", 
            "-T", "ek" 
        ]

        print(f"[INFO] Executing Tshark...")

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            print("[INFO] Capture started. Waiting for traffic...")

            for line in process.stdout:
                line = line.strip()
                if not line: continue
                
                try:
                    data = json.loads(line)
                    if 'layers' not in data: continue
                    
                    layers = data['layers']
                    if 'ip' not in layers: continue

                    # --- 1. LẤY THÔNG TIN CƠ BẢN ---
                    ip_layer = layers['ip']
                    src_ip = ip_layer.get('ip_ip_src', '0.0.0.0')
                    dst_ip = ip_layer.get('ip_ip_dst', '0.0.0.0')
                    
                    frame_layer = layers.get('frame', {})
                    length = int(frame_layer.get('frame_frame_len', 0))

                    dest_port = 0
                    protocol = 'Other'
                    
                    # --- [MỚI - NGÀY 2] 2. LẤY TCP FLAGS ---
                    tcp_flags = None  # Mặc định là None nếu không phải TCP
                    tcp_flags_str = ""

                    if 'tcp' in layers:
                        protocol = 'TCP'
                        tcp_layer = layers['tcp']
                        dest_port = int(tcp_layer.get('tcp_tcp_dstport', 0))
                        
                        # Lấy mã Hex của Flags (Ví dụ: "0x0002" là SYN)
                        # Tshark trả về dạng string hex, ta giữ nguyên để xử lý sau
                        tcp_flags = tcp_layer.get('tcp_tcp_flags', '0x0000')
                        # --- [THÊM DÒNG NÀY ĐỂ DEBUG] ---
                        print(f"[DEBUG] Packet detected! Flags: {tcp_flags} | IP: {src_ip} -> {dst_ip}")
                        # tcp_flags ='0x0000'
                    elif 'udp' in layers:
                        protocol = 'UDP'
                        dest_port = int(layers['udp'].get('udp_udp_dstport', 0))

                    # --- 3. ĐÓNG GÓI LOG ---
                    log_entry = {
                        'Log_Source': 'flows',
                        'Time': int(time.time()),
                        'Source_IP': src_ip,
                        'Dest_IP': dst_ip,
                        'Dest_Port': dest_port,
                        'Protocol': protocol,
                        'Byte_Count': length,
                        # Thêm trường mới vào Log
                        'TCP_Flags': tcp_flags, 
                        'raw_packet': 'live_capture'
                    }

                    yield log_entry

                except json.JSONDecodeError:
                    continue
                except Exception:
                    continue

        except FileNotFoundError:
            print(f"[ERROR] Cannot find Tshark at: {self.tshark_path}")
            yield None
        except Exception as e:
            print(f"[ERROR] Subprocess failed: {e}")
            yield None

if __name__ == "__main__":
    # Test chạy thử để xem có ra Flags không
    streamer = LiveStreamer()
    for log in streamer.stream():
        # Chỉ in ra nếu là TCP để đỡ rối mắt
        if log['Protocol'] == 'TCP':
            print(f"[TCP] Flags: {log['TCP_Flags']} | {log['Source_IP']} -> {log['Dest_IP']}:{log['Dest_Port']}")
import json
import subprocess
import time
import sys

class LiveStreamer:
    def __init__(self, interface='5'):
        # Đường dẫn tshark chính xác từ máy bạn
        self.tshark_path = r"D:\Desktop\Computer_Network\App_hot\Wireshark\tshark.exe"
        self.interface = interface
        print(f"[INFO] Initializing Direct Capture on Interface #{interface}")

    def stream(self):
        # Lệnh chạy Tshark:
        # -i: Interface
        # -l: Flush line (đẩy dữ liệu ra ngay lập tức)
        # -n: Không phân giải tên miền (cho nhanh)
        # -T ek: Định dạng JSON Streaming (Mỗi dòng là 1 gói tin)
        cmd = [
            self.tshark_path,
            "-i", self.interface,
            "-l", 
            "-n", 
            "-T", "ek" 
        ]

        print(f"[INFO] Executing: {' '.join(cmd)}")
        print("[INFO] Capture started. Waiting for traffic...")

        try:
            # Mở tiến trình con chạy ngầm Tshark
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True, # Đọc dạng text thay vì binary
                encoding='utf-8',
                errors='replace' # Bỏ qua lỗi ký tự lạ
            )

            # Đọc từng dòng kết quả trả về
            for line in process.stdout:
                line = line.strip()
                if not line: continue
                
                try:
                    # Parse dòng text thành JSON
                    data = json.loads(line)
                    
                    # Định dạng EK của Tshark in ra 2 loại dòng: index và layers
                    # Chúng ta chỉ quan tâm dòng chứa dữ liệu "layers"
                    if 'layers' not in data:
                        continue
                    
                    layers = data['layers']
                    
                    # Chỉ lấy gói tin IP
                    if 'ip' not in layers:
                        continue

                    # --- TRÍCH XUẤT DỮ LIỆU ---
                    ip_layer = layers['ip']
                    src_ip = ip_layer.get('ip_ip_src', '0.0.0.0')
                    dst_ip = ip_layer.get('ip_ip_dst', '0.0.0.0')
                    
                    # Lấy kích thước (frame length)
                    frame_layer = layers.get('frame', {})
                    length = int(frame_layer.get('frame_frame_len', 0))

                    # Lấy Port & Protocol
                    dest_port = 0
                    protocol = 'Other'

                    if 'tcp' in layers:
                        protocol = 'TCP'
                        dest_port = int(layers['tcp'].get('tcp_tcp_dstport', 0))
                    elif 'udp' in layers:
                        protocol = 'UDP'
                        dest_port = int(layers['udp'].get('udp_udp_dstport', 0))

                    # Tạo log chuẩn
                    log_entry = {
                        'Log_Source': 'flows',
                        'Time': int(time.time()),
                        'Source_IP': src_ip,
                        'Dest_IP': dst_ip,
                        'Dest_Port': dest_port,
                        'Protocol': protocol,
                        'Byte_Count': length,
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
    streamer = LiveStreamer(interface='5')
    for log in streamer.stream():
        print(f"[LIVE] {log['Source_IP']} -> {log['Dest_IP']} ({log['Byte_Count']} B)")
# System Architecture

## Data Flow Pipeline (Luồng dữ liệu)

Hệ thống hoạt động theo mô hình Pipeline (Tuần tự) như sau:

1.  **Input Source (Nguồn vào):**
    * **Offline Mode:** Đọc từ file log nén `.gz` (Dataset LANL).
    * **Online Mode (Future):** Bắt gói tin trực tiếp từ Interface mạng (Wireshark/Pyshark).

2.  **Streamer (Bộ phát):**
    * Module: `src/streamer.py`
    * Nhiệm vụ: Đọc dữ liệu thô theo từng block (Chunking), đồng bộ hóa thời gian giữa các nguồn (Time Synchronization) và đẩy từng dòng sự kiện vào hệ thống.

3.  **Preprocessor (Tiền xử lý):**
    * Module: `src/preprocess.py`
    * Nhiệm vụ:
        * Làm sạch dữ liệu (Cleaning).
        * Tách trường (Parsing): Ví dụ tách `User@Domain` thành `User` và `Domain`.
        * Chuẩn hóa (Normalization): Chuyển đổi IP, Port về định dạng chuẩn.

4.  **Detection Engine (Bộ phát hiện):**
    * Module: `src/detection.py`
    * Nhiệm vụ: So khớp sự kiện với các luật (Rules) hoặc Mô hình AI.
    * Các quy tắc hiện tại:
        * **Signature:** So khớp với danh sách đen (Red Team IP/User).
        * **Network Anomaly:** Phát hiện quét cổng (Port Scan), truyền tải dữ liệu lớn (Data Exfiltration).
        * **Behavior Anomaly:** Phát hiện tiến trình lạ, đăng nhập bất thường.

5.  **Alert System (Hệ thống cảnh báo):**
    * Module: `src/alert.py`
    * Nhiệm vụ:
        * In cảnh báo ra màn hình Console (Real-time).
        * Ghi log cảnh báo vào Database `alerts.db` (SQLite) để lưu trữ.

## 🗂️ Database Schema (SQLite)

Bảng `alerts`:
* `id`: Primary Key (Auto Increment)
* `timestamp`: Thời gian phát hiện.
* `log_time`: Thời gian trong log sự kiện.
* `source_ip`: IP/Máy nguồn.
* `dest_ip`: IP/Máy đích.
* `alert_type`: Loại cảnh báo (VD: RedTeam, PortScan, Anomaly).
* `severity`: Mức độ (Critical, High, Medium, Low).
* `details`: Chi tiết sự kiện (JSON/String).
## [Phase 1] - Foundation
- Thiết lập cấu trúc dự án.
- Xử lý Big Data bằng Chunking (~80k logs/sec).

## [Phase 2 -> Phase 6] - Core System Implementation (Completed 06/01/2026)
### Added
- **Multi-Input Streaming:** Hỗ trợ đọc song song 4 file log và đồng bộ thời gian (`heapq`).
- **Preprocessing:** Module làm sạch dữ liệu, tách trường thông tin User/Machine.
- **Detection Engine (Modular):**
    - Chuyển đổi từ hard-code sang kiến trúc `BaseDetector` (Scalable).
    - Rule 01: Phát hiện `ANONYMOUS LOGON`.
- **Database Integration:**
    - Tích hợp SQLite để lưu trữ cảnh báo bền vững (`alert.db`).
    - Tách biệt Code (`src/`) và Data.
- **Web Dashboard:**
    - Giao diện Flask hiển thị Real-time.
    - Dark Mode UI, thống kê mức độ nghiêm trọng.

### Changed
- Refactor `main.py` để kết nối toàn bộ quy trình: Stream -> Preprocess -> Detect -> DB -> Dashboard.
- Cập nhật quản lý đường dẫn file sử dụng `os.path` để tránh lỗi khi chạy ở các môi trường khác nhau.

## [Phase 7 & 8] - Advanced Rules & AI Integration (07/01/2026)

### Added (Tính năng mới)
- **AI Anomaly Detection:**
    - Tích hợp `scikit-learn` Isolation Forest.
    - Cơ chế hiển thị tiến độ Training (Loading bar) trên Console.
- **Advanced Signature Rules:**
    - Rule phát hiện truy cập Port nhạy cảm (445, 3389) - MEDIUM.
    - Rule phát hiện công cụ Red Team (Process Name) - CRITICAL.
    - Rule phát hiện Data Exfiltration (Volume Check) - HIGH.
- **Dashboard V2:**
    - Thêm biểu đồ tròn (Pie Chart) thống kê AI vs Rules.
    - Thêm chỉ số "AI Anomalies" và hiệu ứng UI.

### Changed (Thay đổi)
- **Refactor:** Tách `BaseDetector` sang `src/interfaces.py` để giải quyết lỗi Circular Import.
- **Engine Core:** Nâng cấp `DetectionEngine` để chạy song song cả Signature Detector và Anomaly Detector.

## [Phase 9] - Real-time Defense & Stateful Analysis (28/01/2026)

### Added (Tính năng mới)
- **Live Packet Capture:**
    - Tích hợp `Tshark` backend để bắt gói tin trực tiếp từ Card Wi-Fi/Ethernet.
    - Hỗ trợ giải mã gói tin TCP/IP thời gian thực.
- **Deep Packet Inspection (DPI):**
    - Khả năng đọc và phân tích các cờ TCP (TCP Flags).
    - Phát hiện các kỹ thuật Scan tàng hình: **Null Scan**, **Xmas Scan**.
- **Stateful Detection Engine (DoS Protection):**
    - Nâng cấp bộ não phát hiện từ "Stateless" sang "Stateful".
    - Cơ chế **SYN Flood Protection**: Theo dõi số lượng gói SYN từ 1 IP trong cửa sổ thời gian trượt (Sliding Window).
    - Ngưỡng cảnh báo (Threshold): > 100 SYN packets/second.

### Changed (Cải thiện)
- **Configuration:** Tách cấu hình Interface mạng ra file `config.py` để dễ dàng chuyển đổi giữa các máy.
- **Fix:** Khắc phục lỗi binding sai Interface khiến Tshark không bắt được gói tin trên Windows.
- **Performance:** Tối ưu hóa việc in log Debug, giảm nhiễu khi hệ thống chạy ở tốc độ cao.


# System Architecture (V2.0)

## 1. High-Level Overview
Hệ thống được thiết kế theo mô hình **Pipeline (Đường ống)** và **Decoupled (Tách biệt)**, đảm bảo khả năng mở rộng dễ dàng cho AI và Real-time sau này.

```mermaid
graph LR
    A1[Dataset LANL (.gz)] --> B{Streamer Selector}
    A2[Live Network (Wi-Fi/Eth)] --> B
    B -->|Offline| C1[LogStreamer]
    B -->|Real-time| C2[LivePacketStreamer]
    C1 & C2 --> D(Preprocessor/Normalizer)
    D --> E{Detection Engine}
    E -->|Stateful| F1[Signature Detector V2]
    E -->|AI/ML| F2[Anomaly Detector]
    F1 & F2 --> G[Alert Manager]
    G --> H[(SQLite Database)]
    H -.-> I[Web Dashboard]
```
## 2. Chi tiết các Module

### A. Streamer Layer

**A.1 LogStreamer:** Xử lý file log tĩnh (Chunking, Merge Sort).(Future).

**A.2 LivePacketStreamer (``src/live_streamer.py``):**

1.  Sử dụng Tshark/PyShark để bắt gói tin trực tiếp từ Interface mạng.

2.  Bộ lọc BPF: Chỉ bắt các gói TCP/UDP quan trọng để tối ưu hiệu năng.


## B. Preprocessing Layer (src/preprocess.py)

**TCP Analysis:** rích xuất cờ TCP (Flags: SYN, ACK, FIN, PSH) để phục vụ phân tích hành vi.

## C. Detection Engine (Stateful Upgrade)



1. SignatureBasedDetector (V2 - Stateful):

 - Stateless Rules: Phát hiện dựa trên mẫu gói tin đơn lẻ (Null Scan, Xmas Scan, Malicious Payload).

- Stateful Memory: Sử dụng bộ nhớ tạm (In-memory tracking) để đếm tần suất gói tin theo thời gian thực (Rate Limiting).

- Ứng dụng: Phát hiện tấn công DoS/SYN Flood (Ví dụ: > 100 SYN packets/sec).

2. AnomalyDetector (AI):

- Sử dụng Isolation Forest để phát hiện bất thường phi tuyến tính.

## D. Alert & Storage (src/alert.py)
**Lưu trữ cảnh báo vào SQLite (alert.db) với độ trễ thấp.**


## E. Visualization (src/dashboard.py)
**Dashboard Flask tự động refresh (3s) để hiển thị các cuộc tấn công đang diễn ra ngay lập tức.**

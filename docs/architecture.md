

# System Architecture (V2.0)

## 1. High-Level Overview
Hệ thống được thiết kế theo mô hình **Pipeline (Đường ống)** và **Decoupled (Tách biệt)**, đảm bảo khả năng mở rộng dễ dàng cho AI và Real-time sau này.

```mermaid
graph LR
    A[Dataset LANL (.gz)] --> B[LogStreamer]
    B --> C(Preprocessor)
    C --> D{Detection Engine}
    D -->|Rule-based| E1[Signature Detector]
    D -->|ML-based| E2[AI Anomaly Detector]
    E1 & E2 --> F[Alert Manager]
    F --> G[(SQLite Database)]
    G -.-> H[Web Dashboard]
```
## 2. Chi tiết các Module

### A. Streamer Layer (``src/streamer.py``)

**A.1 Input:** File Logs (Auth, Proc, Flows, DNS) hoặc Live Capture (Future).

**A.2 Logic:**

1.  Chunking: Đọc file lớn từng phần nhỏ để tiết kiệm RAM.

2.  Merge Sort: Sử dụng heapq để đồng bộ hóa thời gian từ 4 nguồn dữ liệu khác nhau, đảm bảo sự kiện được phát lại đúng trình tự lịch sử.


## B. Preprocessing Layer (src/preprocess.py)

**Nhiệm vụ:** Chuẩn hóa dữ liệu thô thành dạng tiêu chuẩn (JSON/Dictionary).

**Xử lý:**

* Tách User@Domain -> User, Domain.

* Gắn nhãn Is_Machine (Máy tính vs Người dùng).

* Map Protocol ID sang tên (6 -> TCP).

## C. Detection Engine (src/detection.py)
**Kiến trúc:** Plugin-based (Sử dụng Abstract Base Class).

**Thành phần:**

1. SignatureBasedDetector (Đang chạy): Kiểm tra đối chiếu với tập luật cứng (Hard-coded rules) và Danh sách đen (Threat Intel).

2. AnomalyDetector (Future): Module chờ sẵn để tích hợp Model AI/Deep Learning.

3. Engine Core: Quản lý và phân phối log tới tất cả các Detector con.

## D. Alert & Storage (src/alert.py)
**Database:** SQLite (alert.db) đặt tại Root Project.

**Schema:**

1. id: Auto Increment.

2. timestamp: Thời gian thực hệ thống phát hiện.

3. log_time: Thời gian sự kiện trong log.

4. severity: Mức độ (HIGH, MEDIUM, LOW).

5. raw_data: Lưu trữ toàn bộ log gốc (JSON) để phục vụ Forensics/Re-train AI.

## E. Visualization (src/dashboard.py)
**Framework:** Flask (Python).
* Dashboard (Flask): Hiển thị cảnh báo thời gian thực.

* AI Metrics: Biểu đồ tròn so sánh tỷ lệ phát hiện giữa Luật và AI, đếm số lượng bất thường do AI tìm ra.

**Cơ chế:** Đọc dữ liệu từ alert.db độc lập với luồng xử lý chính.

**Tính năng:**

1. Live Monitor (Auto-refresh 3s).

2. Thống kê Severity.

3. Hiển thị chi tiết Alert.


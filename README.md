# Real-time Multi-Input S.O.C System

> Hệ thống giám sát an ninh mạng thời gian thực xử lý đa nguồn dữ liệu (Log, Network Flow, Process).

## Giới thiệu
Dự án mô phỏng một trung tâm S.O.C (Security Operations Center) thu nhỏ. Hệ thống có khả năng tiếp nhận luồng dữ liệu khổng lồ (Big Data) từ dataset LANL Cyber-Security, đồng bộ hóa thời gian thực và phát hiện các cuộc tấn công mạng.

## Tính năng chính
* **Multi-Input Handling:** Xử lý đồng bộ 4 nguồn: Auth, Process, DNS, Flows.
* **High Performance:** Core xử lý ~80.000 sự kiện/giây trên máy cá nhân.
* **Real-time Engine:** Cơ chế Streaming giả lập thời gian thực.
* **Detection System:** Tích hợp phát hiện dựa trên Chữ ký (Signature) và Bất thường (Anomaly).

## 📂 Tài liệu dự án (Documentation)
Để tránh thông tin quá tải, chi tiết kỹ thuật được chia nhỏ tại thư mục `docs/`:

1.  [ **Architecture:**](./docs/architecture.md) Sơ đồ luồng dữ liệu và thiết kế hệ thống.
2.  [ **Dataset Schema:**](./docs/dataset_schema.md) Chi tiết về bộ dữ liệu LANL (Metadata, ý nghĩa các cột).
3.  [ **Project Plan:**](./docs/plan.md) Lộ trình phát triển 30 Tasks và tiến độ hiện tại.
4.  [ **Changelog:**](./CHANGELOG.md) Nhật ký thay đổi và cập nhật phiên bản.

## Cài đặt & Sử dụng (Quick Start)

### 1. Yêu cầu
* Python 3.8+

### 2. Cài đặt
```bash
# Clone dự án
git clone [https://github.com/OnlyD05905/Multi-Input_handle.git](https://github.com/OnlyD05905/Multi-Input_handle.git)
cd Multi-Input_handle

# Tạo môi trường ảo (Khuyến nghị)
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt thư viện
pip install -r requirements.txt
```
### 3. Chạy hệ thống
```bash
python src/main.py
```

## Cấu trúc thư mục
```text
/
MULTI-INPUT_HANDLE/
├── alerts.db           # Database cảnh báo (SQLite)
├── data/raw/           # Nơi chứa dataset (.gz)
├── docs/               # Tài liệu kỹ thuật chi tiết
├── src/                # Source code chính
│   ├── config.py       # Cấu hình
│   ├── streamer.py     # Engine đọc dữ liệu
│   ├── main.py         # File khởi chạy
│   └── ...
├── notebooks/          # Code thử nghiệm
└── CHANGELOG.md        # Lịch sử cập nhật
```

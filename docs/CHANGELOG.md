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
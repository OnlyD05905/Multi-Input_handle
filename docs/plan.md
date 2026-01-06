# Project Plan: Real-time Multi-Input S.O.C (Scalable Architecture)

Dự án xây dựng hệ thống giám sát an ninh mạng (S.O.C) với khả năng xử lý đa luồng dữ liệu, phát hiện tấn công (Signature & AI) và trực quan hóa Real-time.

---

## ✅ Phase 1: Foundation & Architecture (Nền móng)
- [x] **Task 01:** Thiết lập cấu trúc dự án chuẩn (`src/`, `docs/`, `data/`).
- [x] **Task 02:** Xây dựng `config.py` và `utils.py` (Logging, Path validation).
- [x] **Task 03:** Xây dựng `streamer.py` (Base): Đọc file log nén `.gz` bằng kỹ thuật Chunking.
- [x] **Task 04:** Xây dựng `main.py` (V1): Chạy thử luồng đơn.

## ✅ Phase 2: Multi-Input Streaming (Xử lý Đa luồng)
- [x] **Task 05:** Nâng cấp `MultiLogStreamer`: Đọc song song 4 nguồn (Auth, Proc, Flows, DNS).
- [x] **Task 06:** Thuật toán Time Synchronization: Sử dụng `heapq` để hợp nhất dòng chảy sự kiện theo thời gian thực.
- [x] **Task 07:** Chế độ Test linh hoạt: Hỗ trợ flag `TEST_MODE` ('all', 'auth', 'flows'...).

## ✅ Phase 3: Preprocessing (Tiền xử lý & Làm sạch)
- [x] **Task 08:** Xây dựng `LogPreprocessor`: Class chuyên biệt để làm sạch dữ liệu.
- [x] **Task 09:** Logic Parse: Tách `User@Domain`, chuẩn hóa Protocol (6->TCP), gắn nhãn Machine Account (`$`).
- [x] **Task 10:** Tích hợp Preprocessor vào Pipeline chính.

## ✅ Phase 4: Detection Engine Core (Bộ não phát hiện - V1)
- [x] **Task 11:** Thiết kế kiến trúc Modular Detection: Sử dụng `BaseDetector` (Interface) để dễ mở rộng.
- [x] **Task 12:** Implement `SignatureBasedDetector`: Module phát hiện dựa trên luật cứng.
- [x] **Task 13:** Rule 01 (Authentication): Phát hiện `ANONYMOUS LOGON` và Blacklisted Users.
- [x] **Task 14:** Tích hợp Engine vào `main.py`: Cơ chế sinh Alert object khi có vi phạm.

## ✅ Phase 5: Alert Management & Storage (Lưu trữ)
- [x] **Task 15:** Thiết kế Database (SQLite): Schema bảng `alerts` lưu trữ lịch sử tấn công.
- [x] **Task 16:** Xây dựng `AlertDatabase`: Module quản lý kết nối, tự động ghi log vào `alert.db` tại Root.
- [x] **Task 17:** Kết nối Full-Flow: Detection -> Alert -> Save to DB.

## ✅ Phase 6: Visualization (Hiển thị)
- [x] **Task 18:** Xây dựng Web Dashboard (Flask): Backend API đọc dữ liệu từ SQLite.
- [x] **Task 19:** Frontend UI (HTML/CSS/Bootstrap): Giao diện Dark Mode, Auto-refresh sau mỗi 3s.
- [x] **Task 20:** End-to-End Test: Chạy song song 2 Terminal (Scan & Dashboard) thành công.

---

## 🚧 Phase 7: Advanced Signature Rules (Nâng cấp luật)
*Mục tiêu: Đa dạng hóa các loại cảnh báo để Dashboard hiển thị phong phú hơn trước khi qua AI.*

- [ ] **Task 21:** **Rule 02 (Network):** Phát hiện Port Scan (1 IP kết nối tới > N cổng trong 1s).
- [ ] **Task 22:** **Rule 03 (Process):** Phát hiện chuỗi tiến trình độc hại (VD: Word -> PowerShell -> CMD).
- [ ] **Task 23:** **Rule 04 (Volume):** Phát hiện Data Exfiltration (Gửi lượng byte lớn bất thường ra ngoài).

## 🔮 Phase 8: AI Integration & Real-time (Tương lai)
*Mục tiêu: Tích hợp Deep Learning và chuyển sang bắt gói tin mạng thật.*

- [ ] **Task 24:** **[AI Module]** Xây dựng `AnomalyDetector` (kế thừa `BaseDetector`): Load model Deep Learning (.h5/.pkl).
- [ ] **Task 25:** **[Traffic]** Tích hợp thư viện `PyShark`/`Scapy` để bắt gói tin Live từ Card mạng.
- [ ] **Task 26:** **[Architecture]** Chuyển đổi cơ chế ghi DB sang Asynchronous (Redis/Celery) để chịu tải cao.
- [ ] **Task 27:** **[Dashboard]** Nâng cấp Web Socket (SocketIO) để đẩy Alert thời gian thực (thay vì Refresh trang).

---
*Last updated: 06/01/2026*
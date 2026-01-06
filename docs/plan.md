# Project Plan: Real-time Multi-Input S.O.C

Tiến độ dự án được chia thành 6 giai đoạn (Phases). Mục tiêu là xây dựng hệ thống giám sát an ninh mạng từ cơ bản (đọc file log) đến nâng cao (bắt gói tin thực tế và Web Dashboard).

---

## Phase 1: Foundation & Architecture (Xây nền móng)
*Mục tiêu: Thiết lập cấu trúc dự án chuẩn, cấu hình hệ thống và chạy thử luồng dữ liệu đơn giản.*

- [x] **Task 01:** Dọn dẹp thư mục cũ & Tạo cấu trúc file chuẩn (`src/`, `docs/`, `notebooks/`).
- [x] **Task 02:** Viết `src/config.py`: Định nghĩa đường dẫn Dataset và các tham số (Chunk size, Thresholds).
- [x] **Task 03:** Viết `src/utils.py`: Tạo hàm kiểm tra file và thiết lập Logging (thay cho print thường).
- [x] **Task 04:** Viết `src/streamer.py` (Version 1): Chuyển code đọc file `auth.txt.gz` cũ vào Class chuyên biệt.
- [x] **Task 05:** Viết `src/main.py` (Version 1): Chạy thử tích hợp (Import Config -> Gọi Streamer -> In ra màn hình).

---

## Phase 2: Multi-Input Streaming (Xử lý Đa luồng)
*Mục tiêu: Đọc và đồng bộ hóa thời gian từ cả 4 nguồn dữ liệu (Auth, Proc, DNS, Flow).*

- [x] **Task 06:** Nâng cấp `streamer.py`: Tạo class `MultiStreamer` có khả năng mở 4 file cùng lúc.
- [x] **Task 07:** Logic "Time Synchronization": Đảm bảo log từ các nguồn khác nhau được phát ra đúng trình tự thời gian (Giây thứ 1 của Auth phải đi cùng Giây thứ 1 của Flow).
- [x] **Task 08:** Test đồng bộ: Chạy `main.py` để in ra dòng chảy dữ liệu hỗn hợp (VD: 1 dòng Auth xen kẽ 1 dòng DNS).

---

## Phase 3: Preprocessing (Tiền xử lý dữ liệu)
*Mục tiêu: Làm sạch, chuẩn hóa dữ liệu thô thành dạng máy hiểu được.*

- [x] **Task 09:** Viết `src/preprocess.py` - Phần Auth: Tách `User@Domain`, xử lý Machine Account (`$`).
- [x] **Task 10:** Viết `src/preprocess.py` - Phần Flows: Chuẩn hóa IP, Port, tính toán Duration.
- [x] **Task 11:** Viết `src/preprocess.py` - Phần Proc & DNS: Lọc nhiễu, chuẩn hóa tên tiến trình/tên miền.
- [x] **Task 12:** Tích hợp Preprocess vào `main.py`: Dữ liệu từ Streamer -> Preprocess -> In kết quả sạch.

---

## Phase 4: Detection Engine (Bộ não phát hiện)
*Mục tiêu: Xây dựng các luật (Rules) để phát hiện tấn công.*

- [ ] **Task 13:** Viết `src/detection.py`: Tạo khung Class `Detector` và hàm `load_threat_intel`.
- [ ] **Task 14:** Implement Threat Intel: Nạp file `redteam.txt` vào bộ nhớ (Set/Dictionary) để tra cứu nhanh.
- [ ] **Task 15:** **Rule 01 (Signature):** So khớp chính xác log hiện tại với danh sách Redteam (Phát hiện 100%).
- [ ] **Task 16:** **Rule 02 (Network - Port Scan):** Phát hiện 1 IP nguồn kết nối tới > N cổng đích khác nhau trong 1 giây (Dựa trên `flows`).
- [ ] **Task 17:** **Rule 03 (Volume - Data Exfiltration):** Phát hiện lượng Byte gửi đi vượt quá ngưỡng cho phép (Dựa trên `flows`).
- [ ] **Task 18:** **Rule 04 (Behavior - Suspicious Process):** Phát hiện tiến trình lạ hoặc đăng nhập vào khung giờ bất thường.

---

## Phase 5: Alerting & Storage (Cảnh báo & Lưu trữ)
*Mục tiêu: Thông báo khi có tấn công và lưu lại bằng chứng.*

- [ ] **Task 19:** Viết `src/alert.py`: Tạo hàm in cảnh báo ra Console với màu sắc (Đỏ: Nguy hiểm, Vàng: Cảnh báo).
- [ ] **Task 20:** **[Learning]** Tìm hiểu SQLite và thư viện `sqlite3` trong Python.
- [ ] **Task 21:** Viết hàm `save_to_db` trong `alert.py`: Thiết kế bảng `alerts` và lưu cảnh báo vào file `alerts.db`.
- [ ] **Task 22:** Hoàn thiện Pipeline trong `main.py`: Stream -> Preprocess -> Detect -> Alert -> DB.

---

## Phase 6: Advanced Real-time & Dashboard (Nâng cao)
*Mục tiêu: Chuyển sang giám sát mạng thật (Live) và giao diện trực quan.*

- [ ] **Task 23:** Refactor Code: Tối ưu hóa hiệu năng, đo thời gian xử lý (Latency).
- [ ] **Task 24:** Whitelist Mechanism: Thêm cơ chế bỏ qua các IP/User tin cậy trong `config.py`.
- [ ] **Task 25:** **[Learning]** Tìm hiểu thư viện **PyShark** (Wireshark Wrapper).
- [ ] **Task 26:** Viết `tests/test_pyshark.py`: Thử code bắt gói tin thật từ Wifi/LAN của máy cá nhân.
- [ ] **Task 27:** Live Mode Integration: Cập nhật `streamer.py` để hỗ trợ chế độ `mode='live'` (dùng Pyshark) bên cạnh `mode='file'`.
- [ ] **Task 28:** **[Learning]** Tìm hiểu Framework **Streamlit**.
- [ ] **Task 29:** Viết `dashboard.py`: Dựng Web đọc dữ liệu từ `alerts.db` và hiển thị biểu đồ Real-time.
- [ ] **Task 30:** Final Test & Documentation: Kiểm tra toàn bộ hệ thống, cập nhật hướng dẫn sử dụng.

---
*Last updated: [5/1/2026]*
# Đây là về hệ thống xử lý đa đầu vào nhằm mục đích từ nhiều input ( network flow, log,..) sẽ được gộp lại để phù hợp cho hệ thống early warning system

Về Dataset, tôi sẽ dùng dataset "LANL Unified Host and Network Data Set", cụ thể là "Comprehensive, Multi-Source Cyber-Security Events".

## Metadata của dataset:

Đây là một bộ dữ liệu an ninh mạng toàn diện và đa nguồn từ Phòng thí nghiệm Quốc gia Los Alamos (LANL).

* **Thời gian thu thập:** Dữ liệu được thu thập liên tục trong 58 ngày.
* **Nguồn dữ liệu:** Dữ liệu được tổng hợp từ 5 nguồn khác nhau bên trong mạng nội bộ của LANL, bao gồm:
    * Log Xác thực (Authentication events): Từ các máy Windows cá nhân và máy chủ Active Directory.
    * Log Tiến trình (Process events): Ghi lại các tiến trình (process) bắt đầu và kết thúc trên máy Windows.
    * Log DNS: Ghi lại các truy vấn DNS từ máy chủ DNS nội bộ.
    * Dữ liệu Luồng Mạng (Network flow): Thu thập từ mạng.
* **Quy mô:** Bộ dữ liệu này rất lớn, bao gồm:
    * Tổng cộng 1,64 tỷ sự kiện (events).
    * Liên quan đến 12.425 người dùng (users) và 17.684 máy tính (computers).
    * Dung lượng nén khoảng 12 GB.
* **Đặc điểm nổi bật:** Dữ liệu đã được ẩn danh (de-identified) để bảo mật. Dữ liệu thời gian (time) bắt đầu từ 1 và tính theo giây.

---

## Mô tả nhanh các file có trong dataset:

### 1. 📂 auth.txt.gz (Log Xác thực):

* **Nguồn gốc:** Thu thập từ các máy tính Windows cá nhân và các máy chủ Active Directory (máy chủ quản lý danh tính).
* **Phân tích các trường (cột):**
    * `time`: Thời gian (tính bằng giây).
    * `source user@domain` & `destination user@domain`: Ai là người/máy tính khởi tạo yêu cầu xác thực, và họ đang cố gắng trở thành ai.
    * `source computer` & `destination computer`: Yêu cầu đi từ máy nào và nhắm đến máy nào.
    * `authentication type`: Kiểu xác thực (ví dụ: Kerberos, NTLM...).
    * `logon type`: Kiểu đăng nhập (ví dụ: Đăng nhập từ xa, đăng nhập tương tác tại máy...).
    * `authentication orientation`: Hướng (ví dụ: Log on, Log off, hay chỉ là yêu cầu xác thực).
    * `success/failure`: Trạng thái (Thành công/Thất bại).

<img width="1000" height="190" alt="image" src="https://github.com/user-attachments/assets/6ca621fb-f43d-485f-b0a3-9a650f7f7401" />

### 2. 📂 proc.txt.gz (Log Tiến trình):

* **Nguồn gốc:** Thu thập từ các máy tính Windows cá nhân.
* **Phân tích các trường (cột):**
    * `time`: Thời gian.
    * `user@domain`: Người dùng nào đã thực thi tiến trình.
    * `computer`: Tiến trình chạy trên máy tính nào.
    * `process name`: Tên của tiến trình (ví dụ: chrome.exe, powershell.exe).
    * `start/end`: Ghi lại sự kiện bắt đầu hay kết thúc của tiến trình.

<img width="995" height="189" alt="image" src="https://github.com/user-attachments/assets/4225060d-f25a-45d5-8770-b34e0df6891f" />


### 3. 📂 dns.txt.gz (Log DNS):

* **Nguồn gốc:** Thu thập từ các máy chủ DNS nội bộ (máy chủ "phiên dịch" tên miền).
* **Phân tích các trường (cột):**
    * `time`: Thời gian.
    * `source computer`: Máy tính nào đã thực hiện tra cứu.
    * `computer resolved`: Tên miền (hoặc máy tính) đã được tra cứu.

<img width="968" height="188" alt="image" src="https://github.com/user-attachments/assets/b789f3e9-a0f9-4ca2-99d9-b435590a542f" />

### 4. 📂 flows.txt.gz (Luồng Mạng):

* **Nguồn gốc:** Thu thập từ các router nội bộ.
* **Phân tích các trường (cột):**
    * `time`: Thời gian.
    * `duration`: Thời lượng của luồng.
    * `source computer` & `destination computer`: Máy nguồn và máy đích.
    * `source port` & `destination port`: Cổng nguồn và cổng đích.
    * `protocol`: Giao thức (ví dụ: 6=TCP, 17=UDP).
    * `packet count`: Số lượng gói tin.
    * `byte count`: Số lượng bytes (dung lượng).

<img width="996" height="184" alt="image" src="https://github.com/user-attachments/assets/844505c0-575f-4360-ab46-ad3e519e17e4" />

---

## 📂 Cấu trúc Thư mục

```
/
├── data/
│   ├── raw/        # Chứa dữ liệu gốc (.gz) từ LANL
│   └── processed/  # Chứa dữ liệu đã được xử lý và gộp lại
├── notebooks/      # Chứa các file Jupyter Notebook để khám phá, thử nghiệm
├── src/            # Chứa code Python .py chính thức của dự án
│   ├── data_processing.py  # Script xử lý và gộp dữ liệu
│   ├── model.py            # Định nghĩa kiến trúc mô hình đa đầu vào
│   └── train.py            # Script để huấn luyện mô hình
├── models/         # Nơi lưu trữ các file model đã huấn luyện (.h5)
└── requirements.txt  # Danh sách các thư viện Python cần thiết
```

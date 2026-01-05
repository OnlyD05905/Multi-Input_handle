# Dataset Specification

**Dataset Name:** LANL Unified Host and Network Data Set (Comprehensive, Multi-Source Cyber-Security Events).

## 1. Metadata tổng quan
* **Thời gian thu thập:** 58 ngày liên tục.
* **Quy mô:** 1.64 tỷ sự kiện, 12.425 users, 17.684 máy tính.
* **Dung lượng:** ~12 GB (nén).
* **Đặc điểm:** Dữ liệu đã ẩn danh, Time bắt đầu từ 0.

## 2. Chi tiết các file thành phần
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

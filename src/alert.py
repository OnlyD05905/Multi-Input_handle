import sqlite3
import json
import os
from datetime import datetime

class AlertDatabase:
    def __init__(self, db_name="alert.db"):
        # --- QUẢN LÝ ĐƯỜNG DẪN (SCALABILITY) ---
        # Lấy đường dẫn của file alert.py hiện tại
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Nhảy ra ngoài 1 cấp để về thư mục gốc (MULTI-INPUT_HANDLE)
        root_dir = os.path.dirname(current_dir)
        # Nối đường dẫn: root + alert.db
        self.db_path = os.path.join(root_dir, db_name)
        
        self._init_db()

    def _init_db(self):
        """Khởi tạo bảng nếu chưa tồn tại."""
        try:
            # Kết nối tới db_path đã định vị chính xác
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            query = """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                log_time INTEGER,
                source TEXT,
                severity TEXT,
                title TEXT,
                description TEXT,
                raw_data TEXT
            )
            """
            cursor.execute(query)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"DB Init Error: {e}")

    def save_alert(self, alert):
        """Lưu cảnh báo vào DB."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_data = alert.get('log_data', {})
            
            cursor.execute("""
                INSERT INTO alerts (timestamp, log_time, source, severity, title, description, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                current_time,
                log_data.get('Time', 0),
                log_data.get('Log_Source', 'unknown'),
                alert.get('severity', 'INFO'),
                alert.get('title', 'Unknown Alert'),
                alert.get('description', ''),
                json.dumps(log_data)
            ))

            conn.commit()
            conn.close()
        except Exception as e:
            print(f"DB Save Error: {e}")

    def get_recent_alerts(self, limit=10):
        """Lấy danh sách alert mới nhất."""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            print(f"DB Read Error: {e}")
            return []
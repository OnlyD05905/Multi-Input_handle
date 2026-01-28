from flask import Flask, render_template
from alert import AlertDatabase
import os

# Định nghĩa đường dẫn tới thư mục template (giao diện HTML)
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=template_dir)

# Kết nối lại với Database
db = AlertDatabase()

@app.route('/')
def index():
    # 1. Lấy 50 cảnh báo mới nhất từ DB
    recent_alerts = db.get_recent_alerts(limit=100)
    
    # 2. Thống kê nhanh (Logic đơn giản để hiển thị số liệu)
    stats = {
        'total': len(recent_alerts),
        'high_severity': sum(1 for a in recent_alerts if a['severity'] == 'HIGH'),
        # [MỚI] Đếm số alert có chữ '(AI)' trong tiêu đề
        'ai_anomalies': sum(1 for a in recent_alerts if '(AI)' in a['title'])
    }
    
    # 3. Trả về giao diện HTML kèm dữ liệu
    return render_template('dashboard.html', alerts=recent_alerts, stats=stats)

if __name__ == '__main__':
    # Chạy web server ở port 5000
    print(" running at: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
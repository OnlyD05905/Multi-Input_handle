import numpy as np
from sklearn.ensemble import IsolationForest
from interfaces import BaseDetector

class AnomalyDetector(BaseDetector):
    def __init__(self, training_size=1000, contamination=0.01):
        """
        training_size: Số lượng log dùng để học 'bình thường' trước khi bắt đầu dự đoán.
        contamination: Tỷ lệ nhiễu ước tính (0.01 = kỳ vọng 1% là tấn công).
        """
        self.model = IsolationForest(n_estimators=100, contamination=contamination, random_state=42)
        self.training_data = []
        self.training_size = training_size
        self.is_trained = False
        
        # Chỉ quan tâm đến các trường số liệu quan trọng để tìm bất thường
        # Ví dụ: Byte gửi đi, Cổng đích, Thời gian (Logon Type)...
        # Ở đây demo đơn giản với 'Byte_Count' của Flows
        self.features = ['Byte_Count']

    def _extract_features(self, log):
        """Chuyển đổi Log Dictionary thành Vector số học cho AI"""
        # Chỉ xử lý log FLOWS vì nó có số liệu rõ ràng (Bytes)
        if log.get('Log_Source') != 'flows':
            return None
        
        try:
            byte_count = int(log.get('Byte_Count', 0))
            # Reshape để phù hợp input của sklearn (mảng 2 chiều)
            return [byte_count] 
        except:
            return None

    def detect(self, log):
        alerts = []
        
        # 1. Trích xuất đặc trưng (Feature Extraction)
        features = self._extract_features(log)
        if not features:
            return []

        # 2. Giai đoạn Học (Training Phase)
        if not self.is_trained:
            self.training_data.append(features)
            
            # Nếu đã gom đủ dữ liệu mẫu -> Train model ngay lập tức
            if len(self.training_data) >= self.training_size:
                print(f"[AI] Training Isolation Forest on {self.training_size} samples...")
                self.model.fit(self.training_data)
                self.is_trained = True
                print("[AI] Model Trained! Switching to Prediction Mode.")
                # Giải phóng bộ nhớ
                self.training_data = [] 
            return []

        # 3. Giai đoạn Dự đoán (Prediction Phase)
        # Model trả về -1 là Bất thường, 1 là Bình thường
        # reshape(1, -1) vì ta đang dự đoán 1 mẫu đơn lẻ
        prediction = self.model.predict([features])
        
        if prediction[0] == -1:
            # Tính điểm bất thường (Anomaly Score) - càng âm càng dị biệt
            score = self.model.decision_function([features])[0]
            
            alerts.append({
                'title': 'Traffic Anomaly Detected (AI)',
                'severity': 'MEDIUM', # Để Medium vì AI có thể nhận nhầm (False Positive)
                'description': f"Unusual data volume detected by AI. Anomaly Score: {score:.4f}",
                'log_data': log
            })
            
        return alerts
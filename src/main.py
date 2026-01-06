import sys
import time
import config
from utils import setup_logger, validate_paths
from streamer import LogStreamer
from preprocess import LogPreprocessor
from detection import DetectionEngine
from alert import AlertDatabase  

logger = setup_logger()
TEST_MODE = 'all' 

def main():
    if not validate_paths({'Red Team': config.REDTEAM_FILE}):
        sys.exit(1)

    logger.info(f"Initializing SOC System | Mode: {TEST_MODE.upper()}")
    
    # 1. Khởi tạo các module
    streamer = LogStreamer(target_source=TEST_MODE)
    preprocessor = LogPreprocessor()
    detector = DetectionEngine()
    db = AlertDatabase()  # <--- [MỚI] Kết nối Database
    
    count = 0
    start_time = time.time()
    stats = {'processed': 0, 'alerts': 0}

    try:
        logger.info("System Started. Monitoring stream...")
        
        for raw_log in streamer.stream():
            count += 1
            
            # --- PHASE 3: PREPROCESS ---
            log = preprocessor.process(raw_log)
            source = log.get('Log_Source', 'unknown')

            # --- PHASE 4: DETECTION ---
            alerts = detector.analyze(log)
            
            # --- PHASE 5: ALERT MANAGEMENT (CẬP NHẬT) ---
            if alerts:
                stats['alerts'] += len(alerts)
                for alert in alerts:
                    # 1. In ra màn hình (Console Output)
                    print(f"\n[ALERT] [{alert['severity']}] {alert['title']}")
                    print(f"   Description: {alert['description']}")
                    print(f"   Source: {source.upper()} | Time: {log['Time']}")
                    
                    # 2. [MỚI] Lưu vào Database
                    db.save_alert(alert)
                    print("   [DB] Saved to alerts.db")
                    print("-" * 50)

            # Báo cáo tiến độ
            if count % 20000 == 0:
                elapsed = time.time() - start_time
                speed = int(count / elapsed) if elapsed > 0 else 0
                sys.stdout.write(f"\rScan: {count:,} events | Speed: {speed} ev/s | Alerts: {stats['alerts']}")
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n")
        logger.info("Stopped by user.")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\n")
        logger.info(f"Total processed: {count}")
        logger.info(f"Total Alerts Triggered: {stats['alerts']}")

if __name__ == "__main__":
    main()
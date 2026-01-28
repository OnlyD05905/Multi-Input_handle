import sys
import time
import config # <--- Import config
from utils import setup_logger, validate_paths
from streamer import LogStreamer 
from live_streamer import LiveStreamer 
from preprocess import LogPreprocessor
from detection import DetectionEngine
from alert import AlertDatabase

# (ĐÃ XÓA) CONFIGURATION HARD-CODED CŨ

logger = setup_logger()

def main():
    # Lấy chế độ chạy từ config
    run_mode = config.DEFAULT_RUN_MODE
    logger.info(f"System Starting | Mode: {run_mode}")
    
    if run_mode == 'FILE':
        if not validate_paths({'Red Team': config.REDTEAM_FILE}):
            sys.exit(1)
        streamer = LogStreamer(target_source='all')
    else:
        try:
            # Khởi tạo LiveStreamer (tự động lấy interface từ config)
            streamer = LiveStreamer() 
        except Exception as e:
            logger.error(f"Streamer Init Error: {e}")
            sys.exit(1)

    preprocessor = LogPreprocessor()
    detector = DetectionEngine()
    db = AlertDatabase()
    
    count = 0
    stats = {'alerts': 0}

    try:
        for raw_log in streamer.stream():
            if raw_log is None: break
            count += 1
            
            if run_mode == 'FILE':
                log = preprocessor.process(raw_log)
            else:
                log = raw_log 

            alerts = detector.analyze(log)
            
            if alerts:
                stats['alerts'] += len(alerts)
                for alert in alerts:
                    print(f"\n[ALERT] [{alert['severity']}] {alert['title']}")
                    print(f"Desc: {alert['description']}")
                    if 'Dest_IP' in log:
                        print(f"Flow: {log.get('Source_IP')} -> {log.get('Dest_IP')}:{log.get('Dest_Port')}")
                    db.save_alert(alert)

            if count % 50 == 0:
                sys.stdout.write(f"\r[STATUS] Packets: {count} | Alerts: {stats['alerts']}")
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n[INFO] Stopped by user.")
    except Exception as e:
        logger.error(f"Runtime Error: {e}")
    finally:
        print(f"\n[INFO] Session Closed. Total processed: {count}")

if __name__ == "__main__":
    main()
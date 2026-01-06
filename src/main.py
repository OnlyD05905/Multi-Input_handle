import sys
import time
import config
from utils import setup_logger, validate_paths
from streamer import LogStreamer

logger = setup_logger()

# --- CẤU HÌNH CHẾ ĐỘ CHẠY ---
# Options: 'all', 'auth', 'proc', 'flows', 'dns'
TEST_MODE = 'all' 

def main():
    if not validate_paths({'Red Team': config.REDTEAM_FILE}):
        sys.exit(1)

    logger.info(f"Initializing SOC System | Mode: {TEST_MODE.upper()}")
    
    # Truyền chế độ muốn test vào Streamer
    streamer = LogStreamer(target_source=TEST_MODE)
    
    count = 0
    start_time = time.time()
    stats = {}

    try:
        for log in streamer.stream():
            count += 1
            
            # Thống kê loại log
            source = log.get('Log_Source', 'unknown')
            stats[source] = stats.get(source, 0) + 1

            # In thử 15 dòng đầu
            if count <= 15:
                print(f"[DEBUG] [{source.upper()}] Time: {log['Time']} | Data: {str(log)[:60]}...")

            if count % 20000 == 0:
                elapsed = time.time() - start_time
                speed = int(count / elapsed) if elapsed > 0 else 0
                logger.info(f"Processed {count} events. Speed: {speed} ev/s. Stats: {stats}")

    except KeyboardInterrupt:
        logger.info("Stopped by user.")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        
    finally:
        logger.info(f"Total processed: {count}")
        logger.info(f"Final Stats: {stats}")

if __name__ == "__main__":
    main()
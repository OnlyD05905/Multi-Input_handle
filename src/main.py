import sys
import time
import config
from utils import setup_logger, validate_paths
from streamer import LogStreamer

logger = setup_logger()

def main():
    required_files = {
        'Auth Log': config.AUTH_FILE,
        'Red Team Log': config.REDTEAM_FILE
    }
    
    if not validate_paths(required_files):
        logger.error("Missing required datasets. Exiting.")
        sys.exit(1)

    logger.info("Initializing SOC System...")
    logger.info(f"Target dataset: {config.AUTH_FILE}")

    streamer = LogStreamer(config.AUTH_FILE)
    
    count = 0
    start_time = time.time()

    try:
        for log in streamer.stream():
            count += 1
            
            if count % 10000 == 0:
                elapsed = time.time() - start_time
                logger.info(f"Processed {count} logs. Time elapsed: {elapsed:.2f}s")

            # Demo: Print first 3 logs then stop printing
            if count <= 3:
                print(f"[DEBUG] {log.to_dict()}")

    except KeyboardInterrupt:
        logger.info("Process interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        logger.info("System shutting down.")

if __name__ == "__main__":
    main()
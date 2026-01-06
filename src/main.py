import sys
import time
import config
from utils import setup_logger, validate_paths
from streamer import LogStreamer
from preprocess import LogPreprocessor 

logger = setup_logger()

# --- CẤU HÌNH CHẾ ĐỘ CHẠY ---
# Options: 'all', 'auth', 'proc', 'flows', 'dns'
TEST_MODE = 'all' 

def main():
    if not validate_paths({'Red Team': config.REDTEAM_FILE}):
        sys.exit(1)

    logger.info(f"Initializing SOC System | Mode: {TEST_MODE.upper()}")
    
    # 1. Khởi tạo Streamer (Vòi nước)
    streamer = LogStreamer(target_source=TEST_MODE)
    
    # 2. Khởi tạo Preprocessor (Bộ lọc)
    preprocessor = LogPreprocessor()
    
    count = 0
    start_time = time.time()
    stats = {}

    try:
        # Vòng lặp xử lý
        for raw_log in streamer.stream():
            count += 1
            
            # --- BƯỚC TIỀN XỬ LÝ QUAN TRỌNG ---
            # Dữ liệu đi qua bộ lọc để làm sạch và thêm trường thông tin
            log = preprocessor.process(raw_log)
            
            # Thống kê loại log
            source = log.get('Log_Source', 'unknown')
            stats[source] = stats.get(source, 0) + 1

            # In thử 15 dòng đầu
            if count <= 15:
                # Code mới: In ra các trường đã xử lý để kiểm tra
                if source == 'auth':
                    print(f"[DEBUG] [AUTH] User: {log.get('Source_User')} | Machine?: {log.get('Is_Machine_Src')}")
                elif source == 'flows':
                    print(f"[DEBUG] [FLOWS] Protocol: {log.get('Protocol_Name')} | Count: {log.get('Packet_Count')}")
                else:
                    # In 200 ký tự để nhìn thấy phần đuôi
                    print(f"[DEBUG] [{source.upper()}] Data: {str(log)[-200:]}...") # In 200 ký tự cuối cùng

            # Báo cáo định kỳ
            if count % 20000 == 0:
                elapsed = time.time() - start_time
                speed = int(count / elapsed) if elapsed > 0 else 0
                logger.info(f"Processed {count} events. Speed: {speed} ev/s. Stats: {stats}")

    except KeyboardInterrupt:
        logger.info("Stopped by user.")
    except Exception as e:
        logger.error(f"Critical error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        logger.info(f"Total processed: {count}")
        logger.info(f"Final Stats: {stats}")

if __name__ == "__main__":
    main()
#---------------------<print file JSon>-------------------------------#
# import sys
# import time
# import config
# import json  # <--- [MỚI] Thêm thư viện này
# from utils import setup_logger, validate_paths
# from streamer import LogStreamer
# from preprocess import LogPreprocessor

# logger = setup_logger()
# TEST_MODE = 'all' 

# def main():
#     if not validate_paths({'Red Team': config.REDTEAM_FILE}):
#         sys.exit(1)

#     logger.info(f"Initializing SOC System | Mode: {TEST_MODE.upper()}")
    
#     streamer = LogStreamer(target_source=TEST_MODE)
#     preprocessor = LogPreprocessor()
    
#     count = 0
#     start_time = time.time()
#     stats = {}

#     # [MỚI] Mở file để ghi mẫu báo cáo (chế độ 'w' - ghi mới)
#     sample_file = open("sample_report.json", "w", encoding="utf-8")

#     try:
#         for raw_log in streamer.stream():
#             count += 1
#             log = preprocessor.process(raw_log)
            
#             source = log.get('Log_Source', 'unknown')
#             stats[source] = stats.get(source, 0) + 1

#             # --- [MỚI] TÍNH NĂNG XUẤT BÁO CÁO MẪU ---
#             # Thay vì in ra màn hình, ta ghi full dữ liệu vào file
#             if count <= 1000: # Lưu 1000 dòng đầu tiên
#                 # json.dumps giúp biến Dictionary thành chuỗi text đẹp
#                 sample_file.write(json.dumps(log, default=str) + "\n")
            
#             # In debug gọn nhẹ ra màn hình để biết code đang chạy
#             if count <= 5:
#                 print(f"[DEBUG] Processing: {source.upper()} - Time: {log['Time']}")

#             # Báo cáo định kỳ
#             if count % 20000 == 0:
#                 elapsed = time.time() - start_time
#                 speed = int(count / elapsed) if elapsed > 0 else 0
#                 logger.info(f"Processed {count} events. Speed: {speed} ev/s. Stats: {stats}")
                
#                 # [MỚI] Đóng file mẫu sau khi đã ghi đủ để tiết kiệm tài nguyên
#                 if count > 1000 and not sample_file.closed:
#                     sample_file.close()
#                     logger.info("✅ Đã xuất file mẫu 'sample_report.json' thành công!")

#     except KeyboardInterrupt:
#         logger.info("Stopped by user.")
#     except Exception as e:
#         logger.error(f"Critical error: {e}")
#     finally:
#         if not sample_file.closed:
#             sample_file.close()
#         logger.info(f"Total processed: {count}")

# if __name__ == "__main__":
#     main()
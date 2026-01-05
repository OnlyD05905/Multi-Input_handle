import os
import sys
import logging

def setup_logger(name="SOC_Logger"):
    """
    Thiết lập hệ thống ghi log (thay thế cho print truyền thống).
    Giúp in ra thông báo có kèm thời gian và mức độ quan trọng.
    """
    # Định dạng: [Thời gian] [Mức độ] Nội dung
    # Ví dụ: [2023-10-25 10:00:00] [INFO] System started.
    formatter = logging.Formatter(
        fmt='[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Tránh việc add handler nhiều lần gây log bị lặp
    if not logger.handlers:
        logger.addHandler(handler)

    return logger

def check_file_exists(file_path):
    """
    Kiểm tra xem file có tồn tại không.
    Trả về True nếu có, False nếu không.
    """
    if not os.path.exists(file_path):
        return False
    return True

def validate_paths(paths_dict):
    """
    Kiểm tra một danh sách các file.
    :param paths_dict: Dictionary chứa {tên_file: đường_dẫn}
    """
    logger = setup_logger()
    all_exist = True
    
    for name, path in paths_dict.items():
        if not check_file_exists(path):
            logger.error(f" Không tìm thấy file {name} tại: {path}")
            all_exist = False
        else:
            logger.info(f" Đã tìm thấy {name}")
            
    return all_exist
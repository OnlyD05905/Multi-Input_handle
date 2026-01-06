# Changelog

## [Phase 1] - Foundation & Architecture
- **Architecture:** Thiết lập cấu trúc dự án Modular (Config, Streamer, Utils).
- **Performance:** Xử lý Big Data bằng kỹ thuật Chunking (~80k logs/sec).
- **Docs:** Hoàn thiện tài liệu kiến trúc và kế hoạch 30 task.

## [Phase 2] - Multi-Input Streaming
- **sửa lại single input ở phase 1:** điều chỉnh streamer có thể nhận đầu vào 1 trong 4 ( đối với single-input) và all 
(đối với multi-input) bằng 1 biến cờ target
- **các file sửa:** ``main.py`` , ``streamer.py``.

## ## Phase 3: Preprocessing

import pandas as pd
import heapq
import config
from utils import setup_logger, check_file_exists

logger = setup_logger()

class LogStreamer:
    def __init__(self, target_source='all'):
        """
        :param target_source: 'all' (default), 'auth', 'proc', 'flows', or 'dns'
        """
        # Định nghĩa tất cả nguồn dữ liệu có thể( xem ở docs để hiểu rõ mô tả các trường)
        self.full_sources = {
            'auth': {
                'path': config.AUTH_FILE,
                'cols': ['Time', 'Source_User@Domain', 'Dest_User@Domain', 'Source_Computer', 'Dest_Computer', 'Auth_Type', 'Logon_Type', 'Auth_Orientation', 'Success']
            },
            'proc': {
                'path': config.PROC_FILE,
                'cols': ['Time', 'User@Domain', 'Computer', 'Process_Name', 'Start_End']
            },
            'flows': {
                'path': config.FLOWS_FILE,
                'cols': ['Time', 'Duration', 'Source_Computer', 'Source_Port', 'Dest_Computer', 'Dest_Port', 'Protocol', 'Packet_Count', 'Byte_Count']
            },
            'dns': {
                'path': config.DNS_FILE,
                'cols': ['Time', 'Source_Computer', 'Computer_Resolved']
            }
        }

        # Lọc nguồn dữ liệu dựa trên yêu cầu
        if target_source == 'all':
            self.sources = self.full_sources
        elif target_source in self.full_sources:
            self.sources = {target_source: self.full_sources[target_source]}
        else:
            logger.error(f"Invalid source type: {target_source}")
            self.sources = {}

        self.generators = []

    def _create_generator(self, source_name, source_config):
        path = source_config['path']
        cols = source_config['cols']
        
        if not check_file_exists(path):
            logger.warning(f"Skipping missing source: {source_name}")
            return

        logger.info(f"Initializing source: {source_name.upper()}")
        
        try:
            chunks = pd.read_csv(
                path, 
                header=None, 
                chunksize=config.CHUNK_SIZE
            )

            for chunk in chunks:
                chunk.columns = cols
                records = chunk.to_dict('records')
                for record in records:
                    record['Log_Source'] = source_name
                    yield record

        except Exception as e:
            logger.error(f"Error reading {source_name}: {e}")

    def stream(self):
        for name, conf in self.sources.items():
            gen = self._create_generator(name, conf)
            if gen:
                self.generators.append(gen)

        if not self.generators:
            return

        # Nếu chỉ có 1 nguồn, heapq.merge vẫn hoạt động tốt như generator thường
        merged_stream = heapq.merge(*self.generators, key=lambda x: x['Time'])
        
        for log in merged_stream:
            yield log
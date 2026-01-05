import pandas as pd
import config
from utils import setup_logger, check_file_exists

logger = setup_logger()

class LogStreamer:
    def __init__(self, file_path, chunk_size=None):
        self.file_path = file_path
        self.chunk_size = chunk_size if chunk_size else config.CHUNK_SIZE
        self.auth_columns = [
            'Time', 'Source_User@Domain', 'Dest_User@Domain', 
            'Source_Computer', 'Dest_Computer', 
            'Auth_Type', 'Logon_Type', 'Auth_Orientation', 'Success'
        ]

    def stream(self):
        if not check_file_exists(self.file_path):
            logger.error(f"File not found: {self.file_path}")
            return

        logger.info(f"Streaming data from: {self.file_path}")

        try:
            chunks = pd.read_csv(
                self.file_path, 
                header=None, 
                chunksize=self.chunk_size
            )

            for chunk in chunks:
                if 'auth' in self.file_path:
                    chunk.columns = self.auth_columns
                
                for _, row in chunk.iterrows():
                    yield row

        except Exception as e:
            logger.error(f"Error streaming file: {e}")
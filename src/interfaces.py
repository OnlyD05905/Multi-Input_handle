import abc

# --- 1. Base Class (Interface chuẩn) ---
class BaseDetector(abc.ABC):
    @abc.abstractmethod
    def detect(self, log):
        """
        Input: 1 dòng log (Dictionary)
        Output: List các alert (Dictionary)
        """
        pass
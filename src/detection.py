import abc

class BaseDetector(abc.ABC):
    @abc.abstractmethod
    def detect(self, log):
        pass

class SignatureBasedDetector(BaseDetector):
    def __init__(self):
        self.rules = {
            'suspicious_auth': {'ANONYMOUS LOGON'},
            'suspicious_processes': {'mimikatz', 'powershell', 'cmd', 'psexec', 'net', 'nmap'}
        }

    def detect(self, log):
        alerts = []
        source = log.get('Log_Source')

        if source == 'auth':
            src_user = log.get('Source_User', '')
            if src_user in self.rules['suspicious_auth']:
                alerts.append({
                    'title': 'Suspicious Auth Pattern',
                    'severity': 'HIGH',
                    'description': f"Blacklisted login detected: {src_user}",
                    'log_data': log
                })

        elif source == 'proc':
            proc_name = log.get('Process_Name', '').lower()
            for bad_proc in self.rules['suspicious_processes']:
                if bad_proc in proc_name:
                    alerts.append({
                        'title': 'Malicious Process Detected',
                        'severity': 'MEDIUM',
                        'description': f"Execution of restricted tool: {proc_name}",
                        'log_data': log
                    })
        
        return alerts

class DetectionEngine:
    def __init__(self):
        self.detectors = [
            SignatureBasedDetector()
        ]

    def analyze(self, log):
        all_alerts = []
        for detector in self.detectors:
            try:
                alerts = detector.detect(log)
                if alerts:
                    all_alerts.extend(alerts)
            except Exception as e:
                print(f"Error in detector {type(detector).__name__}: {e}")
                
        return all_alerts
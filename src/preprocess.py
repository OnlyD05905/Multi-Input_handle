class LogPreprocessor:
    def __init__(self):
        self.protocol_map = {6: 'TCP', 17: 'UDP'}

    def process(self, log):
        source = log.get('Log_Source')
        
        if source == 'auth':
            return self._process_auth(log)
        elif source == 'proc':
            return self._process_proc(log)
        elif source == 'flows':
            return self._process_flows(log)
        elif source == 'dns':
            return self._process_dns(log)
        return log

    def _process_auth(self, log):
        # Xu ly Source User
        src_user_full = str(log.get('Source_User@Domain', ''))
        log['Source_User'], log['Source_Domain'] = self._split_user_domain(src_user_full)
        log['Is_Machine_Src'] = log['Source_User'].endswith('$')

        # Xu ly Dest User
        dst_user_full = str(log.get('Dest_User@Domain', ''))
        log['Dest_User'], log['Dest_Domain'] = self._split_user_domain(dst_user_full)
        log['Is_Machine_Dst'] = log['Dest_User'].endswith('$')

        return log

    def _process_proc(self, log):
        # Xu ly User
        user_full = str(log.get('User@Domain', ''))
        log['User'], log['Domain'] = self._split_user_domain(user_full)
        
        # Chuan hoa ten process (ve chu thuong)
        proc_name = str(log.get('Process_Name', ''))
        log['Process_Name'] = proc_name.lower()
        
        return log

    def _process_flows(self, log):
        # Chuyen doi Protocol ID sang ten (6 -> TCP)
        proto = log.get('Protocol')
        if proto in self.protocol_map:
            log['Protocol_Name'] = self.protocol_map[proto]
        else:
            log['Protocol_Name'] = str(proto)
            
        return log

    def _process_dns(self, log):
        # Chuan hoa ten mien
        resolved = str(log.get('Computer_Resolved', ''))
        log['Computer_Resolved'] = resolved.lower()
        return log

    def _split_user_domain(self, full_str):
        if '@' in full_str:
            parts = full_str.split('@')
            return parts[0], parts[1]
        return full_str, ''
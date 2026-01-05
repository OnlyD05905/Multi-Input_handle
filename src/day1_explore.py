import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')

REDTEAM_FILE = os.path.join(DATA_DIR, 'redteam.txt.gz')
AUTH_FILE = os.path.join(DATA_DIR, 'auth.txt.gz')




def explore_redteam():
    if not os.path.exists(REDTEAM_FILE):
        print("not found {REDTEAM_FILE}")
        return
    
    df_red = pd.read_csv(REDTEAM_FILE, header = None)
    df_red.columns = ['Time', 'User', 'Source_Computer', 'Dest_Computer']  
    print(f" Tổng số cuộc tấn công: {len(df_red)}")
    print(df_red.tail())
    
    
def explore_auth_preview():
    if not os.path.exists(AUTH_FILE):
        print(f" Không tìm thấy file {AUTH_FILE} ")
        return
    df_auth = pd.read_csv(AUTH_FILE, header=None, nrows=10)    
    # Đặt tên cột theo tài liệu LANL
    df_auth.columns = [
        'Time', 'Source_User@Domain', 'Dest_User@Domain', 
        'Source_Computer', 'Dest_Computer', 
        'Auth_Type', 'Logon_Type', 'Auth_Orientation', 'Success'
    ]
    print(df_auth)
if __name__ == '__main__':
    #explore_redteam()
    explore_auth_preview()
from pathlib import Path
import shutil
import subprocess
import os
import ctypes, sys
from shutil import copy
import time



def start(prt):
    # define directories
    autostartdir = str(Path.home()) + '\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\\'
    clientdir = str(Path.home())

    # check if the user has granted the script admin privileges
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    if is_admin(): # run this if the user granted admin perms
        PATH = './clientv2.py'
        if os.path.isfile(PATH) and os.access(PATH, os.R_OK): # if the clientv2.py is in the same folder as the
            shutil.copy('start.cmd', autostartdir)
            subprocess.Popen('pythonw.exe ' + clientdir + '\clientv2.py client ' + prt)
        else:
            subprocess.Popen('pythonw.exe ' + clientdir + '\clientv2.py client ' + prt)
        
        
    else: # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    # 

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])


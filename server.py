import socket
import time

HOST = '10.20.18.185' # '192.168.43.82'
PORT = 2222 # 2222
server = socket.socket()
server.bind((HOST, PORT))
print('[+] Server Started')
print('[+] Listening For Client Connection ...')
server.listen(1)
client, client_addr = server.accept()
print(f'[+] {client_addr} Client connected to the server')
output = "null"

def loop():
    while True:
        global output
        command = input('Enter Command : ')
        command = command.encode()
        client.send(command)
        print('[+] Command sent')
        safeloop()
        output = client.recv(1024)
        output = output.decode()
        print(f"Output: {output}")
 
def safeloop():
    time.sleep(20)
    global output
    if output == "null":
        loop() 
       
loop()


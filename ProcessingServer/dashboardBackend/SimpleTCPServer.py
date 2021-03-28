
#!/usr/bin/env python3


import socket
import datetime
HOST = "Josephs-MacBook-Pro-2.local"  # Standard loopback interface address (localhost)
PORT = 8080        # Port to listen on (non-privileged ports are > 1023)

print("Hello TCP socket")

def openTCPSocketWithESP():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(HOST)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while conn : 
                data = conn.recv(1024)
                
                print("data_received %s @%s",data,datetime.datetime.now().time())
                if not data:
                    break
                conn.sendall(data)






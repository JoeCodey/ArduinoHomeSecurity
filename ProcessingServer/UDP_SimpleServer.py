import socket

UDP_IP = "192.168.2.54"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

print("UDP Socket starting")


while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print('Data from ', addr)
    print("received message:", data)
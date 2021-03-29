import socket

UDP_IP = "192.168.2.12"
UDP_PORT = 50000


class realTimeEventDetector :
    
    def __init__(self, Host_IP="192.168.2.12", port="50000"):
        self.Host_IP = Host_IP 
        self.port = port
        self.sock = None
    
    def start_and_bind(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, UDP_PORT))

    def closeConnection(self):
        self.sock.close() 

    def begin(self):       
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            print('Data from ', addr)
            print("received message:", data)
   





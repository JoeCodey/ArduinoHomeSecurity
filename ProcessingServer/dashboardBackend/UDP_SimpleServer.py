import socket
import datetime
import json
from queue import Queue 
UDP_IP = "192.168.2.12"
UDP_PORT = 50000

def genTimeStamp():
    time = datetime.datetime.now().time().strftime('%H:%M:%S.%f') 
    return time[:-3] 

def test1():
    sock = realTimeEventDetector() 
    sock.start_and_bind() 
    sock.begin() 

class realTimeEventDetector :
    
    def __init__(self, database ='', Host_IP="192.168.2.12", port="50000", espSensorType='text'):
        self.Host_IP = Host_IP 
        self.port = port
        self.sock = None
        self.eventlist = []
        self.espSensorType = espSensorType 
        
        
    
    def start_and_bind(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, UDP_PORT))

    def closeConnection(self):
        self.sock.close() 

    def begin(self):       
        index = 0 
        json_data = {}
        json_data['id'] = index 
        packetPair = (0,'','') # (packet_id, packet 1, packet 2)
        while not realTimeEventDetector.is_socket_closed(self.sock):
            
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            print('Data from ', addr)
            print("received message:", data)
            data = data.decode('utf-8')
            
            # packetPair[0] = data[data.find(':')+1]
            if(data.find('Detect')):
                json_data['id'] = index 
                json_data['dataType'] = self.espSensorType 
                json_data['location'] = 'entrance' 
                json_data['timeStart'] = genTimeStamp() 
                # packetPair[0] = data
                
            if(data.find("Ended")):
                json_data['timeEnd'] = genTimeStamp() 

            
            self.eventlist.append(json_data)
            with open("newData.json","w") as write_file:    
                json.dump(self.eventlist,write_file)
            json_data = {}
             
            print("socketClosed %s" % (realTimeEventDetector.is_socket_closed(self.sock))) 
            index += 1 
            
            #----
            #flip switch every other packet to check for packet pairs (e.g. start and end of sensor event)
            #everyOtherPacket = not everyOtherPacket 
            #----
    
    @staticmethod
    def is_socket_closed(sock: socket.socket) -> bool:
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception as e:
            logger.exception("unexpected exception when checking if a socket is closed")
            return False
        return False

   

exit



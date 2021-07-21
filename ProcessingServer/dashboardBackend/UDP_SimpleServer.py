import socket,platform
import datetime
import json
import threading, time
from queue import Queue 
from colorama import Fore, Back, Style
from  ArduCam_Backend import isCameraAvail,runArduCam
from tools_and_tests import genTimeStamp, getUniqueId, ping_address
from database.cassandra_connection import MyCassandraDatabase 


if platform.system() == 'Darwin':
    UDP_IP = "192.168.2.12"
elif platform.system() == 'Linux':
    UDP_IP = socket.gethostbyname(socket.gethostname())

UDP_PORT = 50000

class realTimeEventSocket :
    
    def __init__(self, database =None, host_IP=UDP_IP, port=50000, espSensorType='text'):
        self.host_IP = host_IP 
        self.port = port
        self.database = database 
        self.sock = None
        self.eventlist = []
        self.espSensorType = espSensorType 
        
    def start_and_bind(self):       
        # TODO FIX: If IP address is unavailble, code execution is blocked 
        try:
            print(Fore.YELLOW +"Attempting to bind (%s,%s)" %(self.host_IP,self.port))
            self.sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
            self.sock.bind((self.host_IP, self.port))
            print(Fore.GREEN + "Sock open @ -> " + str(self.sock.getsockname()), Style.RESET_ALL)
            
        except Exception as e: 
            print(Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX + "Start_and_bind says -> Exceptions: %s" % (str(e)), Style.RESET_ALL)
            

    def closeConnection(self):
        self.sock.close() 
    def write_db(self,data):
        # Dump dictionary object into string 
        json_string = json.dumps(data)
        self.database.insertJSON(json_string) if self.database != None \
        else print('db not initialized')
            
    def begin(self):       
        index = 0 
        json_data = {}        
        packetPair = (0,'','') # (packet_id, packet 1, packet 2)
        while not realTimeEventSocket().is_socket_closed(self.sock):     
            
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
           
            data = data.decode('utf-8')
            print("Data -> %s" % (data))
            #packetID from esp, same id -> related packets, (eg Start,end)
            #TODO: packets from ESP are not sending ':' before packet_id
            #packetId = data[data.find(':')+1]
            # if('packetId' in json_data 
            #    and json_data['packetId'] == packetId):
            #     json_data['timeEnd'] = genTimeStamp()
            if(data.find('Detect') >= 0 ):   
                event_id = int(getUniqueId()) 
                json_data['event_id'] = event_id
                #json_data['packet_id'] = packetId
                json_data['dataType'] = self.espSensorType 
                json_data['location'] = 'entrance' 
                json_data['timeStart'] = genTimeStamp()
                #check if camera data is available        
                # TODO: # isCameraAvail cannot check it r.status_code == 200 if camera is off. 
                # Simply waits for request to timeout while blocking code '''
                if(isCameraAvail()):
                    thread = threading.Thread(target=runArduCam, args= (event_id,123))
                    thread.start()
                    json_data["imagePath"] = "./imageCache/" + str(event_id) + ".jpg"
                    json_data["cameraData"] = 'yes'
                          
            if(data.find("Ended") >= 0 ):
                json_data['timeEnd'] = genTimeStamp()         
                if ('timeStart' in json_data):
                    # write data to cassandra 
                    self.database.insertJSON(json_data) 
                    #write to array to store in JSON file 
                    self.eventlist.append(json_data)
                json_data = {}
                index += 1 

                with open("./JSON/newData.json","w") as write_file:    
                 json.dump(self.eventlist,write_file)
    
    @staticmethod
    def is_socket_closed(sock: socket.socket) -> bool:
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            print("len(data) -> %s" % (len(data)))
            if len(data) == 0:
                return True
        except BlockingIOError:
            return False  # socket is open and reading from it would block
        except ConnectionResetError:
            return True  # socket was closed for some other reason
        except Exception as e:
            print("unexpected exception when checking if a socket is closed")
            return False
        return False

def start_socket():
    print(Fore.YELLOW+"... Executing start_socket() procedure ... ")
    cassandra_db = MyCassandraDatabase.getInstance()
    print(Fore.GREEN + "Cass Db instance -> %s " % (type(cassandra_db)))
    sock = realTimeEventSocket(database=cassandra_db) 
    sock.start_and_bind() 
    sock.begin() 

if __name__ == '__main__':
    start_socket()

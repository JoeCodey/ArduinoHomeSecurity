import socket
import datetime
import json
import threading, time
from queue import Queue 
from  ArduCam_Backend import isCameraAvail,runArduCam
from ToolsAndTests import genTimeStamp, getUniqueId
UDP_IP = "192.168.2.12"
UDP_PORT = 50000

class realTimeEventSocket :
    
    def __init__(self, database ='', Host_IP="192.168.2.12", port="50000", espSensorType='text'):
        self.Host_IP = Host_IP 
        self.port = port
        self.database = database 
        self.sock = None
        self.eventlist = []
        self.espSensorType = espSensorType 
        
    def start_and_bind(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.sock.bind((UDP_IP, UDP_PORT))

    def closeConnection(self):
        self.sock.close() 
    def write_db(self,data):
        # Dump dictionary object into string 
        json_string = json.dumps(data)
        self.database.insertJSON(json_string)

    def begin(self):       
        index = 0 
        json_data = {}        
        packetPair = (0,'','') # (packet_id, packet 1, packet 2)
        while not realTimeEventSocket().is_socket_closed(self.sock):     
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            data = data.decode('utf-8')
            print("Data -> %s" % (data))
            #packetID from esp, same id -> related packets, (eg Start,end)
            packetId = data[data.find(':')+1]
            # if('packetId' in json_data 
            #    and json_data['packetId'] == packetId):
            #     json_data['timeEnd'] = genTimeStamp()
            if(data.find('Detect') >= 0 ):   
                event_id = int(getUniqueId()) 
                json_data['event_id'] = event_id
                json_data['packet_id'] = packetId
                json_data['dataType'] = self.espSensorType 
                json_data['location'] = 'entrance' 
                json_data['timeStart'] = genTimeStamp()
                #check if camera data is available        
                # TODO: # isCameraAvail cannot check it r.status_code == 200 if camera is off. 
                # Simply waits for request to timeout while blocking code '''
                # if(isCameraAvail()):
                #     thread = threading.Thread(target=runArduCam, args= (event_id,123))
                #     thread.start()
                #     json_data["imagePath"] = "./imageCache" + str(event_id)
                #     json_data["cameraData"] = 'yes'
                          
            if(data.find("Ended") >= 0 ):
                json_data['timeEnd'] = genTimeStamp()         
                if ('timeStart' in json_data):
                    # write data to cassandra 
                    #self.write_db(json_data) 
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

   
def test_startSocket():
    sock = realTimeEventSocket() 
    sock.start_and_bind() 
    sock.begin() 



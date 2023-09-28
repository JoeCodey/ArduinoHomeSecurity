
import socket,platform, os, subprocess, re
print("Python Path %s"%(os.environ.get('PYTHONPATH')))
import json , requests
import time
from threading import Thread
from queue import Queue 
from colorama import Fore, Back, Style
from server.ArduCam_Backend import isCameraAvail,runArduCam
from utilities.tools_and_tests import genTimeStamp, getUniqueId, ping_address
from database.cassandra_connection import MyCassandraDatabase 
from utilities.logger import get_logger_obj

log = get_logger_obj() 
UDP_PORT = 50000
if platform.system() == 'Darwin':
    UDP_IP = str(os.system("ipconfig getifaddr en0"))
    

elif platform.system() == 'Linux':
    UDP_IP = socket.gethostbyname(socket.gethostname())
    UDP_PORT = 5000

def get_udp_ip_and_port():
    if platform.system() == 'Darwin':
        host_external = socket.gethostbyname_ex(socket.gethostname())
        #Ouput is a tuple with fromat -> ('host_machien.local', [], ['127.0.0.1', '192.168....'])
        UDP_IP = host_external[2][1] 
        print("UDP_IP->%s"%(UDP_IP))
        START_PORT = 50000
    elif platform.system() == 'Linux':
        UDP_IP = socket.gethostbyname(socket.gethostname())
        START_PORT = 5000
    else:
        UDP_IP = "127.0.0.1"  # Default IP for other platforms
        START_PORT = 5000     # Default port for other platforms
    log.logic("UDP_IP->%s START_PORT->%s"%(UDP_IP,START_PORT))
    return UDP_IP, START_PORT


class realTimeEventSocket :
    
    def __init__(self, database =None, host_IP=UDP_IP, port=UDP_PORT, espSensorType='text',name=None):
        self.host_IP = host_IP 
        self.port = port
        self.database = database 
        self.sock = None
        self.name = None
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
        
        while not realTimeEventSocket().is_socket_closed(self.sock):     
            
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
           
            data = data.decode('utf-8')
            print("Data -> %s" % (data))
            if(data.find('Detect') >= 0 ):   
                event_id = int(getUniqueId()) 
                json_data['event_id'] = event_id
                json_data['dataType'] = self.espSensorType 
                json_data['location'] = 'entrance' 
                json_data['timeStart'] = genTimeStamp()
                json_data['cameraData'] = 'no'
                #check if camera data is available      
                camera_flag = isCameraAvail() 
                log.debug("is camera available? %s"%(camera_flag))
                if(camera_flag):
                    thread = Thread(target=runArduCam, args= (event_id,123))
                    thread.start()
                    json_data["imagePath"] = "./imageCache/" + str(event_id) + ".jpg"
                    json_data["cameraData"] = 'yes'
                       
            if(data.find("Ended") >= 0 ):
                json_data['timeEnd'] = genTimeStamp()    
                # TODO: add a timeout when waiting for thread containing image
                if (json_data['cameraData'] == 'yes'):
                    thread.join()      
                if ('timeStart' in json_data):
                    # write data to cassandra 
                    log.debug("Attempting to write new data to DB, Camera?= %s"%(json_data['cameraData']))
                    if self.database != None:
                        self.database.insertJSON(json_data) 
                    #write to array to store in JSON file 
                    self.eventlist.append(json_data)
                json_data = {}
                index += 1 
                log.info("Path is currently %s"%(os.getcwd()))
                with open("./JSON/newData.json","w") as write_file:    
                 json.dump(self.eventlist,write_file)
    
    @staticmethod
    def is_socket_closed(sock: socket.socket) -> bool:
        try:
            # this will try to read bytes without blocking and also without removing them from buffer (peek only)
            data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
            #print("len(data) -> %s" % (len(data)))
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

def start_socket(_host_IP=UDP_IP):

    print(Fore.YELLOW+"... Executing start_socket() procedure ... ")
    log.debug("Attempted to start socket")
    # Get reference to Cassandra Db
    cassandra_db = MyCassandraDatabase.getInstance() 
    print(Fore.GREEN + "Cass Db instance -> %s " % (type(cassandra_db)), Style.RESET_ALL)
    sock = realTimeEventSocket(database=cassandra_db,host_IP=_host_IP) 
    sock.start_and_bind() 
    sock.begin() 


class RealTimeEventSocketManager:

    def __init__(self,database=None):
        self.sockets = []
        self.host_IP, self.current_port = get_udp_ip_and_port()
        self.ip_addresses = []
        self.db = database

    def create_socket(self, host_IP,name,espSensorType='text'):
        new_socket = realTimeEventSocket(name=name,host_IP=self.host_IP, database=self.db,port=self.current_port, espSensorType=espSensorType)
        self.sockets.append(new_socket)
        self.current_port += 1  # Increment the port number for the next socket
        return new_socket

    def start_all_sockets(self):
        for sock in self.sockets:
            sock.start_and_bind()
            thread = Thread(target=sock.begin,name=sock.name)
            thread.start()

    def get_network_devices(self):
        try:
            if platform == 'Darwin': 
                output = subprocess.check_output(["arp", "-a"], universal_newlines=True)
                pattern = re.compile(r"\d+\.\d+\.\d+\.\d+")
                self.ip_addresses = pattern.findall(output)
            else :
                self.ip_addresses = os.environ.get("HOST_DEVICES_ON_NETWORK").split(" ")
            device_identities = []
            log.info("\tPotential IP Address of devices on network->%s"%(self.ip_addresses))
            # Ignore the first IP address as it is the Gateway/router 's IP Address. 
            for ip in self.ip_addresses[1:]:
                try:
                    response = requests.get(f"http://{ip}/identity", timeout=1)
                    if response.status_code == 200:
                        log.logic("ESP device IP=%s Identity=%s"%(ip,response.text))
                        device_description = tuple(response.text.split(','))
                        device_identities.append(device_description)
                except requests.exceptions.RequestException:
                    pass
            return device_identities
        except subprocess.CalledProcessError as e:
            print(f"Error executing arp command: {e}")
            return []

def start_RealTimeEventSocketManager():
    log.info("Attempting to Start RealTimeEventSocketManager .... ")
    cassandra_db = MyCassandraDatabase.getInstance() 
    manager = RealTimeEventSocketManager(database=cassandra_db)
    device_identities = manager.get_network_devices()

    for device in device_identities:
        print(device)
        # You can create and start new sockets based on the identities found
        #TODO: Handle output type of devices .
        manager.create_socket(host_IP=device[0], espSensorType='text',name=str(device))

    # Starting all sockets
    manager.start_all_sockets()

if __name__ == '__main__':
    start_RealTimeEventSocketManager();

    



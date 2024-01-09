
import socket,platform, os, subprocess, re
print("Python Path %s"%(os.environ.get('PYTHONPATH')))
import json , requests
import time
from threading import Thread
from queue import Queue 
from colorama import Fore, Back, Style
# from server.ArduCam_Backend import isCameraAvail,runArduCam
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



class RealTimeEventSocketManager:

    def __init__(self,database=None):
        self.sockets = []
        self.host_IP, self.current_port = get_udp_ip_and_port()
        self.ip_addresses = os.environ.get("HOST_DEVICES_ON_NETWORK").split(" ")
        self.device_identities = [] # IP address of sensors on the network
        #TODO: how to we get the external IP  of the laptop/device running on the local network.
        #self.local_network_host_IP = 
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
        
                log.info("\tPotential IP Address of devices on network->%s"%(self.ip_addresses))
            # Ignore the first IP address as it is the Gateway/router 's IP Address. 
            for ip in self.ip_addresses[1:]:
                try:
                    response = requests.get(f"http://{ip}/identity", timeout=1)
                    if response.status_code == 200:
                        log.logic("ESP device IP=%s Identity=%s"%(ip,response.text))
                        device_description = tuple(response.text.split(','))
                        self.device_identities.append(device_description)
                        self.create_UDP_connection_with_device(ip) 
                except requests.exceptions.RequestException:
                    pass
            return self.device_identities
        except subprocess.CalledProcessError as e:
            print(f"Error executing arp command: {e}")
            return []
        
    def create_UDP_connection_with_device(self,device_IP) :
        ip_addresses = self.ip_addresses
        
        for ip in ip_addresses[1:]:
            try:
                responce = requests.post("http://%s/configureHost"%(device_IP),data=self.host_IP)
                prepared = responce.request
                pretty_print_POST(prepared)
            except requests.exceptions.RequestException:
                pass 
            

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    log.info('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def start_RealTimeEventSocketManager():
    log.info("Attempting to Start RealTimeEventSocketManager .... ")
    cassandra_db = MyCassandraDatabase.getInstance() 
    manager = RealTimeEventSocketManager(database=cassandra_db)
    device_identities = manager.get_network_devices()

    for device in device_identities:
        print(device)
        # You can create and start new sockets based on the identities found
        #TODO: Handle output type of devices .
        manager.create_socket(host_IP=manager.host_IP, espSensorType='text',name=str(device))

    # Starting all sockets
    manager.start_all_sockets()

if __name__ == '__main__':
    start_RealTimeEventSocketManager();
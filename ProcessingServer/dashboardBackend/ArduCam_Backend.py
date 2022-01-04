import requests , shutil
import threading, time 
import subprocess

base_ArduCam_IP = "192.168.2.203"
class ArduCamBackend:
    def __init__(self,ip = base_ArduCam_IP):
        self.base_ip = ip
  
    def get_image_event_synced(self,event_id):
        #first check the camera 
        image_name = "./imageCache/" +str(event_id) + '.jpg'
        uri_arducam = 'http://' + self.base_ip + '/capture'
        #always 
        if (isCameraAvail(self.base_ip)):
            r = requests.get(uri_arducam,stream = True )
            if r.status_code == 200:
                r.raw.decode_content = True 
                with open(image_name,'wb') as f:
                    shutil.copyfileobj(r.raw,f)
    def write_image_to_db(): 
        return 0 

def isCameraAvail(base_IP = base_ArduCam_IP):
        """Check if arduCam is online and responsive (status : 200)\ 
        \n**Ping Ip address w/out paths to test responsiveness """
        uri_arducam = "http://" + base_IP + '/capture'
        try: 
            res = subprocess.call(['ping','-q','-c','1',base_IP])
            if res == 0 :
                req = requests.get(uri_arducam)
            return True if res==0 and req.status_code==200 else False     
        except Exception as e: 
            print("isCameraAvail() says -> %s" %(str(e)))    

def runArduCam(_id,blank):
    cam = ArduCamBackend()    
    cam.get_image_event_synced(_id)

def test_isCameraAvail(): 
    returned_value = isCameraAvail(base_ArduCam_IP)
    print(returned_value)

def run_network_scan():
    addresses_of_interest = ["192.168.2.42",base_ArduCam_IP]
    for ping in addresses_of_interest:
        address = base_ArduCam_IP
        res = subprocess.call(['ping', '-c', '3', address])
        if res == 0:
            print( "ping to", address, "OK")
        elif res == 2:
            print("no response from", address)
        else:
            print("ping to", address, "failed!")


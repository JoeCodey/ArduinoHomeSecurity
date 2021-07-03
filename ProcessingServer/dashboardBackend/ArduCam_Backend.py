import requests , shutil
import threading, time 


base_ArduCam_IP = "http://192.168.2.203"

def isCameraAvail(base_IP = base_ArduCam_IP):
        'uri for arducam software, sends image over network for HTTP'
        uri_arducam = base_IP + '/capture' 
        r = requests.get(uri_arducam)
        return r.status_code == 200 

class ArduCamBackend:
    def __init__(self,uri = base_ArduCam_IP):
        self.base_uri = base_ArduCam_IP
  

    def get_image_event_synced(self,event_id):
        #first check the camera 
        image_name = "./imageCache/" +str(event_id) + '.jpg'
        uri = self.base_uri + '/capture'
        if (isCameraAvail(uri)):
            r = requests.get(uri,stream = True )
            if r.status_code == 200:
                r.raw.decode_content = True 
                with open(image_name,'wb') as f:
                    shutil.copyfileobj(r.raw,f)
    def write_image_to_db(): 
        return 0 
        
    
    
def runArduCam(_id,blank):
    cam = ArduCamBackend()    
    cam.get_image_event_synced(_id)





          


def test_isCameraAvail(): 
    returned_value = isCameraAvail(base_ArduCam_IP)
    print(returned_value)



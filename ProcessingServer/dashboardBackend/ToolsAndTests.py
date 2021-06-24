import unittest
import datetime
from unittest.case import TestCase
import uuid 
import os 

#import Cassandra Db backend 
from database.cassandra_connection import MyCassandraDatabase 

def getUniqueId():
    return str(uuid.uuid4().fields[-1])[:5] 
class TestCassDb(unittest.TestCase):

    __db = None 

    def test_coldstart(self):
        '''Tests if application can recover from a coldstart of the db'''
        TestCassDb.__db = MyCassandraDatabase.getInstance() 
        
        self.assertIsNotNone(TestCassDb.__db,"Failed MyCassDb instance was not assigned")
    
    def test_displayTable(self):
        TestCassDb.__db.displayTableContents() 



    def test_crud(self):
        '''Test CRUD functionality of Cassandra db''' 
        _uuid = getUniqueId()
        test_row = "INSERT INTO EventTable(event_id,packedId,dataType,timeStart,timeEnd) \
        VALUES("+_uuid+",0,'text','15:30:12:532','15:30:18:532');"
        test_json = '{"dataType": "text&video", \
        "event_id": %s, \
        "packet_id": 3, \
        "location": "entrance", \
        "timeEnd": "15:30:18:532", \
        "timeStart": "15:30:12:532" }' % (_uuid)
        TestCassDb.__db.insertJSON(test_json)
        res = TestCassDb.__db.getRowById(_uuid)
        print(res)
        self.assertEqual(1,1,"bleh")

if __name__ == '__main__':
    unittest.main() 


def gen_filename(extension='.jpg') : 
    """Generates filename with current time. \n
    Provide extension to change default '.jpg' \n
    (Rounds to 3 decimical places at miliseconds"""
    filename = extension
    time = datetime.datetime.now().time().strftime('%H:%M:%S.%f')
    filename = time[:-3] + filename
    return filename

def genTimeStamp():
    time = datetime.datetime.now().time().strftime('%H:%M:%S.%f') 
    return time[:-3] 



#--- Tests ----- 
def test1_capture(uri = "/capture"):
   url = base_ArduCam_IP + uri 
   filename = gen_filename() 
   r  = requests.get(url, stream = True ) 
   if r.status_code == 200 : 
      print("********\nresponse status code : %d\n********\n" % r.status_code )
      r.raw.decode_content = True 
      with open(filename,'wb') as f:
         shutil.copyfileobj(r.raw,f) 




        



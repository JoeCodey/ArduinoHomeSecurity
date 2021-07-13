
import unittest
import datetime
from unittest.case import TestCase
import uuid 
import os 
import json 

#import Cassandra Db backend 
from database.cassandra_connection import MyCassandraDatabase 

def getUniqueId():
    return int(str(uuid.uuid4().fields[-1])[:5] )
class TestCassDb(unittest.TestCase):

    __db = None 

    def test_coldstart(self):
        '''\nTests if application can recover from a coldstart of the db'''
        TestCassDb.__db = MyCassandraDatabase.getInstance() 
        
        self.assertIsNotNone(TestCassDb.__db," MyCassDb instance was not assigned")
        
    
    def test_connect_and_ping(self): 
        cass = MyCassandraDatabase.getInstance()
        #cass.displayTableContents()
        
        
    def test_crud(self):
        '''\nTest CRUD functionality of Cassandra db''' 
        _uuid = getUniqueId()
        test_json = {}
        test_json['event_id'] = _uuid 
        test_json['datatype'] = "text&video"
        test_json['location'] = 'entrance'
        test_json['packet_id'] = 3 
        test_json['timeend'] = "15:30:18:532"
        test_json['timestart'] = "15:30:12:532"
        TestCassDb.__db.insertJSON(json.dumps(test_json))
        res = TestCassDb.__db.getRowById_JSON(_uuid)
        res = json.loads(res)
        TestCassDb.__db.deleteRow(_uuid)
        self.assertDictEqual(test_json,res,"Test-json data does not match Db query result")

    def test_query_all_json(self):
        ''' test MyCassandraDatabase method to query results in JSON output\n'''
        result_set = TestCassDb.__db.query_all_json().all()
        result_arr = []
        #print("Raw results set : \n%s\n" %(result_set.all()))
        for row in result_set : 
            dict_item = json.loads(row.json)
            result_arr.append(dict_item) 
            #print("\nA row -> %s | %s \n" % (row.json,type(row)))
            #print("\t str(row) -> %s | %s \n " % (str(row.json),type(str(row.json))))
        #print(result_arr)
        return result_arr

if __name__ == '__main__':
    unittest.main(verbosity=2)

def run_db_unittest():
    return unittest.defaultTestLoader


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




        



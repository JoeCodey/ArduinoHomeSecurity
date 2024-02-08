import subprocess
import time
import unittest
import datetime
from unittest.case import TestCase
import uuid 
import os 
import json 
import socket
from utilities.logger import get_logger_obj
import requests

#---- Tools ----

def ping_address(addr):
    res = subprocess.call(['ping', '-q','-c', '3', addr])
    if res == 0:
        print( "ping to", addr, "OK")
    elif res == 2:
        print("no response from", addr)
    else:
        print("ping to", addr, "failed!")



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


def get_ip():
    """Function to reliably get host ip_address, (not 127.0.0.1)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

#import Cassandra Db backend$
#---- Cassandra Db tests ---- 
from database.cassandra_connection import MyCassandraDatabase 

def getUniqueId():
    return int(str(uuid.uuid4().fields[-1])[:5] )
log = get_logger_obj()

def isUrlCorrect(url):
        """Check if arduCam is online and responsive (status : 200)\ 
        \n**Ping Ip address w/out paths to test responsiveness """
        try: 
            res = subprocess.call(['ping','-q','-c','1',url])
            if res == 0 :
                req = requests.get(url)
            return True if res==0 and req.status_code==200 else False     
        except Exception as e: 
            print("isUrlCorrect says -> %s" %(str(e)))    
            log.error("isUrlCorrect says -> %s" %(str(e)))

class TestCassDb(unittest.TestCase):

    __db = None 

    def test_coldstart(self):
        '''\nTests if application can recover from a coldstart of the db'''
        TestCassDb.__db = MyCassandraDatabase.getInstance() 
        log.info("test_coldstart")
        self.assertIsNotNone(TestCassDb.__db," MyCassDb instance was not assigned")
        
    
    def test_connect_and_ping(self): 
        cass = MyCassandraDatabase.getInstance()
        #cass.displayTableContents()
        log.info("test_connect_and_ping")
        self.assertIsNotNone(cass)

        
        
    # def test_crud(self):
    #     '''\nTest CRUD functionality of Cassandra db''' 

    #     log.info("test_crud")
    #     unique_id = getUniqueId()
    #     data = '{"dataType": "text&video", \
    #     "event_id": %s, \
    #     "packet_id": 3, \
    #     "location": "entrance", \
    #     "timeEnd": "15:30:18:532", \
    #     "timeStart": "15:30:12:532" }' % (unique_id)
    #     TestCassDb.__db.insertJSON(data) 
    #     res = TestCassDb.__db.getRowById_JSON(unique_id)
    #     res = json.loads(res)
    #     TestCassDb.__db.deleteRow(unique_id)
    #     self.assertDictEqual(data,res,"Test-json data does not match Db query result")

    def test_query_all_json(self):
        ''' test MyCassandraDatabase method to query results in JSON output\n'''
        log.info("test_query_all_json")
        #--  CassandraDb returns results as a "set"  
        #result_set = TestCassDb.__db.query_all_json().all()
        result_arr = TestCassDb.__db.query_all_json()
        
        # ---- 'Set' to 'List' conversion implm in MyCassDb class 
        # for row in result_set : 
        #     dict_item = json.loads(row.json)
        #     result_arr.append(dict_item) 
            #print("\nA row -> %s | %s \n" % (row.json,type(row)))
            #print("\t str(row) -> %s | %s \n " % (str(row.json),type(str(row.json))))
        #print(result_arr)
        return result_arr
    # def test_delete_all(self):
    #     ''' test MyCassandraDatabase method to delete all rows in table '''
    #     log.info("test_delete_all")
    #     TestCassDb.__db.deleteAll()
    #     result_arr = TestCassDb.__db.query_all_json()
    #     self.assertEqual(len(result_arr),0,"test_delete_all failed, table not empty")
    def test_insert_with_websocket(self):
        ''' insert data into mycassandra database, websocket should update frontend'''
        log.info("test_insert_with_websocket" )
        unique_id = getUniqueId()
        data = '{"dataType": "text&video", \
        "event_id": %s, \
        "packet_id": 3, \
        "location": "entrance", \
        "timeEnd": "15:30:18:532", \
        "timeStart": "15:30:12:532" }' % (unique_id)
        TestCassDb.__db.insertJSON(data)
        # TestCassDb.__db.insertJSON(data)
        # TestCassDb.__db.insertJSON(data) 
    def test_run_external_socketio_event(self):
        '''\nTest if socketio event can be triggered from external process'''
        log.info("test_run_external_socketio_event")
        from server.websockettest import emmit_event_external_process
        from server.backendArduinoHomeSecurity import socketio
        emmit_event_external_process(socketio=socketio)
    #     #self.assertTrue(True,"test_run_external_socketio_event failed")
    def test_bhs_socketio_event(self):
        '''\nTest sdfgsdfgdsgif socketio event can be triggered from external process'''
        log.info("***test_bhs_socketio_event")
        from server.backendArduinoHomeSecurity import socketio
        from server.backendArduinoHomeSecurity import bhs_emmit_event_external_process
        bhs_emmit_event_external_process()
        #self.assertTrue(True,"test_run_external_socketio_event failed")
    # def test_trigger_websocket_update(self):
    #     log.info("test_trigger_websocket_update")
    #     isUrlCorrect("http://backend:8888/api/trigWebSockUpdate")
    #     response = requests.get("http://backend:8888/api/trigWebSockUpdate")
    #     self.assertEqual(response.status_code,200,"test_trigger_websocket_update failed")

    
        

def run_db_unittest(db_instance=None):
    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.loadTestsFromTestCase(TestCassDb)
    test_runner = unittest.TextTestRunner()
    return test_runner.run(test_suite)
    
if __name__ == '__main__':
    unittest.main(verbosity=2)






        


    
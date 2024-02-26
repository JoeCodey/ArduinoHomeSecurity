import subprocess
import unittest
import datetime
from unittest.case import TestCase
import uuid 
import os 
import json 
import socket

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

def run_db_unittest():
    return unittest.defaultTestLoader
    
if __name__ == '__main__':
    unittest.main(verbosity=2)






        



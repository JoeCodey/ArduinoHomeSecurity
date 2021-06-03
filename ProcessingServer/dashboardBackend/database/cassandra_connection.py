import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uuid #great tool for generating unique IDs 
from cassandra.cluster import Cluster 


def getUniqueId():
    return str(uuid.uuid4().fields[-1])[:5] 

class MyCassandraDatabase:
   '''
    Encapsulation of cassandra database implementation**Implements Singleton pattern, so only one database can be created** 
   '''
   __instance = None
   @staticmethod 
   def getInstance():
      """ Static access method. """
      if MyCassandraDatabase.__instance == None:
        try: 
            MyCassandraDatabase()
        except Exception as e:
            print("Err Occured ->  %s" % (e)) 

      return MyCassandraDatabase.__instance
   def __init__(self):
      """ Virtually private constructor. """
      if MyCassandraDatabase.__instance != None:
         raise Exception("This class is a singleton! We only have one database bro.")
      else:
         MyCassandraDatabase.__instance = self
         self.cluster = Cluster(['0.0.0.0'],port=9042)
         self.session = self.cluster.connect() 
         self.session.execute("USE ahs_event_database")
   def connectToCluster(): 
    cluster = Cluster(['0.0.0.0'],port=9042)
    session = cluster.connect()
    session.execute('USE ahs_event_database')

   def insertJSON(self,new_json_row):
       ''' Insert row given JSON ''' 
       querry = 'INSERT INTO eventtable JSON \'' + new_json_row + "';"
       print(querry)
       self.session.execute(querry)
    
   

   def deleteRow(self,_id):
        query = "Delete from eventtable where event_id = %s " % (_id)
        self.session.execute(query)

   def insertTestRow():
    return "INSERT INTO EventTable(event_id,packedId,dataType,timeStart,timeEnd) \
        VALUES("+getUniqueId()+",0,'text','15:30:12:532','15:30:18:532');"

   def createEventTable():
        return ("""CREATE TABLE EventTable(
    event_id int PRIMARY KEY,
    packet_id int,
    dataType text,
    location text,
    timeStart text,
    timeEnd text
    );""")
 
 
   def getRowById(self,_id):
       query = "select JSON* from eventtable where event_id=%d ;" % (_id)
       res = self.session.execute(query)
       return res


   def displayTableContents(self): 
        ''' Display all event table contents (FOR TESTING) ''' 
        rows = self.session.execute('SELECT * FROM eventtable')
        for row in rows:

            print(row.event_id,row.datatype,row.timeend)

def test_connect_and_ping(): 
    cass = MyCassandraDatabase() 
    cass.displayTableContents()
    return cass

def test_insertJSON() : 
    cass = MyCassandraDatabase()
    unique_id = getUniqueId()
    data = '{"dataType": "text&video", \
    "event_id": %s, \
    "packet_id": 3, \
    "location": "entrance", \
    "timeEnd": "15:30:18:532", \
    "timeStart": "15:30:12:532" }' % (unique_id)
    cass.insertJSON(data) 
    cass.displayTableContents()
    cass.deleteRow(unique_id) 

def test_getRowJSON() : 
    cass = MyCassandraDatabase.getInstance() 
    res = cass.getRowById(0)
    print(res.one())
    
    

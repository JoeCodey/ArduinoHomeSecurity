import datetime as dt
from email.quoprimime import unquote
import os,platform
import sys, time 
import json 
from datetime import date, timedelta
from colorama import Fore, Back, Style
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uuid #great tool for generating unique IDs 
from cassandra.cluster import Cluster

if platform.system() == 'Darwin':
    Cass_IP = '0.0.0.0'
elif platform.system() == 'Linux':
    Cass_IP = 'cas1'

 # Temp 
def getUniqueId():
    return str(uuid.uuid4().fields[-1])[:5] 

class MyCassandraDatabase:
   '''
    Encapsulation of cassandra database implementation **Implements Singleton pattern, so only one database can be created** 
   '''
   __instance = None
   __isStarting = False 
   __debug_counter =0
   
   @staticmethod 
   def getInstance():
      """ Static access method. """
      if MyCassandraDatabase.__instance == None:
        try: 
            MyCassandraDatabase()
        except Exception as e:
            # print("Err Occured ->  %s" % (e)) 
            error = str(e)
            print(Fore.RED+" DB ERROR ->\n -- %s -- \n\n" %(e))
      return MyCassandraDatabase.__instance
   
   def __init__(self):
      """ Virtually private constructor. """
      self.keyspace_id = 'ahs_event_db'
      if MyCassandraDatabase.__instance != None:
         raise Exception("This class is a singleton! We only have one database bro.")
      else:
         self.db_online = False
         MyCassandraDatabase.__instance = self
         
         try:
            self.connectToCluster()
         except Exception as e:
            print("***\n***\t"+Fore.GREEN+"DB Err Occured ->  %s\n***" % (e))
            error = str(e)
        # Check if cassandra docker needs to be coldstarted (Error 2200)
            if error.find('2200') and MyCassandraDatabase.__isStarting == False :
                MyCassandraDatabase.__isStarting = True 
                print("Attempting to run docker-compose.yaml file ...\n***Make take 60-90 seconds for Cassandra docker container to initialize")
                _cwd = os.getcwd() 
                cmd = '''echo "cd %s; docker-compose up; echo DONE! " > cassDoc.command; chmod +x cassDoc.command; open cassDoc.command;
                ''' %(_cwd)
                status = os.system(cmd)
                
                #Wait for Cassandra docker container to be online (90 sec)
                timeout_at = dt.datetime.now() + timedelta(seconds=90)
               
                while(True and self.db_online != True):
                    try:
                        self.connectToCluster() 
                        
                    except Exception as e:
                        pass 
                    if timeout_at < dt.datetime.now() :
                        raise Exception("TimeOutError: Cassandra_connection.py says -> Timeout, Could not connect to Cassandra Db")
                        break

   def connectToCluster(self): 

    self.cluster = Cluster([Cass_IP],port=9042)
    print(Fore.BLUE + str(self.__debug_counter)+"cassandra_connection ... Attempting to connect to Db")
    self.__debug_counter += 1
    self.session = self.cluster.connect()
    #If this line is executed, no error was thrown and Cass docker is online 
    self.db_online = True
    try:
        self.session.execute('USE ahs_event_db')
    except Exception as e: 
        error = str(e)
        index = error.find("Keyspace 'ahs_event_db' does not exist")
        #--Auto-initialize Keyspace if it hasn't been initialized--
        if index > 0: 
            self.session.execute("CREATE KEYSPACE ahs_event_db \
            WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};")
            self.session.execute(self.createEventTable(self))
            # --- delcare 'USE' of new keyspace ahs_event_db after it was made 
            self.session.execute('USE ahs_event_db')
    try: 
        db = self.query_all_json()
        # if db is empty, populate it with test_data
        # WARNING --- THIS SHOULD BE CHANGED IN PRODUCTION (actively detecting events) 
        if len(db) == 0:
            self.session.execute(self.createEventTable())
            populate_db_test_data()
    except Exception as e: 
        index = str(e).find('table eventtable does not exist') 
        if index > 0 :
            self.session.execute(self.createEventTable())
            
    
   def insertJSON(self,new_json_row):
       ''' Insert row given JSON ''' 
       if type(new_json_row) == dict:
           new_json_row = json.dumps(new_json_row)
       querry = 'INSERT INTO eventtable JSON \'' + new_json_row + "';"
       self.session.execute(querry)
    
   def deleteRow(self,_id):
        query = "Delete from eventtable where event_id = %s " % (_id)
        self.session.execute(query)
   def deleteAll(self):
       query = 'select JSON* from eventtable' 
       res_set = self.session.execute(query)
       for row in res_set:
           json_elem = json.loads(row.json)
           self.deleteRow(json_elem['event_id'])
        

   def insertTestRow(self):
    return "INSERT INTO EventTable(event_id,packet_Id,dataType,timeStart,timeEnd) \
        VALUES("+getUniqueId()+",0,'text','15:30:12:532','15:30:18:532');"

   
   def createEventTable(self):
        return ("""CREATE TABLE eventtable(
    event_id int PRIMARY KEY,
    packet_id int,
    dataType text,
    location text,
    timeStart text,
    timeEnd text,
    imagepath text,
    cameradata text
    );""")
   def query_all_json(self):
       ''' Returns all entries as Cassandra Result Set object'''
       query = 'select JSON* from eventtable'
       res_set = self.session.execute(query)
       res_json_arr = []
       for row in res_set:
           json_elem = json.loads(row.json)
           res_json_arr.append(json_elem)
       return res_json_arr
 
   def getRowById_JSON(self,_id):
       query = "select JSON* from eventtable where event_id=%s ;" % (_id)
       res = self.session.execute(query)
       return res.one().json


   def displayTableContents(self): 
        ''' Display all event table contents (FOR TESTING) ''' 
        rows = self.session.execute('SELECT * FROM eventtable Limit 100')
        for row in rows:
            print(row.event_id,row.datatype,row.timeend,row.imagepath,row.cameradata)

def test_connect_and_ping(): 
    cass = MyCassandraDatabase.getInstance()
    cass.displayTableContents()
    return cass

def test_insertJSON() : 
    cass = MyCassandraDatabase.getInstance()
    unique_id = getUniqueId()
    data = '{"dataType": "text&video", \
    "event_id": %s, \
    "packet_id": 3, \
    "location": "entrance", \
    "timeEnd": "15:30:18:532", \
    "timeStart": "15:30:12:532" }' % (unique_id)
    cass.insertJSON(data) 
    cass.displayTableContents()
    # cass.deleteRow(unique_id) 
def insertCustomEvent(imageId):
    imageId = str(imageId)
    eventId = imageId.split(".")[0]
    cass = MyCassandraDatabase.getInstance() 
    data = '{"dataType": "text", \
    "event_id": %s, \
    "packet_id": 3, \
    "location": "entrance", \
    "timeEnd": "12:30:18:532", \
    "timeStart": "12:30:12:532", \
    "imagePath": "./imageCache/%s", \
    "cameraData": "yes" }'% (eventId,imageId)
    cass.insertJSON(data)
    cass.displayTableContents()
def populate_db_test_data():
    cass = MyCassandraDatabase.getInstance() 
    test_events = os.listdir("../imageCache")
    for event in test_events : 
        # note InsertCustomEvent strips file extensions
        # -- e.g. feed function "testexample.jpg"
        insertCustomEvent(event)



    


    


def test_getRowJSON() : 
    cass = MyCassandraDatabase.getInstance() 
    res = cass.getRowById()
    print(res.one())
    
    

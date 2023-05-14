import datetime as dt
from email.quoprimime import unquote
import os,platform
import sys, time 
import json 
import logging  
from datetime import date, timedelta
from colorama import Fore, Back, Style
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uuid #great tool for generating unique IDs 
from cassandra.cluster import Cluster
from utilities.logger import get_logger_obj


if platform.system() == 'Darwin':
    Cass_IP = '0.0.0.0'

elif platform.system() == 'Linux':
    Cass_IP = 'cas1'

 # Temp 
def getUniqueId():
    return str(uuid.uuid4().fields[-1])[:5] 

# Define new level
LOGIC_LEVEL_NUM = 15
logging.addLevelName(LOGIC_LEVEL_NUM, "LOGIC")

# Add a new method to the logger
def logic(self, message, *args, **kws):
    if self.isEnabledFor(LOGIC_LEVEL_NUM):
        self._log(LOGIC_LEVEL_NUM, message, args, **kws) 

log = get_logger_obj() 

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
      log.info("Returning reference to existing Cassandra DB")
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
            print("***\n***\t"+"(Alpha) DB Err Occured ->  %s\n***" % (e))
            log.error("***\n***\t"+"(Alpha) DB Err Occured ->  %s\n***" % (e))
            
            error = str(e)
            #Wait for Cassandra docker container to be online (90 sec)
            timeout_at = dt.datetime.now() + timedelta(seconds=90)
            attempt_delay = 5 
            
            while(True and self.db_online != True):
                        # attempt connection after attempt_delay 
                        next_time = time.time() + attempt_delay 
                        try:
                            #print(Fore.RED + str(self.__debug_counter)+"(beta) cassandra_connection ... Attempting to connect to Db")
                            print("Sleep Time -> %s"%(str(max(0,next_time-time.time()))))
                            log.logic("Sleep Time -> %s"%(str(max(0,next_time-time.time()))))
                            sleep_time = max(0,next_time-time.time())
                            time.sleep(sleep_time)
                            self.connectToCluster() 
                            
                        except Exception as e:
                            pass 
                        if timeout_at < dt.datetime.now() :
                            raise Exception("TimeOutError: Cassandra_connection.py says -> Timeout, Could not connect to Cassandra Db")
                            break
                        next_time += (time.time() - next_time) // attempt_delay * attempt_delay + attempt_delay
        # Check if cassandra docker needs to be coldstarted (Error 2200)
        # ONLY USEFULL WHEN STARTING FROM MAC OS OUTSIDE A DOCKER ENVIRONMENT 
            if platform.system() == 'Darwin':
                if error.find('2200') and MyCassandraDatabase.__isStarting == False :
                    MyCassandraDatabase.__isStarting = True 
                    print("Attempting to run docker-compose.yaml file ...\n***Make take 60-90 seconds for Cassandra docker container to initialize")
                    _cwd = os.getcwd() 
                    os.lstat()
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
    #print(Fore.BLUE + str(self.__debug_counter)+"(Charlie) cassandra_connection ... Attempting to connect to Db")
    log.logic("cassandra_connection ... Attempting to connect to Db")
    self.__debug_counter += 1
    self.session = self.cluster.connect()
    #If this line is executed, no error was thrown and Cass docker is online 
    print(Fore.YELLOW + str(self.__debug_counter)+"(delta) Cassandra Db connection established")
    log.info(str(self.__debug_counter)+"(delta) Cassandra Db connection established")
    self.db_online = True   
    try:
        self.session.execute('USE ahs_event_db')
    except Exception as e: 
        error = str(e)
        print(Fore.LIGHTYELLOW_EX + str(self.__debug_counter)+"(echo) Setting Up Table")
        log.error(error)
        index = error.find("Keyspace 'ahs_event_db' does not exist")
        #--Auto-initialize Keyspace if it hasn't been initialized--
        if index > 0:
            self.session.execute("CREATE KEYSPACE ahs_event_db \
            WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};")
            # --- delcare 'USE' of new keyspace ahs_event_db after it was made 
            self.session.execute('USE ahs_event_db')
            # Create Eventtable after keyspeac is created 
            # --- TODO: If these commands fail, how can we ensure that the keyspaces and eventtable are created and attacehd to the instance
            self.session.execute(self.createEventTable())
    try: 
        db = self.query_all_json()
        # if db is empty, populate it with test_data
        # WARNING --- THIS SHOULD BE CHANGED IN PRODUCTION (actively detecting events) 
        if len(db) == 0:
            try:
                log.logic("populating with db test data")
                val = populate_db_test_data() 
                print('Val = %s'%(val))
            except Exception as e: 
                print("Error from data population funciton RetVal:%s,\nErr:%s"%(val,str(e)))
    except Exception as e: 
        index = str(e).find('table eventtable does not exist') 
        if index > 0 :
            print(Fore.RED+"DELTA ")
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
    #cass.displayTableContents()

def populate_db_test_data():
    cass = MyCassandraDatabase.getInstance() 
    try:
        test_events = os.listdir("./imageCache")
    except Exception as e: 
        log.error(str(e))
    for event in test_events : 
        # note InsertCustomEvent strips file extensions
        # -- e.g. feed function "testexample.jpg"
        #print("attempting to insert %s"%(event))
        insertCustomEvent(event)

    log.info("func populate_db_test_data EXECUTED")
    return 1



    


    


def test_getRowJSON() : 
    cass = MyCassandraDatabase.getInstance() 
    res = cass.getRowById()
    print(res.one())
    
    

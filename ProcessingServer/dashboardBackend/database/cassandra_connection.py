import datetime as dt
from email.quoprimime import unquote
import os,platform
import sys, time 
import json
import requests
from datetime import date, timedelta
from colorama import Fore, Back, Style
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import uuid #great tool for generating unique IDs 
from cassandra.cluster import Cluster
from utilities.logger import get_logger_obj


from flask import current_app
from flask_socketio import SocketIO , Namespace

if platform.system() == 'Darwin':
    Cass_IP = '0.0.0.0'

elif platform.system() == 'Linux':
    Cass_IP = 'cas1'

 # Temp 
def getUniqueId():
    return str(uuid.uuid4().fields[-1])[:5] 

#Get custom logger object from utilites module {Log.error()...}
log = get_logger_obj() 




class MyCassandraDatabase:
   '''
    Encapsulation of cassandra database implementation **Implements Singleton pattern, so only one database can be created** 
   '''  
   __instance = None
   __isStarting = False 
   __debug_counter =0
   
   @staticmethod 
   def getInstance(FlaskAppContext=None):   
      """ Static access method. """
      if MyCassandraDatabase.__instance == None:
        try: 
            MyCassandraDatabase(FlaskAppContext=None)
        except Exception as e:
            # print("Err Occured ->  %s" % (e)) 
            error = str(e)
            log.error(" DB ERROR ->\n -- %s -- \n\n" %(str(e)))
      log.info("Returning reference to existing Cassandra DB")
      return MyCassandraDatabase.__instance
   
   def __init__(self,FlaskAppContext=None):
      """ Virtually private constructor. """
      self.keyspace_id = 'ahs_event_db'
      #lines to get context from flask app, so we can call socketio.emit() from cassandra_connection.py
      from server.backendArduinoHomeSecurity import app 
      self.socketio_mycassdb = SocketIO(message_queue='redis://redis:6379')
      
      self.FlaskAppContext = app 
      
      if MyCassandraDatabase.__instance != None:
         raise Exception("This class is a singleton! We only have one database bro.")
      else:
         self.db_online = False
         MyCassandraDatabase.__instance = self
         try:
            self.connectToCluster()
         except Exception as e:
            log.error("***\n***\t"+"(Alpha) DB Err Occured ->  %s\n***" % (e))
            error = str(e)
            #Wait for Cassandra docker container to be online (90 sec)
            timeout_at = dt.datetime.now() + timedelta(seconds=90)
            #Attempt to connect to the Cassandra every {attempt_delay} seconds
            attempt_delay = 5 
            
            while(True and self.db_online != True):
                        # attempt connection after attempt_delay 
                        next_time = time.time() + attempt_delay 
                        try: 
                            #-- If the db is still spinning up wait 'attempt_delay' seconds and restart 
                            log.error("Coudn't connect ... wait for DB to start ... retry in -> %s seconds"%(str(max(0,next_time-time.time()))))
                            sleep_time = max(0,next_time-time.time())
                            time.sleep(sleep_time)
                            self.connectToCluster() 
                        except Exception as e:
                            pass 
                        if timeout_at < dt.datetime.now() :
                            raise Exception("TimeOutError: Cassandra_connection.py says -> Timeout, Could not connect to Cassandra Db")
                        
                        next_time += (time.time() - next_time) // attempt_delay * attempt_delay + attempt_delay
   
   def close(self):
     """Close the connection to the Cassandra cluster."""
     try:
        print("doing nothign")
     except Exception as e:
        log.error(f"Error occurred while closing Cassandra connection: {str(e)}")

   def connectToCluster(self): 

    self.cluster = Cluster([Cass_IP],port=9042)
    log.logic("cassandra_connection ... Attempting to connect to Db")
    self.__debug_counter += 1
    #If this line is executed, no error was thrown and Cass docker is online 
    self.session = self.cluster.connect()
    
    log.info(str(self.__debug_counter)+"(delta) Cassandra Db connection established")
    self.db_online = True 
    self.__isStarting = False   
    try:
        #Load Cassandra Keyspace. Catch error and create keyspace if doesn't exist 
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
                val = CassandraDbManualTools.populate_db_test_data() 
                print('Val = %s'%(val))
            except Exception as e: 
                print("Error from data population funciton RetVal:%s,\nErr:%s"%(val,str(e)))
    except Exception as e: 
        index = str(e).find('table eventtable does not exist') 
        if index > 0 :
            print(Fore.RED+"DELTA ")
            self.session.execute(self.createEventTable())

   def execute_query(self,query,web_sock_communication=True): 
       '''
       Universal method to execute Cassandra querry
       Flags that data has change to WebSocket can communciate '''
       #/** --- Depricated -> attempting to import Flask app context in order to trigger WebScoket responses
       #/** import function which updates the WebSocket connected to the front end
       #/** from main controller file of the app (backendArdu...)
       from server.backendArduinoHomeSecurity import update_websocket
       from server.backendArduinoHomeSecurity import socketio
       #local_socketio = socketio
       #local_socketio = SocketIO(self.FlaskAppContext, cors_allowed_origins="http://localhost:3000",logger=True, engineio_logger=True) 
       #local_socketio = SocketIO() 
       try : 
           res = self.session.execute(query)
           #if no error is thrown, querry sucessful
           #if querry includes 
           query = query.lower()    
           insert_truth = query.find("insert")>=0
           delete_truth = query.find("delete")>=0
           truncate_truth = query.find("truncate")>=0
           #log.debug("query -> %s ||| truth value -> %s,%s"%(query,str(insert_truth),str(delete_truth)))

           # /**- Check if query changes db contents (add,delete) 
           try:
            if insert_truth or delete_truth or truncate_truth and web_sock_communication==True: 
                #executed query changed db -> update WebSocket
                log.info("Db changing query %s receivedAttempting to update front via WebSocket")
                #** http request that can commnunicate using docker networking to trigger the Flask app to
                #** Update the dashboard content in real-time via WebSocket
                #** NOTE: This avoids having to import Flask app context to cassandra_connection.py
                #response = requests.get("http://backend:8888/api/trigWebSockUpdate")
                from server.backendArduinoHomeSecurity import socketio
                with self.FlaskAppContext.app_context():
                    log.debug("App Context from Cassandra_connection --> "+str(current_app.name))
                    #call_update_websocket_with_context()  
                    # connect to the redis queue as an external process
                    #    external_sio = socketio.RedisManager('redis://', write_only=True)
                    
                    #self.socketio_mycassdb.emit('new_data','from_mycassdb !!',namespace='/socket.io')
                    update_websocket()
                    #    with self.FlaskAppContext.app_context():
                    #        log.debug("App Context from Cassandra_connection --> "+str(current_app.name))
                    #        local_socketio.emit('new_data','get new data from server',namespace='/socket.io')
                    
        
                # return results from query 
                return res
                #from server.backendArduinoHomeSecurity import socketio
                #local_socketio.emit('new_data',"get new data",namespace='/socket.io')
           except Exception as e:
             log.error(str(e))
           # returns results from query despite failure of websocket update
           return res 
       except Exception as e: 
           log.error(str(e))
    
   def insertJSON(self,new_json_row,web_sock_communication=True):
       ''' Insert row given JSON ''' 
       if type(new_json_row) == dict:
           new_json_row = json.dumps(new_json_row)
       querry = 'INSERT INTO eventtable JSON \'' + new_json_row + "';"
       self.execute_query(querry,web_sock_communication)
    
   def deleteRow(self,_id):
        query = "Delete from eventtable where event_id = %s " % (_id)
        self.execute_query(query)
   def deleteAll(self):
       query = 'truncate eventtable' 
       res_set = self.execute_query(query)
        

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
       res_set = self.execute_query(query)
       res_json_arr = []
       for row in res_set:
           json_elem = json.loads(row.json)
           res_json_arr.append(json_elem)
       return res_json_arr
 
   def getRowById_JSON(self,_id):
       query = "select JSON* from eventtable where event_id=%s ;" % (_id)
       res = self.execute_query(query)
       return res.one().json


   def displayTableContents(self): 
        ''' Display all event table contents (FOR TESTING) ''' 
        rows = self.execute_query('SELECT * FROM eventtable Limit 100')
        for row in rows:
            print(row.event_id,row.datatype,row.timeend,row.imagepath,row.cameradata)

class CassandraDbManualTools:
    # Collection of functions to control db manually 

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
        #cass.displayTableContents()
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
        "imagePath": "../imageCache/%s", \
        "cameraData": "yes" }'% (eventId,imageId)
        cass.insertJSON(data)
        #cass.displayTableContents()

    def populate_db_test_data():
        cass = MyCassandraDatabase.getInstance() 
        try:
            test_events = os.listdir("./imageCache")
        except Exception as e: 
            log.error(str(e))
        for event in test_events[1:5] : 
            # note InsertCustomEvent strips file extensions
            # -- e.g. feed function "testexample.jpg"
            #print("attempting to insert %s"%(event))
            CassandraDbManualTools.insertCustomEvent(event)

        log.info("func populate_db_test_data EXECUTED")
        return 1

    def test_getRowJSON() : 
        cass = MyCassandraDatabase.getInstance() 
        res = cass.getRowById()
        print(res.one())

    def run_test_insertJSON():
        cass = MyCassandraDatabase.getInstance()
        cass.insertTestRow()
        cass.displayTableContents()
    
    def trigger_websocket_update():
        response = requests.get("http://backend:8888/api/trigWebSockUpdate")


def getCassandraDbInstance():
    return MyCassandraDatabase.getInstance()
def delete_all_custom_test():
        cass = MyCassandraDatabase.getInstance()
        cass.deleteAll()
def add_three_custom_test():
    for i in range(3):
        CassandraDbManualTools.test_insertJSON() 

# if __name__ == '__main__':
#     add_three_custom_test
    

    
    

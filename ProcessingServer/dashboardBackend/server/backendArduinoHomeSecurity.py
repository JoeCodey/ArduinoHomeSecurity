
from flask import Flask, current_app,redirect, url_for, request, send_file, jsonify, g
import flask_cors
from flask_socketio import SocketIO , Namespace
import requests , shutil 
import threading, time 
from io import BytesIO  
import os
import logging 
import json , datetime
from queue import Queue
import unittest 
#From project
from database.cassandra_connection import MyCassandraDatabase
from database.cassandra_connection import CassandraDbManualTools
from server.UDP_SimpleServer import start_socket
from server.ArduCam_Backend import base_ArduCam_IP
from utilities.tools_and_tests import gen_filename, run_db_unittest
from utilities.logger import get_logger_obj
import eventlet 

# new version of UDP server. Considering separating the server from Application.
from api.devices import start_RealTimeEventSocketManager
class WebSockCustomNamespace(Namespace):
   '''Class which implements socket.io functions to listen and emit events on the namespace '/socker.io used
   by the client.'''
   def on_connect(self):
        print('Client connected to namespace /socket.io')
   def on_disconnect(self):
        print('Client disconnected')
   def on_test_event(self, message):
      print("Received testEvent from react: "+str(message))
      log.logic("Test Event Message -> "+message)
      socketio.emit('test_response','** SERVER (on_testEvent) ---->'+message,namespace='/socket.io')
   def on_test_message(self,message):
      print("Received ' from react: "+str(message))
      log.logic("Test Event Message -> "+message)
      socketio.emit('test_response','** SERVER (on_test_message) ---->'+message,namespace='/socket.io')

def create_app():
    # 
    eventlet.monkey_patch()
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000",logger=True, engineio_logger=True)
    socketio.on_namespace(WebSockCustomNamespace('/socket.io'))
    with app.app_context():
       get_db(app,socketio)

    return app,socketio

def get_db(app=None,socketio=None):
      if 'db' not in g:
         g.db = MyCassandraDatabase.getInstance(FlaskAppContext=app,socket_io_cass = socketio)
      return g.db


log = get_logger_obj()
log.majorcheckpoint("Main? -> %s, Where are we? -> %s" %(__name__=='__main__',str(__name__)))

# Q?: can you write documentation for the next line 
# Flask app created with
app,socketio = create_app()
#Acknowledge initiation of Flask App and that it exists  
log.majorcheckpoint("BACKEND: Flask Defined , exec: app = %s" % Flask(__name__))
'''
Socket.io initialization 
'''
# socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000",logger=True, engineio_logger=True)
# socketio = SocketIO(app,cors_allowed_origins="http://localhost:3000",logger=True, engineio_logger=True) 
# socketio.on_namespace(WebSockCustomNamespace('/socket.io'))



global_variable = "im a global variable"


# with app.app_context():
#       #Start Cassandra Database and check connection 
#       db = MyCassandraDatabase.getInstance()

def getNewBlockData(id=None):
   db = get_db(app)
   if db == None:
      with open('./JSON/newData.json', 'r') as myfile:
         data=myfile.read()
   else:
      data = db.query_all_json()
      #log.debug("Data from cassandra -> "+str(data))
   if id == None:
      return jsonify(data)
   else:
      return 'specific data'   

def update_websocket(): 
   '''Updates frontend with data from db via WebSocket'''

   with app.app_context():
      log.debug("** func udpate_websocket: App Context --> "+str(current_app.name))
      try:
         #Get jsonified data from database
         data = getNewBlockData()
         log.majorcheckpoint("what var am I? -> "+global_variable)
         log.debug("** func udpate_websocket: Data from getNewBlockData() -> "+str(data))
         log.debug("** func update_websocket: Type of data from getNewBlockData() -> "+str(type(data)))
         log.debug("** func update_websocket: data.json -> "+str(data.json))
         log.info("** func update_websocket: flask_web_socket sending data to frontent") 
         socketio.emit('new_data_from_server',data.json,namespace='/socket.io')
      except Exception as e: 
         log.error(str(e))

#Initiates logger CUSTOM logger object which colours {errors,info,debug..etc}


ctx = app.test_request_context() 

# queue to save 10 most recent pictures 
q = Queue(maxsize=11)   

#Start Cassandra Database and check connection 

#log.majorcheckpoint("Cass Db instance -> %s " % (type(g.db))) 

#Start realTimeEventSocket to talk to ESP8266 devices
log.majorcheckpoint("... Starting ESP sockdet ...")
# (Complete) TODO: .begin() call blocks flask backend from starting ... create new thread?
thread_event_socket = threading.Thread(target=start_RealTimeEventSocketManager)
thread_event_socket.start()


if __name__ == '__main__':
   log.majorcheckpoint("... Attempting to run Flask app from main file (__name__=='__main__') ... ")
   socketio.run(app, port=8888)

# DEPRICATED: 
# method to emmit websocket events when querries are executed on the database
def execute_cassandra_querry(query):
   try:
      res = g.db.execute_query(query)
      if query.find("insert")>=0 or query.find("delete")>=0:
         update_websocket()
   except Exception as e:
      log.error(str(e))
# *** generates list of all files names in image directory
# DIR = './imageCache'
# cached_images = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]

#http route which triggers a test response to the client via Socket.io WebSocket
@app.route('/api/testWebSocket')
def hello():
    log.debug("@...flask/api/testWebSocket")
    #Give socket time to establish connection
    time.sleep(3)
    log.majorcheckpoint("...****-> do I have a global sid memer var? -> "+str(g.sid))
    bhs_emmit_event_external_process()
    log.debug("... emitting testResponse from route /api/testWebSocket")
    socketio.emit('test_response',"replying to testWebSocket() react function",namespace='/socket.io')
    #update_websocket()
    
    return 'Hello World'

#Http Route which triggers a WebSocket 
@app.route('/api/trigWebSockUpdate')
def trigger_websocket_update():
   try:
      update_websocket() 
   except Exception as e:
      log.error(str(e))
   return 'none'

def call_update_websocket_with_context():
   update_websocket(getNewBlockData(),socketio_local_context=socketio) 
   

#Gets new data of events from the database (defaults to file if database doesn't exist)
   

   
@app.route('/login',methods = ['POST', 'GET'])
#TODO: add login functionality 
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/api/blockdata',methods = ['GET'])
def getBlockData(id=None):
   """Get initial sample data \n 
   This is used to test front end  """
   print("/blockdata")
   with open('TestData/initialBlockData.json', 'r') as myfile:
    data=myfile.read()
    
   blockData = json.loads(data)
    
   if id == None:          
      return jsonify(blockData) 
   else: 
      return "specifc data"
   


@app.route('/api/newblockdata',methods = ['GET'])
def router_for_getNewBlockData(id=None):
   """ Get most up to data from file \n    
   UDP_SimpleServer populates file with ESP12-E events """
   response = getNewBlockData()
   log.debug("Data returned from getNewBlockData() -> "+str(response))
   return response 

@app.route('/api/getImage',methods = ['POST', 'GET'])
def getCameraimage():
   """Get image from file \n
   Indexed by id of corresponsing sensor event (e.g. motion)"""
   data = request.args.get("id")
   
   #working directory is /usr/src/app from docker configuration (see docker-compose.prod.yml)  
   cwd = os.getcwd()
   filename = cwd + "/imageCache/"+data + ".jpg"

   with open(filename,'r') as f:

    return send_file(filename, mimetype='image/jpeg')

#Get image from ArduCam camera if availabel 
@app.route('/capture',methods = ['POST', 'GET'])
def capture():
   """ Get a captured image from ESP12-E camera \n
   Saves image to filesystem (max 10 images) \n
   Sends jpg image to client """

   uri = '/capture'
   url = base_ArduCam_IP + uri 
   filename = "./imageCache/"+ gen_filename('.jpg') 
   r  = requests.get(url, stream = True ) 
   if r.status_code == 200 : 
      print("********\nresponse status code : %d\n********\n" % r.status_code )
      r.raw.decode_content = True 
      if q.full() : 
         file = q.get()
         os.remove(file) # remove oldest image from storage 
      if not q.full() :
         print(q.qsize())
         q.put(filename)
         with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw,f) 
         return send_file(filename, mimetype='image/jpeg')

#Route to be used for testing ArduCam data (not meant to work with dashboard frontend)
@app.route('/capture_test',methods = ['POST', 'GET'])
def capture_test():
   """FOR TESTING - FrontEnd\n
   Get static image and send to frontend"""

   filename = './imageCache/20:25:09.378.jpg'
   with open(filename,'r') as f:
    return send_file(filename, mimetype='image/jpeg')


#/** Depreciated -> route to start listening for motion events from sensor **/ 
# @app.route('/motion',methods = ['POST', 'GET'])
# def realtime_event_linsener():
#    """ Open a local socket over the network with a an 
#        ESP device to get events in real time"""
#    events = realTimeEventSocket(database='/TestData/initialBlockData.json')
#    events.start_and_bind() 
#    events.begin() 
#    startFlag = True 

@app.after_request
def after_request(response):
   """Tells Browswer to Allow CORS from flask requests"""
   response.headers.add('Access-Control-Allow-Origin', '*')
   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
   return response

@app.teardown_appcontext
def close_db(e=None):
   db = g.pop('db', None)
   if db is not None:
      db.close()  

def bhs_emmit_event_external_process():
    log = get_logger_obj()
    log.info("emmit_event_external_process")
    socketio.emit('test_response', 'Server generated event', namespace='/socket.io')



''' Run db unit tests '''
log.majorcheckpoint("\n\n... Running db unit tests ...\n")
# time.sleep(3)
#run_db_unittest() 

log.majorcheckpoint("running bhs emmit event external process manually")
with app.app_context():
   bhs_emmit_event_external_process()
   time.sleep(5)
   bhs_emmit_event_external_process()




   
 
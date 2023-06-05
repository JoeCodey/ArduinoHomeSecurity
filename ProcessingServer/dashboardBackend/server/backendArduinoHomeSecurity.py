
from flask import Flask, current_app,redirect, url_for, request, send_file, jsonify
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
from utilities.tools_and_tests import gen_filename, TestCassDb
from utilities.logger import get_logger_obj



app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000",logger=True, engineio_logger=True) 


class WebSockCustomNamespace(Namespace):
   '''Class which implements socket.io functions to listen and emit events on the namespace '/socker.io used
   by the client.'''
   def on_connect(self):
        print('Client connected to namespace /socket.io')
   def on_disconnect(self):
        print('Client disconnected')
   def on_testEvent(self, message):
      print("Received testEvent from react: "+str(message))
      log.logic("Test Event Message -> "+message)
      socketio.emit('testResponse','** SERVER (on_testEvent) ---->'+message,namespace='/socket.io')
   def on_test_message(self,message):
      print("Received ' from react: "+str(message))
      log.logic("Test Event Message -> "+message)
      socketio.emit('testResponse','** SERVER (on_test_message) ---->'+message,namespace='/socket.io')

socketio.on_namespace(WebSockCustomNamespace('/socket.io'))
#Acknowledge initiation of Flask App and that it exists 
print("BACKEND: Flask Defined , exec: app = Flask(__name__)") 

#Initiates logger CUSTOM logger object which colours {errors,info,debug..etc}
log = get_logger_obj()

log.info("Arew we in main? ->"+str(__name__ == '__main__'))
ctx = app.test_request_context() 

# queue to save 10 most recent pictures 
q = Queue(maxsize=11)   

#Start Cassandra Database and check connection 
db = MyCassandraDatabase.getInstance() 
print("Cass Db instance -> %s " % (type(db)))   

#Start realTimeEventSocket to talk to ESP8266 devices

print("... Starting ESP sockdet ...")
# (Complete) TODO: .begin() call blocks flask backend from starting ... create new thread?
thread_event_socket = threading.Thread(target=start_socket)
thread_event_socket.start()

# DEPRICATED: 
# *** method to emmit websocket events from cassandra_connection.py 
# def execute_cassandra_querry(querry):
#    try:
#       res = db.execute_query(querry)
#       update_websocket()
#    except Exception as e:
#       log.error(str(e))
# *** generates list of all files names in image directory
# DIR = './imageCache'
# cached_images = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]

#http route which triggers a test response to the client via Socket.io WebSocket
@app.route('/api/testWebSocket')
def hello():
    log.debug("@...flask/api/testWebSocket")
    #Give socket time to establish connection
    time.sleep(3)
    socketio.emit('newdata',"get new data",namespace='/socket.io')
    update_websocket()
    return 'Hello World'

#Http Route which triggers a WebSocket 
@app.route('/api/trigWebSockUpdate')
def trigger_websocket_update():
   try:
      socketio.emit('newdata',"Server says -> GET NEW DATA",namespace='/socket.io')
   except Exception as e:
      log.error(str(e))
   return 'none'
   
def update_websocket(): 
   '''Updates frontend with data from db via WebSocket'''
   with app.app_context():
      log.debug("App Context --> "+str(current_app.name))
      try:
         data = db.query_all_json()
         log.info("flask_web_socket sending data to frontent")
         socketio.emit('newData',jsonify(data))
      except Exception as e: 
         log.error(str(e))

   
@app.route('/login',methods = ['POST', 'GET'])
#TODO: add login functionality 
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))


@app.route('/api/blockdata',methods = [ 'GET'])
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
#Gets new data of events from the database (defaults to file if database doesn't exist)
@app.route('/api/newblockdata',methods = [ 'GET'])
def getNewBlockData(id=None):
   """Get most up to data from file \n    
   UDP_SimpleServer populates file with ESP12-E events """
   if db == None:
      with open('./JSON/newData.json', 'r') as myfile:
         data=myfile.read()
   else:
      data = db.query_all_json()
      
   if id == None:          
      return jsonify(data)
   else: 
      return "specifc data"

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


if __name__ == '__main__':
   log.info("... Attempting to run Flask app from main file (__name__=='__main__') ... ")
   # app.run(debug = False, port = 8888)
   socketio.run(app, port=8888)





   
 

from flask import Flask, redirect, url_for, request, send_file, jsonify
import flask_cors
import requests , shutil 
import threading, time 
from io import BytesIO
import os
import json , datetime
from queue import Queue
import unittest 
#From project
from database.cassandra_connection import MyCassandraDatabase 
from UDP_SimpleServer import realTimeEventSocket
from ArduCam_Backend import base_ArduCam_IP
from tools_and_tests import gen_filename
from tools_and_tests import TestCassDb

app = Flask(__name__)

ctx = app.test_request_context() 

# queue to save 10 most recent pictures 
q = Queue(maxsize=10)   

#generates list of all files names in image directory
# DIR = './imageCache'
# cached_images = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]

#Start Cassandra Database and check connection 

db = MyCassandraDatabase.getInstance() 
print("Cass Db instance -> %s " % (type(db)))

#Start realTimeEventSocket to talk to ESP8266 devices
esp8266_event_socket = realTimeEventSocket(database = db)
print("... Starting ESP socket ...")
esp8266_event_socket.start_and_bind()
# (Complete) TODO: .begin() call blocks flask backend from starting ... create new thread?
# *** start_and_bind() is blocking on Fail 
_cwd = os.getcwd() 
cmd_start_socket = '''echo "cd %s; source ./.AHS_backend/bin/activate; python UDP_SimpleServer.py ; " \
   > udp_serv.command; chmod +x udp_serv.command; open udp_serv.command''' %(_cwd)
os.system(cmd_start_socket)

# thread_event_socket = threading.Thread(target=esp8266_event_socket.begin())
# thread_event_socket.start()

@app.route('/login',methods = ['POST', 'GET'])
#TODO: add login functionality 
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')

      return redirect(url_for('success',name = user))

@app.route('/blockdata',methods = [ 'GET'])
def getBlockData(id=None):
   """Get initial sample data \n 
   This is used to test front end  """
   with open('initialBlockData.json', 'r') as myfile:
    data=myfile.read()
   blockData = json.loads(data)
    
   if id == None:          
      return jsonify(blockData)
   else: 
      return "specifc data"

@app.route('/newblockdata',methods = [ 'GET'])
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

@app.route('/getImage',methods = ['POST', 'GET'])
def getCameraimage():
   """Get image from file \n
   Indexed by id of corresponsing sensor event (e.g. motion)"""
   data = request.args.get("id")
   filename = "./imageCache/"+data + ".jpg"

   with open(filename,'r') as f:
    return send_file(filename, mimetype='image/jpeg')

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

@app.route('/capture_test',methods = ['POST', 'GET'])
def capture_test():
   """FOR TESTING - FrontEnd\n
   Get static image and send to frontend"""

   filename = './imageCache/20:25:09.378.jpg'
   with open(filename,'r') as f:
    return send_file(filename, mimetype='image/jpeg')

@app.route('/motion',methods = ['POST', 'GET'])
def realtime_event_linsener():
   """ Open a local socket over the network with a an 
       ESP device to get events in real time"""
   events = realTimeEventSocket(database='initialBlockData.json')
   events.start_and_bind() 
   events.begin() 
   startFlag = True 

@app.after_request
def after_request(response):
   """Tells Browswer to Allow CORS from flask requests"""
   response.headers.add('Access-Control-Allow-Origin', '*')
   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
   return response


if __name__ == '__main__':
   app.run(debug = True, port = 8888)





   
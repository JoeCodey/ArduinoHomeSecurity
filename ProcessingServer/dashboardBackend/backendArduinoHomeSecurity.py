from flask import Flask, redirect, url_for, request, send_file, jsonify
import flask_cors
import requests , shutil 
from io import BytesIO
import datetime
import wget
import os
import json 
from queue import Queue
from UDP_SimpleServer import realTimeEventDetector



app = Flask(__name__)

ctx = app.test_request_context() 

base_ESP_URL = "http://192.168.2.203"

# queue to save 10 most recent pictures 
q = Queue(maxsize=10)   



DIR = './imageCache'
cached_images = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]

def gen_filename() : 
    filename = '.jpg'
    time = datetime.datetime.now().time().strftime('%H:%M:%S.%f')
    filename = time[:-3] + filename
    return filename


@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])

def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/blockdata',methods = [ 'GET'])

def getBlockData(id=None):
   with open('initialBlockData.json', 'r') as myfile:
    data=myfile.read()
   blockData = json.loads(data)
    
   if id == None:          
      return jsonify(blockData)
   else: 
      return "specifc data"

@app.route('/newblockdata',methods = [ 'GET'])

def getNewBlockData(id=None):
   
   with open('newData.json', 'r') as myfile:
      data=myfile.read()
      
   blockData = json.loads(data)
    
   if id == None:          
      return jsonify(blockData)
   else: 
      return "specifc data"

@app.route('/getImage',methods = ['POST', 'GET'])
def getCameraimage():
   data = request.args.get("id")
   filename = "./imageCache/"+data + ".jpg"

   with open(filename,'r') as f:
    return send_file(filename, mimetype='image/jpeg')


@app.route('/capture',methods = ['POST', 'GET'])
def capture():
   """ Get a captured image from ESP12-E camera """

   uri = '/capture'
   url = base_ESP_URL + uri 
   filename = "./imageCache/"+ gen_filename() 
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
   """ Get a captured image from ESP12-E camera """

  
   filename = './imageCache/20:25:09.378.jpg'
   with open(filename,'r') as f:
    return send_file(filename, mimetype='image/jpeg')





@app.route('/motion',methods = ['POST', 'GET'])
def realtime_event_linsener():
   """ Open a local socket over the network with a an 
       ESP device to get events in real time"""
   events = realTimeEventDetector(database='initialBlockData.json')
   events.start_and_bind() 
   events.begin() 
   startFlag = True 

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
   app.run(debug = True, port = 8888)




def test1_capture(uri = "/capture"):
   url = base_ESP_URL + uri 
   filename = gen_filename() 
   r  = requests.get(url, stream = True ) 
   if r.status_code == 200 : 
      print("********\nresponse status code : %d\n********\n" % r.status_code )
      r.raw.decode_content = True 
      with open(filename,'wb') as f:
         shutil.copyfileobj(r.raw,f) 
   
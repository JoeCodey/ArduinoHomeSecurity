from flask import Flask, redirect, url_for, request, send_file, jsonify
import flask_cors
import requests , shutil 
from io import BytesIO
import datetime
import wget
import json 
from queue import Queue
# from UDP_SimpleServer import openUDPSocketWithESP



app = Flask(__name__)

ctx = app.test_request_context() 

base_ESP_URL = "http://192.168.2.203"

# queue to save 10 most recent pictures 
q = Queue(maxsize=10)   
with open('initialBlockData.json', 'r') as myfile:
    data=myfile.read()
blockData = json.loads(data)


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
   if id == None:          
      return jsonify(blockData)
   else: 
      return "specific data"





@app.route('/capture',methods = ['POST', 'GET'])
def capture():
   """ Get a captured image from ESP12-E camera """

   uri = '/capture'
   url = base_ESP_URL + uri 
   filename = gen_filename() 
   r  = requests.get(url, stream = True ) 
   if r.status_code == 200 : 
      print("********\nresponse status code : %d\n********\n" % r.status_code )
      r.raw.decode_content = True 
      if q.full() : q.get() # remove oldest image from storage 
      if not q.full(): 
         q.put(filename)
         with open(filename,'wb') as f:
            shutil.copyfileobj(r.raw,f) 
         return send_file(filename, mimetype='image/jpeg')

def realtime_event_linsener():
   """ Open a local socket over the network with a an 
       ESP device to get events in real time"""
   #openUDPSocketWithESP() 

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
   
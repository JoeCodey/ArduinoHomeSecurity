
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

#--- Tests ----- 
def test1_capture(uri = "/capture"):
   url = base_ArduCam_IP + uri 
   filename = gen_filename() 
   r  = requests.get(url, stream = True ) 
   if r.status_code == 200 : 
      print("********\nresponse status code : %d\n********\n" % r.status_code )
      r.raw.decode_content = True 
      with open(filename,'wb') as f:
         shutil.copyfileobj(r.raw,f) 
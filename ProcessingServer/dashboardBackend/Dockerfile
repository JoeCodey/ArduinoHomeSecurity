FROM python:3.9

RUN apt-get update -y 
# /** "python-dev" seems to be depreciates **/
# RUN apt-get install -y python3-pip python-dev build-essential 
RUN apt-get install -y python3-pip
RUN apt-get install curl -y
RUN apt-get install iputils-ping -y

RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app 

COPY requirements.txt /usr/src/app/

RUN pip install -r requirements.txt


CMD ["gunicorn","-b",":8888","backendArduinoHomeSecurity:app"]

#CMD ["run", "--host=0.0.0.0","--port=8888"]    

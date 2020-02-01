


> Written with [StackEdit](https://stackedit.io/).`
> 

# ArduinoHomeSecurity


## Description
Embedded home security camera system which can stream video of events at front door to a locally hosted web session. Images/Videos are intelligently analyzed and a description of the nature of the event is displayed to the user who can authorize appropriate actions such as openning door via a smart lock. 

# Architecture Diagrams 
- Activity https://go.gliffy.com/go/share/image/sr0pe8knaa19fgfq9qy1.png?utm_medium=live-embed&utm_source=custom 
- Sequence https://go.gliffy.com/go/share/image/slbc2iovuksl3v2gt6qo.png?utm_medium=live-embed&utm_source=custom


## Materials 

* Elegoo ATmega2560-16u (16 analog out pins) with ATmega16u2 (same chip as official Arduino version)
  * *future version will use a smaller board such as an Arduino nano*
* ESP8266 wifi module 
* Arducam Mini Module Camera Shield
* August Smart Lock

# Design Doc Specifications 

## Arduino Code - Roles
Originally the arduino's main role will be to control a camera to establish establish communication over wifi with a Web Server. The camera data would have been pushed to a local server immediatley for processing (no memory on an arduino to store images). However, the images are too low quality for any relevant video processing. Useful Camera information would require more powerful components such as a Rasberry pi. 

The arduino should be used for a very specifc repeatble task, which is limited by fast I/O and unique analog sensors. The arduino will be use a passive infrared sensor (PIR) or a laser trip sensor to log both TimeIN/TimeOut of people entering the home and control an entrance light. 

### freeRTOS
![Alt](Arduino_State_Diagram.svq)


## Image Processing Server
The server (either local or in the cloud) use OpenCV to perfrom intelligent analysis on the data provided. The server will then stream the images/video to a web interface with results from the analysis, so that the user can act on the situation. 

## Web page 
The web page will display the video gathered from the Arducam camera along with the results of the analysis of the image processing server. The dashboard uses a CSS gridlayout to Layout different React Components for each type of information - e.g. A camera feed, a time stamp of entering. 



`

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


## Arduino Code 
Arduino's main role will be to control the camera ,and establish communication over wifi with a server for image processing.  The Arduino should be listening for commands over wifi from the user manually or from a google home request.

## Image Processing Server
The server (either local or in the cloud) will use OpenCV to perfrom intelligent analysis on the data provided. The server will then stream the images/video to a web interface with results from the analysis, so that the user can act on the situation. 

## Web page 
The web page will display the video gathered from the Arducam camera along with the results of the analysis of the image processing server. 








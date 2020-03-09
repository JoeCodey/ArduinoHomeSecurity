# Self configuring Network
Design doc for new feature for Arduino Home Security.

## Abstract
* New feature for Arduino Home Security
* Arduino should be able to find an appropriate network  connection automatically to dump data from sensors OR if no network connection is available store as much data as possible locally. 

\*Arduino should refer to any compatible board {Atmega8, Atmega156, Atmega256}. And code should be indepentent of platform.

## Networking Currently

* Currently, the Arduino (Atmega256 in this case) must make a connection to a python TCP/UDP socket on **setup**. Otherwise, only LEDs display security events (e.g. motion sensed).

## new features / changes 

### local storage
* if no network is available, the Arduino should store as much data locally as possible until it runs out of memory.
	* As memory becomes constrained, arduino will save only  most recent data.
* If a network becomes available at any time, the arduino should attempt to connect to the network and dump sensor data from memory
	* **Note** : the arduino will have to check for a network periodically.

### Listen for connection and connect 
* The arduino should listen periodically for a connection on a trusted ip adress and port. 
* Should not interfere with detection of events.
	* e.g. checking for a network connection should not prevent a motion event from being detected. 
	* This can be prevents with interputs and scheduler when Real-Time OS integration is implemented. 

> Written with [StackEdit](https://stackedit.io/).

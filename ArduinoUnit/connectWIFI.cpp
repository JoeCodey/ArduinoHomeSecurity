/*
make the connections without tx and rx first,then upload the code connect tx,rx and the reset arduino
Wiring - 
 LM35             Arduino
 Pin 1            5V
 Pin 2            A0
 Pin 3            GND
 
 ESP8266          Arduino
 CH_PD,VCC        3.3V
 GND              GND
 TX               RX (Arduino)
 RX               TX (Ardino)
 Written By
 Angelin John
 Last Update - 
 January 19, 2017
 
*/

#include "EspTools.hpp"




//Connect to WiFi when Arduino starts up. One time run called during void setup().
int connectWiFi(String SSID, String PASS){
  Serial.println("AT+CWMODE=3");//wifi mode
  delay(2000);
  String cmd="AT+CWJAP=\"";//join access point
  cmd+=SSID;
  cmd+="\",\"";
  cmd+=PASS;
  cmd+="\"";
  Serial.println(cmd);
  delay(15000); //it takes some time to connect to WiFi and get an IP address
}


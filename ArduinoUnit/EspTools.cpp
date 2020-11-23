#include "EspTools.h"


void checkSerialResponse() {
    delay(1000);
    // Check to to see if ESP8266 responds
    // prints the command sent and the response 
    //(i.e. everything received by the ESP serial port)
    String message = "s-----s\n"; 
    char inChar; // Where to store the character read
    while(Serial1.available() > 0) {
        inChar = Serial1.read() ; 
        message = message + inChar ; 
    }
    message = message + "\ne-----e" ; 
        Serial.println(message);
}

EspTools::EspTools() {}


EspTools::attemptConnection(String ip_address, CommProtocol protocolChoice)
{
    char *serial_cmd[50];
    String protocol;
    switch (protocolChoice)
    {case TCP:
        protocol = "TCP";
        break;
    case UDP:
        protocol = "UDP";
        break;
    }
    Serial.println("protocol selected: " + protocol);
    String cmd = "AT+CIPSTART=\"" + protocol + "\",\""; //set up TCP connection
    cmd += ip_address;
    cmd += "\",8080";

    Serial.println("startTCP command: \n" + cmd);
    Serial1.println(cmd);
    delay(1500);
    //checkSerialResponse() ; 
    // Respones from ESP8266 { Ok, ERROR}
    if (Serial1.find("OK"))
    {
        Serial.println("TCP Connected @"+ip_address);
        return 1 ; 
    }else if (Serial1.find("ERROR"))
    {
        Serial.println("AT+CIPSTART Error");
        return 0 ;
    }else if(Serial1.find("ALREADY CONNECTED")){    
        return 1; 
    }
}

EspTools::sendEvent_TCP(String data)
{
    String cmd;
    int failFlag = 0 ; 
    cmd += data;
    Serial1.print("AT+CIPSEND="); //send TCP/IP data
    Serial1.println(cmd.length());
    //cmd.toCharArray(serial_cmd,sizeof(serial_cmd));
    //Serial1Com.write(serial_cmd.length());
    delay(1000);
    // delay(1000);
    Serial1.println(cmd);
    //delay(3000);
    //checkSerialResponse() ;
     
    if (Serial1.find(">"))
    {
        //send commmand
        Serial1.println(cmd);
        failFlag = 1 ; // Successful Transmission 
    }else {
        Serial.println("AT+CIPSEND error");
    }
    return failFlag ;
}

EspTools::connectWIFI()
{
    //Connect to WiFi when Arduino starts up. One time run called during void setup().
    Serial.println("AT+CWMODE=3"); //wifi mode
    delay(2000);
    String cmd = "AT+CWJAP=\""; //join access point
    cmd += SSID;
    cmd += "\",\"";
    cmd += PASS;
    cmd += "\"";
    Serial.println(cmd);
    delay(15000); //it takes some time to connect to WiFi and get an IP address
}


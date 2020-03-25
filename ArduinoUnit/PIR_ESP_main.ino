

#include "EspTools.hpp" 


#define IP "192.168.2.68"

int ledPin = 43;                // choose the pin for the LED
int inputPin = 35;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status
int eventId = 0 ; 
String message = "";

// SoftwareSerial Serial1(19,18);

EspTools esptools ; 


void setup(){
    pinMode(ledPin, OUTPUT);      // declare LED as output∏
    pinMode(inputPin, INPUT);     // declare sensor as input
    Serial.begin(9600);
    Serial1.begin(9600) ; // baud rate of MY (yours may be different)ESP8266
    delay(1000);
    Serial1.println("AT");
    delay(5000);
    // check that ESP8266 is reponsive
    if(Serial1.find("OK")){
        Serial.println("OK");
        // connectWiFi();
        esptools.attemptConnection(IP, esptools.TCP);
        delay(1000);
    }else{
        Serial.println("ESP8266 unresponsive!!");

    }
}

void loop(){

    val = digitalRead(inputPin);// read input value

    if (val == HIGH) {            // check if the input is HIGH
        digitalWrite(ledPin, HIGH);  // turn LED ON
        if (pirState == LOW) {
        // we have just turned on
        Serial.println("Motion detected!");
        eventId++;
        message = "TCPmessage: Motion Event Detected id_#"; 
        
        if(!esptools.sendEvent_TCP(message)) Serial.println("message send failed");
        // We only want to print on the output change, not state
        pirState = HIGH;
        }
    } else {
    
        digitalWrite(ledPin, LOW); // turn LED OFF
        if (pirState == HIGH){
        // we have just turned of
        Serial.println("Motion ended!");
        
        if(!esptools.sendEvent_TCP("TCPmessage: Motion Event ended id_#"))  Serial.println("message send failed");
        // We only want to print on the output change, not state
        pirState = LOW;
        }
    }
}





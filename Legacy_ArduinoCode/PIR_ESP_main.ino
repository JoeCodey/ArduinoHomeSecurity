
#include "EspTools.h"

#define IP "192.168.2.68"



int ledPin = 43;                // choose the pin for the LED
int inputPin = 35;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;
unsigned long referenceTime = 0 ;                     // variable for reading the pin status


// SoftwareSerial Serial1(19,18);

EspTools esptools ; 

// void test() {
//     aunit::TestRunner::run(); 
// }
bool networkConnection = false ; 


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

void localMode(){
     /**
      * Store data collected on board temporaily
      * Check for network connection periodically 
      * Delete oldest data when on board memory is full
      */ 
     int memoryAvailable  = 0 ; // (Must Implement)
     while(networkConnection == false ){

     }

}

void detectMotion(bool netStatus){

    if (val == HIGH) {            // check if the input is HIGH
        digitalWrite(ledPin, HIGH);  // turn LED ON
        if (pirState == LOW) {
        // we have just turned on
        Serial.println("\t--serial-- Motion detected!");
        
        String message = "TCPmessage: Motion Event Detected"; 
        if(netStatus){
            if(!esptools.sendEvent_TCP(message)) Serial.println("message send failed");
        }
        // We only want to print on the output change, not state
        pirState = HIGH;
        }
    } else {
        digitalWrite(ledPin, LOW); // turn LED OFF
        String message = "TCPmessage: Motion Event ended" ; 
        if (pirState == HIGH){
        Serial.println("\t--serial-- Motion ended!");
        if(netStatus){
            if(!esptools.sendEvent_TCP(message)) Serial.println("message send failed");
        }
        // We only want to print on the output change, not state
        pirState = LOW;
        }
    }
}

int networkCheckInterval = 30 * 1000 ; // in miliseconds 
void loop(){
    unsigned long currentTime = millis(); 
    if(networkConnection == false){ // ... future should make AT cmd to ESP
        if (currentTime - referenceTime >= networkCheckInterval){
            referenceTime = currentTime ; 
            Serial.println("***\t Attempting to connect ...  ");
            if(esptools.attemptConnection(IP,esptools.TCP) == true){
                networkConnection = true ; 
            }
        }
    }
    
    val = digitalRead(inputPin);// read input value

    detectMotion(networkConnection); 

}





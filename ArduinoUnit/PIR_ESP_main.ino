
#include "espTools.hpp" 

#define IP "127.0.0.1" 

int ledPin = 43;                // choose the pin for the LED
int inputPin = 35;               // choose the input pin (for PIR sensor)
int pirState = LOW;             // we start, assuming no motion detected
int val = 0;                    // variable for reading the pin status



void setup(){
    pinMode(ledPin, OUTPUT);      // declare LED as output∏
    pinMode(inputPin, INPUT);     // declare sensor as input

    Serial.begin(9600) ; // baud rate of ESP8266
    Serial.println("AT");
    delay(5000);
    // check that ESP8266 is reponsive
    if(Serial.find("OK")){
        Serial.println("OK");
        // connectWiFi();
        startTCP(IP);
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
        if(!sendEvent_TCP("TCP messaage: \n\t Motion detected!")) return;
        // We only want to print on the output change, not state
        pirState = HIGH;
        }
    } else {
    
        digitalWrite(ledPin, LOW); // turn LED OFF
        if (pirState == HIGH){
        // we have just turned of
        Serial.println("Motion ended!");
        if(!sendEvent_TCP("TCP message: \n\t Motion detected!")) return;
        // We only want to print on the output change, not state
        pirState = LOW;
        }
    }
}



// void setup(){
//   Serial.begin(115200);
//   String cmd = "AT+CIPSTART=\"TCP\",\"";//set up TCP connection
//   cmd += IP;
//   cmd += "\",80";
//   Serial.println(cmd);
// }

// void loop(){
//     String cmd = "AT+CIPSTART=\"TCP\",\"";//set up TCP connection
//   cmd += IP;
//   cmd += "\",80";
//   Serial.println(cmd);


// }


#include "AUnit.h"

#include "/Users/josephlefebvre/ArduinoHomeSecurity/ArduinoUnit/EspTools.h"
#include "/Users/josephlefebvre/ArduinoHomeSecurity/ArduinoUnit/EspTools.cpp"
#include <EEPROM.h> 
#define IP "192.168.2.68"

EspTools esptools ; 
// test(correct) {
//   int x = 1;
//   assertEqual(x, 1);
// }


test(responsive){
  int reply=0 ; 
  Serial1.println("AT");
  delay(2000);
  if(Serial1.find("OK")){
      //ESP8266 is alive and Responsive
      reply = 1 ;
      Serial.println("**\tESP is responsive!") ;
  }
  //checkSerialResponse();
  assertEqual(reply,1);
} 

test(attemptConnection){
  
  int reply = esptools.attemptConnection(IP,esptools.TCP);
  //checkSerialResponse() ; 
  assertEqual(reply,1) ; 
}

// test(writeByteToEEPROM){
//   //!!! Only run this test when specifically testing EEPROM !
//   // (don't want to waste read/write cycles)
//   int addr = 0 ; 
//   byte val = 5 ; 
//   EEPROM.write(addr,val); 
//   byte valStored= EEPROM.read(addr);
//   Serial.print("***\tvalStored -> ");
//   Serial.println(valStored);
  
//  assertEqual(val,valStored);  
//   //Serial.println(freeMemory());
// }

void setup() {
  delay(1000); // wait for stability on some boards to prevent garbage Serial
  Serial.begin(9600); // Serial port for debugging ESP8266 responses 
  Serial1.begin(9600); // Communication with ESP8266 
  delay(3000); // wait for statbility 

  //while(!Serial); // for the Arduino Leonardo/Micro only
}

void loop() {
  // Should get:
  // TestRunner summary:
  //    1 passed, 1 failed, 0 skipped, 0 timed out, out of 2 test(s).
  aunit::TestRunner::run();

  
}
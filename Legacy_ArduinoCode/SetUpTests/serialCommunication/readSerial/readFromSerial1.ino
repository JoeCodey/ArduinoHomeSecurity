uint32_t period = 1000;       // 2 seconds

HardwareSerial &ESP_Serial1 = Serial1 ; 


void setup() {
    Serial.begin(9600);   
    ESP_Serial1.begin(9600);
    delay(2000) ; 
    Serial.println("Setting up ... ") ; 
    Serial1.println("AT");
}

void loop() {

    
            checkSerialResponse() ; 
    
    Serial.println("Results?");
    delay(2000) ;
    Serial.println("Sending AT command");
    Serial1.println("AT");
    delay(5000) ; 
}


void checkSerialResponse() {
    // Check to to see if ESP8266 responds
    // prints the command sent and the response 
    //(i.e. everything received by the ESP serial port)
    String message = ""; 
    char inChar; // Where to store the character read
    while(Serial1.available() > 0) {
        inChar = Serial1.read() ; 
        message = message + inChar ; 
    }
        Serial.println(message);
}
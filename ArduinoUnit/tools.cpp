#include "espTools.hpp"

    int startTCP(String IP ) {
        

        String cmd = "AT+CIPSTART=\"TCP\",\"";//set up TCP connection
        cmd += IP;
        cmd += "\",65432";
        Serial.println(cmd);
        delay(1000);
        if(Serial.find("Error")){
            Serial.println("AT+CIPSTART Error");
            return 0;
        }
        return 1;

    } 

    int sendEvent_TCP(String data){
        String cmd ; 

      
        cmd += data ;
        Serial.print("AT+CIPSEND=");//send TCP/IP data
        Serial.println(cmd.length());
        delay(1000);
        delay(1000);
        Serial.print(cmd); 
        if(Serial.find(">")){ 
            Serial.print(cmd); 
            return 1 ;
        }
        else
            Serial.println("AT+CIPSEND error");
            return 0 ; 

    }







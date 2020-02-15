 #include "espTools.hpp"

    int startTCP(String ip_address ) {
        char *serial_cmd[50] ;

        String cmd = "AT+CIPSTART=\"TCP\",\"";//set up TCP connection
        cmd += ip_address;
        cmd += "\",8080";
        //cmd.toCharArray(serial_cmd,sizeof(serial_cmd));
        delay(1000);
        Serial.print("startTCP command: "+cmd);
        Serial1.println(cmd);
        delay(5000);
        if(Serial1.available()) Serial.println(Serial1.read());
        if(Serial1.find("OK")){
        Serial.println("TCP is OK!");
        // connectWiFi();
        }
    

        if(Serial1.find("Error")){
            Serial.println("AT+CIPSTART Error");
            return 0;
        }
        return 1;

    } 

    int sendEvent_TCP(String data){
        String cmd ; 
        char *serial_cmd[50] ;
      
        cmd += data ;
        Serial1.print("AT+CIPSEND=");//send TCP/IP data
        Serial1.println(cmd.length());
        //cmd.toCharArray(serial_cmd,sizeof(serial_cmd));
        //Serial1Com.write(serial_cmd.length());
        delay(1000);
        delay(1000);
        Serial1.println(cmd); 
        if(Serial1.find(">")){ 
            Serial1.println(cmd); 
            Serial.println("send: "+cmd);
            return 1 ;
        }
        else
            Serial.println("AT+CIPSEND error");
            return 0 ; 

    }






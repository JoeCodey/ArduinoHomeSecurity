


#ifndef ESPTOOLS_H
#define ESPTOOLS_H

#include <Arduino.h>

class EspTools
{
public:
    EspTools();

    enum CommProtocol
    {
        TCP,
        UDP
    };

    String SSID = "desired network" ; 
    String PASS = "not a password" ; 

    int connectWIFI();
    int attemptConnection(String IP, CommProtocol protocol);
    int sendEvent_TCP(String data);
};

#endif


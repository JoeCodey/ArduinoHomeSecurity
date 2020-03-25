
#include <Arduino.h>
#ifndef CONNECTWIFI_H_INCLUDED
#define CONNECTWIFI_H_INCLUDED

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
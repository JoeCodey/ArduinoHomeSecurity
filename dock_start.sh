#!/bin/bash 

export HOST_IP=$(ipconfig getifaddr en0)    
echo $HOST_IP
echo $1

if [ $1 = "prod" ] 
then 
    echo "Building in Production mode"
    docker-compose -f docker-compose.prod.yml up --build
#Spin Up in Development mode 
else 
    echo "Building in Dev mode "
    docker-compose up --build
fi
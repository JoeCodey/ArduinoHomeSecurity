#!/bin/bash 

export HOST_IP=$(ipconfig getifaddr en0)
echo $HOST_IP
docker-compose up 
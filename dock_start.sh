#!/bin/bash 

export HOST_IP=$(ipconfig getifaddr en0)  
# Run 'arp -a' and store IP addresses in the 'ip_addresses' array
ip_addresses=($(arp -a | awk '{ print $2 }' | tr -d '()'))

# Convert the array to a space-separated string
ip_addresses_str=$(echo "${ip_addresses[@]}")

# Export the variable
export HOST_DEVICES_ON_NETWORK="$ip_addresses_str"

# Print the exported variable to verify
echo "Exported HOST_DEVICES_ON_NETWORK: $HOST_DEVICES_ON_NETWORK"

echo $HOST_IP
echo $1
echo $2

if [ "$1" = "prod" ] && [ "$2" = "nodb" ]; then
    echo "Building without restarting db mode"
    echo "docker-compose -f docker-compose.prod.yml up -d --no-deps --build frontend backend redis &"
    docker-compose -f docker-compose.prod.yml up -d --no-deps --build frontend backend redis &
elif [ "$1" = "prod" ]; then
    echo "Building in Production mode"
    docker-compose -f docker-compose.prod.yml up --build
else
    echo "Building in Dev mode"
    docker-compose -f docker-compose.dev.yml up --build
fi

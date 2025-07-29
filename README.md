# Pseudo MQTT Client to send timestamps

This Docker Container + Shell Script aims to send the current timestamp into the topic **"time"** to simulate a light barrier

## Needed Modules

- Docker
- Mosquitto

## How to run

1. Open port 1883 in firewall using ```sudo firewall-cmd --zone=public --add-port=1883/tcp --permanent```
2. Reload firewall using ```sudo firewall-cmd --reload```
3. Start docker container using ```sudo docker compose -f pseudo-mqtt.yml up --build```
4. Change IP address in **send-time.sh** to host machine IP address
5. Execute **send-time.sh**

### Verify

To verify, that the setup works, you need to have the following things installed:

- Mosquitto

Once mosquitto is installed, you can subscribe the the topic using ```mosquitto_sub -h <ip-address-of-broker> -t time``` and when the **send-time.sh** script is executed, you can see the current time in the shell

## Used Links

- https://hub.docker.com/_/eclipse-mosquitto
- https://mosquitto.org/man/mosquitto-conf-5.html

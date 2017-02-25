# MQTT-RS-GTW
Simple mqtt gateway passing messages from serialline to mqtt broker and from broker to serialline:

##Implemented Features
- Configurable logging levels
- Configurable logging target ( Console, Syslog )
- Configurable topic names
- MQTT Publish with Qos 0
##Missing Features
-  

##Example HW setup
```
                                          _____________________________________      
 Pressure     _______________            |           RASPBERRYPI              |
 _____       |   ARDUINO     |           |                                    |
|     |______|               |           |______     __________     ________  |
|_____|      |               |   USB     |      |   |         |   |        |  |
             |               |<=========>|gtw.py|<=>|Mosquitto|<=>|Openhab |  |
Humidity/Temp|               |           |______|   |_________|   |________|  |
 _____       |               |           |                                    |
|     |______|               |           |                                    |
|_____|      |_______________|           |____________________________________|

```
##Protocol
Simple ASCII protocol where messages start with specific msgstart character. 
Message fields are separeted with specific separator character.
Message ends with \n leading \r is accepted also following example:
```
D|20.1|30.8|990\n
```
 - D is msg startcharacter
 - | is separator character
 

##Usage
```
./gtw.py -f myConfig.cfg

```

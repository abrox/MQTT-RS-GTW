# MQTT-RS-GTW

Simple mqtt gateway passing messages from serialline to mqtt broker and from broker to serialline.

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

- Help and available options:
```
./gtw.py -h
usage: gtw.py [-h] --file FILE [--log {INFO,DEBUG,WARN,ERR,CRITICAL}]
              [--log_target {SYSLOG,STDOUT}]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  Configuration file path
  --log {INFO,DEBUG,WARN,ERR,CRITICAL}, -l {INFO,DEBUG,WARN,ERR,CRITICAL}
                        Sets log level
  --log_target {SYSLOG,STDOUT}, -lt {SYSLOG,STDOUT}
                        Sets log target
```
- Run directly from commandline 
```
./gtw.py -f myConfig.cfg

```
- Use as systemD service:
Check from *mqqt-rs-gtw.service* file   that your **WorkingDirectory** and **ExecStart ** are pointing  correct place. 
And do following:
```
sudo cp mqqt-rs-gtw.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable mqqt-rs-gtw.service
sudo systemctl start mqqt-rs-gtw.service
```


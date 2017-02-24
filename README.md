# MQTT-RS-GTW
Simple mqtt gateway passing messages from serialline to mqtt broker and from broker to serialline.

Examample setup:

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


```

./gtw.py -f

```

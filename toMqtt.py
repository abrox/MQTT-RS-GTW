
#!/usr/bin/env python
'''
The MIT License (MIT)
Copyright (c) 2017  Jukka-Pekka Sarjanen
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
import communication as cm
import config as cfg
import Queue
import paho.mqtt.client
import logging
import defs

class Monitor():
    def __init__(self,args):
        self.state ='uc'
        self.alive = True
        self.queue = Queue.Queue( maxsize=20 )# Just prevent's increase infinity...

        self.logger = logging.getLogger('mqtt-rs-gtw')
        cfgHandler = cfg.ConfigHandler(args.file)

        self.port = cm.ArduinoIf( cfgHandler.getSerialCfg(), self)

        #Setup Mqtt client and items to publishToBroker
        serverCfg = cfgHandler.getMqttConfig()
        self.mqttClient = paho.mqtt.client.Client()
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_disconnect = self.on_disconnect
        self.MqttItems = cfgHandler.getPublishItems()

        #COnnect to server an open serial port
        self.logger.info("Mqtt loop starting.." + str(serverCfg))
        self.mqttClient.loop_start()
        self.mqttClient.connect_async(serverCfg[defs.KEY_MQTT_SERVER], 
                                      port=serverCfg[defs.KEY_MQTT_SERVERPORT],
                                      keepalive=30)

        self.port.start()

    def putQ(self, msg):
        '''Callback function handling incoming messages'''
        rc=self.alive
        try:
            self.queue.put(msg,False)
        except Queue.Full,e:
            self.logger.error('Queue overflow: '+ str(e))
            self.alive = False #No reason to continue 
            rc= False
        return rc
    
    def runMe(self):

        while(self.alive):
            try:
                data = self.queue.get()
                self.publishToBroker(data)
            except Queue.Empty:
                pass
                
        self.mqttClient.loop_stop()
        self.logger.debug('Main Thread say bye bye')

        self.port.alive = False
        self.port.join()

    def on_connect(self,client, userdata, flags, rc):
        self.logger.info("Connected")
        self.state ='co'

    def on_disconnect(self,client, userdata, rc):
        self.logger.warning("Disconnect rc:"+str(rc))
        self.state ='uc'

    def publishToBroker(self,data):
        self.logger.debug('msgin:'+data)
        try:
            msgStart  = data[:1]
            DataDef   = self.MqttItems[msgStart]
            separator = DataDef[defs.KEY_SEPARATOR]
            topics    = DataDef['topics']

            msgData = data.split(separator)
            msgData = msgData[1:] #Remove msg start byte from data

            if(len(msgData) == len(topics)):
                for t,d in zip(topics.values(),msgData):
                    self.mqttClient.publish(t,d)
                    self.logger.debug('publishToBroker:'+t+'data:'+d)
            else:
                self.logger.error('invalid msg content'+str(msgData))
        except KeyError, e:
            self.logger.error('Invalid msg strart byte:'+ str(e))



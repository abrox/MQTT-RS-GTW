
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
import time
import Queue
import paho.mqtt.client
import logging

class Monitor():
    def __init__(self,args):
        self.logger = logging.getLogger('mqtt-rs-gtw')
        self.cfgHandler = cfg.ConfigHandler(args.file)
        self.cfg = self.cfgHandler.getMqttConfig()
        self.queue      = Queue.Queue( maxsize=20 )# Just prevent's increase infinity... 
        self.port       = cm.ArduinoIf( self.cfgHandler.getSerialCfg(), self)
        self.alive      = True
        self.mqttClient = paho.mqtt.client.Client()
        self.mqttClient.on_connect = self.on_connect
        self.state ='uc'
        self.port.start()

       
    def putQ(self, msg):
        '''Callback function handling incoming messages'''
        rc=self.alive
        try:
            self.queue.put(msg,False)
        except Queue.Full,e:
            print('Queue overflow: '+ str(e))
            self.alive = False #No reason to continue 
            rc= False
        return rc
    
    def runMe(self):
        while(self.alive):
            if self.state == 'uc':
                print self.cfg
                self.mqttClient.connect(self.cfg['host'], port=self.cfg['serverport'])
                print 'dss'
            try:
                data = self.queue.get(block=False)
                l = data.split('|')
                print l
                if self.state == 'co':
                    self.publish(l)
                
            except Queue.Empty:
                print "empty"
                
            self.mqttClient.loop()
        print('Main Thread say bye bye')
        self.port.alive = False
        self.port.join()

    def on_connect(self,client, userdata, flags, rc):
        print ("Connected")
        self.state ='co'
        
    def publish(self,l):
        if len(l)>= 3:
            if l[0]=='D': 
                self.mqttClient.publish("jukkis/hum",l[1])
                self.mqttClient.publish("jukkis/temp",l[2])
                self.mqttClient.publish("jukkis/press",l[3])






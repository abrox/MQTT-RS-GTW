import communication as cm
import time
import Queue
import signal
import sys
import paho.mqtt.client

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        monitor.alive=False

signal.signal(signal.SIGINT, signal_handler)

class Monitor():
    def __init__(self,cfg):
        self.queue      = Queue.Queue( maxsize=20 )# Just prevent's increase infinity... 
        self.port       = cm.ArduinoIf( cfg, self)
        self.alive      = True
        self.mqttClient = paho.mqtt.client.Client()
        self.mqttClient.on_connect = self.on_connect
        self.cfg = cfg
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
                self.mqttClient.connect(self.cfg['host'], port=self.cfg['Serverport'])
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
def main(  ):
    global monitor
    cfg={'port':'/dev/ttyACM0','speed':'9600','Serverport':'1883','host':'localhost'}
    monitor = Monitor(cfg)
    monitor.runMe() 
    
if __name__ == '__main__':
    main()






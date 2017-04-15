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
from ConfigParser import SafeConfigParser
import logging
import sys
import defs

class ConfigError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ConfigHandler():
    def __init__(self,cfgFile):
        self.logger = logging.getLogger('mqtt-rs-gtw')
        self.parser = SafeConfigParser(defaults={defs.KEY_SEPARATOR:'|',
                                                 defs.KEY_MQTT_SERVERPORT:'1883',
                                                 defs.KEY_MQTT_SERVER:'localhost',
                                                 defs.KEY_MQTT_QOS:'0'}
                                       )
        files       = self.parser.read(cfgFile)

        if( len(files)== 0 ):
            self.logger.error("Configuration file: %s does not exist"%cfgFile)
            sys.exit(1)
    
    def __getCfg(self,section):
        cfg={}
        for name, value in self.parser.items(section):
            cfg[name] = value
        return cfg

    def getSerialCfg(self):
        return self.__getCfg('SERIAL')

    def getMqttConfig(self):
        return self.__getCfg('MQTT')

    def getMqttPubItems(self):
        '''Extract outgoing mqtt message definations from config file'''
        theItems={}
        for section_name in self.parser.sections():
            if 'MQTT_TO_BROKER' in section_name:
                msgstart  = self.parser.get(section_name,defs.KEY_MSGSTART)
                separator = self.parser.get(section_name,defs.KEY_SEPARATOR)

                d={}
                for key,val in self.parser.items(section_name):
                    try:
                        d[int(key)] = val #store only stuff that have numeric key, aka position in message
                    except ValueError:
                        pass

                theItem={defs.KEY_SEPARATOR:separator,'topics':d}
                if not  msgstart in theItems:
                    theItems[msgstart] = theItem
                else:
                    raise ConfigError('Duplicate msg defination!'+ msgstart)
        return theItems

    def getMqttSubItems(self):
        '''Extract incomming mqtt message definations from config file'''
        theItems={}
        for section_name in self.parser.sections():
            if 'MQTT_FROM_BROKER' in section_name:
                msgstart  = self.parser.get(section_name,defs.KEY_MSGSTART)
                topic     = self.parser.get(section_name,defs.KEY_TOPIC)
                maxLen    = self.parser.get(section_name,defs.KEY_MQTT_DATA_MAX_LEN)
                qos       = self.parser.get(section_name,defs.KEY_MQTT_QOS)
                #In case we have more than one subscribe items they should have 
                #different message start byte on serial.
                for val in theItems.values():
                    if val[defs.KEY_MSGSTART] == msgstart:
                        raise ConfigError('Duplicate msg start!'+ msgstart)

                theItem={defs.KEY_MSGSTART:msgstart,
                         defs.KEY_MQTT_DATA_MAX_LEN:maxLen,
                         defs.KEY_MQTT_QOS:qos}

                if not  topic in theItems:
                    theItems[topic] = theItem
                else:
                    raise ConfigError('Duplicate  mqtt topic defination!'+ topic)
        return theItems

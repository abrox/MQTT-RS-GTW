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
import argparse
import logging.handlers
import signal

from toMqtt import Monitor as bm 

def signal_handler(signal, frame):
        global monitor
        print('You pressed Ctrl+C!')
        monitor.alive=False

signal.signal(signal.SIGINT, signal_handler)

def handleCmdLineArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file','-f',help='Configuration file path',required=True)
    parser.add_argument('--log','-l',help='Sets log level',  choices=[ 'INFO','DEBUG', 'WARN','ERR','CRITICAL'],default='ERR')
    parser.add_argument('--log_target','-lt',help='Sets log target ',  choices=[ 'SYSLOG','STDOUT'],default='STDOUT')
    return parser.parse_args()

def createLogger(args):
    # create logger
    logger = logging.getLogger('mqtt-rs-gtw')
    level = { 'INFO':logging.INFO, 'DEBUG':logging.DEBUG, 'WARN':logging.WARN, 'ERR':logging.ERROR,'CRITICAL':logging.CRITICAL}
    logger.setLevel(level[args.log])
    
    #set log destination 
    ch=None
    if args.log_target == 'SYSLOG':
        ch = logging.handlers.SysLogHandler(address = '/dev/log')
    elif args.log_target == 'STDOUT':
        ch = logging.StreamHandler()

    ch.setLevel(level[args.log])
    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # add formatter to ch
    ch.setFormatter(formatter)
    # add ch to logger
    logger.addHandler(ch)
    
def main( args ):
    global monitor
    createLogger(args)
    monitor = bm(args)
    monitor.runMe() 
    
if __name__ == '__main__':
    main(handleCmdLineArgs())
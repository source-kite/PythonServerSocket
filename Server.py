##################################################

#       P26 ----> Relay_Ch1
#	P20 ----> Relay_Ch2
#	P21 ----> Relay_Ch3

##################################################
#!/usr/bin/python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
import SocketServer
import threading
from time import ctime,sleep
import Queue

Relay_CH1 = 26
Relay_CH2 = 20
SIGNAL_IN   = 24

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup( Relay_CH1, GPIO.OUT )
GPIO.setup( Relay_CH2, GPIO.OUT )
GPIO.setup( SIGNAL_IN, GPIO.IN )

GPIO.output( Relay_CH1, GPIO.HIGH )
GPIO.output( Relay_CH2, GPIO.HIGH )
 
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.
 
    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def SendTask( self ):
        while True:
            try:
                sleep( 0.1 )

                self.response_last_time = self.response_this_time
                self.response_this_time = GPIO.input( SIGNAL_IN )

                if self.response_this_time != self.response_last_time:
                    if GPIO.LOW == GPIO.input( SIGNAL_IN ):
                        print "R0"
                        self.request.sendall( "R0" )
                    else:
                        GPIO.output( Relay_CH1, GPIO.HIGH )
                        GPIO.output( Relay_CH2, GPIO.HIGH )
                        self.request.sendall( "R1" )
                        print "R1"
            except:
                print "Exit Tx"
                break

    def setup( self ): 
        print "Start serve"
        self.response_this_time = GPIO.input( SIGNAL_IN )
        self.thread_for_send = threading.Thread( target = MyTCPHandler.SendTask, args = ( self, ) )
        self.thread_for_send.setDaemon( True )
        self.thread_for_send.start()
        # self.thread_for_send.join()
    
    def handle( self ):
        while True:
            try:
                self.data = self.request.recv( 1024 )
                print self.data
                self.request.sendall( self.data )

                length = len( self.data )
                if "t" == self.data[0] and length >= 3:
                    if "0" == self.data[1]:
                        if "0" == self.data[2]:
                            GPIO.output( Relay_CH1, GPIO.HIGH )
                        else:
                            GPIO.output( Relay_CH1, GPIO.LOW )
                    else:
                        if "0" == self.data[2]:
                            GPIO.output( Relay_CH2, GPIO.HIGH )
                        else:
                            GPIO.output( Relay_CH2, GPIO.LOW )

                # elif "r" == self.data[0]:
                #     if GPIO.LOW == GPIO.input( SIGNAL_IN ):
                #         self.request.sendall( "R0" )
                #     else:
                #         self.request.sendall( "R1" )
                # else:
                #     print "Unknown request."
            except:
                print "Exit Rx"
                print "Stop serve"
                break
 
if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
 
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    print "Setup server."
 
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

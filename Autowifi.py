#!/usr/bin/python
import os, time
 
while True:
    if '192' not in os.popen('ifconfig | grep 192').read():
        print '\n****** wifi is down, restart... ******\n'
        os.system('sudo /etc/init.d/networking restart')
    time.sleep(5) #5 seconds 

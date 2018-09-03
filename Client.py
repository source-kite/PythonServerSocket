import socket
import sys
from time import sleep
 
HOST, PORT = "192.168.150.100", 9999
 
# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
toggle = 0
index = 0
str = [ "t00", "t01", "t10", "t11" ]
try:
    sock.connect((HOST, PORT))
    while 1:
        # Connect to server and send data
        index = (index + 1) % 4

        sock.sendall( str[ index ] )
        sock.sendall( "r" )

        # Receive data from the server and shut down
        received = sock.recv(1024)
        print received

        sleep( 1 )
finally:
    sock.close()
 

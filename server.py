import socket
import sys

def server_init():
    if(sys.argv[2]):
        BindPort = int(sys.argv[2])
    else:
        BindPort = int(input("Enter Bind Port: "))
        
    localIP = "127.0.0.1"
    bufferSize  = 256
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, BindPort))

    while(True):
        RecvMsg = UDPServerSocket.recvfrom(bufferSize)
        message = RecvMsg[0].decode()
        address = RecvMsg[1][1]
        print("{}".format(address), ": {}".format(message))

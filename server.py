import socket
import sys
from os import listdir

def server_init():  
    if(sys.argv[1]):
        ConnectionPort = int(sys.argv[1])
    else:
        ConnectionPort = int(input("Enter Connection Port: "))

    if(sys.argv[2]):
        BindPort = int(sys.argv[2])
    else:
        BindPort = int(input("Enter Bind Port: "))

    localIP = "127.0.0.1"
    ConnectionPort = (localIP, ConnectionPort)
    bufferSize  = 256
    resourcesPath = "./resources"

    print("Server: ",ConnectionPort, " ", BindPort)

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, BindPort))

    while(True):
        RecvMsg = UDPServerSocket.recvfrom(bufferSize)
        message = RecvMsg[0].decode()
        address = RecvMsg[1]
        port = address[1]
        if(message == "givelist?"):
            list = listdir(resourcesPath)
            list = str.encode("\n" + '\n'.join(list))
            print(address)
            UDPServerSocket.sendto(list, ConnectionPort)
        else:
            print("{}".format(port), ": {}".format(message))

import socket
import sys
from os import listdir
from utils import RecvMsg, app_recvMsg

#******************************************************************#
                                #Global
#******************************************************************#

#####################################
#        Get Connection Ports       #
#####################################  
# Who are we connecting to
if(sys.argv[1]):
    ConnectionPort = int(sys.argv[1])
else:
    ConnectionPort = int(input("Enter server port you want to connect to: "))

# What port are we binding to
if(sys.argv[2]):
    BindPort = int(sys.argv[2])
else:
    BindPort = int(input("Enter Bind Port: "))

# Setup global Variables
localIP = "127.0.0.1"
ConnectionPort = (localIP, ConnectionPort)
bufferSize  = 256
resourcesPath = "./resources"

list = listdir(resourcesPath)
sendList = str.encode("\n" + '\n'.join(list))

print("Server: ",ConnectionPort, " ", BindPort)

# Create server socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, BindPort))

#******************************************************************#
                            #Program Start
#******************************************************************#

#####################################
#          Start Listening          #
#####################################
def server_init():
    while(True):
        receivedMsg = RecvMsg(app_recvMsg(UDPServerSocket, bufferSize)).getRecvMsg()
        server_msgManager(receivedMsg)

#####################################
#          Message Manager          #
#####################################
def server_msgManager(msg: RecvMsg):
    if(msg.message == "givelist?"): givelist(msg)
    else:
        print(f"{msg.port}: {msg.message}")

def givelist(msg: RecvMsg):
    UDPServerSocket.sendto(sendList, msg.address)

    # rewrite this into some other function to read file
    # also will have to be split into packages
    receivedMsg = RecvMsg(app_recvMsg(UDPServerSocket, bufferSize)).getRecvMsg()
    f = open(resourcesPath + "/" + receivedMsg.message, "r")
    f = str.encode(f.read())
    UDPServerSocket.sendto(f, receivedMsg.address)

#******************************************************************#
#******************************************************************#
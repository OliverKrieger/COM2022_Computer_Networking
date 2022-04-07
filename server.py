import socket
import sys
from os import listdir
from utils import RecvMsg, app_recvMsg, app_sendMsg, readFile, Package
from header import makeRequest, Requests
from constants import c_buffer, s_buffer

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
bufferSize  = 32
resourcesPath = "./resources"

list = listdir(resourcesPath)
sendList = "\n" + '\n'.join(list)

print("Server: ",ConnectionPort, " ", BindPort)

# Create server socket
#UDP Server Socket
UDP_ss = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDP_ss.bind((localIP, BindPort))

#******************************************************************#
                            #Program Start
#******************************************************************#

#####################################
#          Start Listening          #
#####################################
def server_init():
    while(True):
        receivedMsg = RecvMsg(app_recvMsg(UDP_ss, s_buffer)).getRecvMsg()
        server_msgManager(receivedMsg)

#####################################
#          Message Manager          #
#####################################
def server_msgManager(msg: RecvMsg):
    if(msg.type == Requests.handshake.value): handshake(msg)
    elif(msg.type == Requests.givelist.value): givelist(msg)
    else:
        print(f"{msg.port}: {msg.message}")

#####################################
#           Functionality           #
#####################################
def handshake(msg: RecvMsg):
    print("Client Has said buffer size is:", msg.message)
    req = makeRequest([Requests.handshake.value], c_buffer.to_bytes(2, "little"))
    app_sendMsg(UDP_ss, req, msg.address)

def givelist(msg: RecvMsg):
    app_sendMsg(UDP_ss, str.encode(sendList), msg.address)

    # rewrite this into some other function to read file
    # also will have to be split into packages
    receivedMsg = RecvMsg(app_recvMsg(UDP_ss, s_buffer)).getRecvMsg()
    f = readFile(resourcesPath + "/" + receivedMsg.message)
    sendMessage(f, receivedMsg.address)
    #app_sendMsg(UDP_ss, f, receivedMsg.address)

def sendMessage(msg, addr):
    pck = Package(msg)
    initPckHandshake(pck, addr)
    pn = 1 # package counter
    while(True):
        print("server send pck nr ", pn)
        req = makeRequest([Requests.req.value, pn, pck.pt], pck.getListItem(pn-1))
        app_sendMsg(UDP_ss, req, addr)
        print("server waiting to send next pck")
        rMsg = RecvMsg(app_recvMsg(UDP_ss, s_buffer)).getRecvMsg()
        if(rMsg.type == Requests.fullyreceived.value):
            print("last sent: ", pck.getListItem(pn-1))
            break
        print("server received request for pck nr ", rMsg.pn)
        pn = rMsg.pn
    print("server finished sending msg")

def initPckHandshake(pck:Package, addr):
    print("server: Total packages to send is: ", pck.pt)
    #print("".join(pck.list))
    req = makeRequest([Requests.req.value, 0, pck.pt], bytes())
    app_sendMsg(UDP_ss, req, addr)

#******************************************************************#
#******************************************************************#
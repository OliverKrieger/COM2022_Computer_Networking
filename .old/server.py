from re import M
import socket
import sys
from os import listdir
from utils import RecvMsg, app_recvMsg, app_sendMsg, readFile, Package, PckListItem
from header import makeRequest, Requests
from constants import c_buffer, s_buffer

#******************************************************************#
                                #Global
#******************************************************************#

ToSendPackageList = list()

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
resourcesPath = "./resources"

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
        if(receivedMsg.pt != 0):
            addMessageQueue(receivedMsg)
        else:
            server_msgManager(receivedMsg)

#####################################
#          Message Manager          #
#####################################
def server_msgManager(msg: RecvMsg):
    if(msg.type == Requests.handshake.value): handshake(msg)
    elif(msg.type == Requests.givelist.value): givelist(msg)
    elif(msg.type == Requests.filereq.value): filereq(msg)
    elif(msg.type == Requests.req.value): pckRequest(msg)
    elif(msg.type == Requests.fullyreceived.value): removeFromPckList(msg)
    else:
        print(f"{msg.port}: {msg.message}")

#####################################
#           Functionality           #
#####################################

def addMessageQueue(msg: RecvMsg):
    print("msg queue called")
    listItem:PckListItem = findInPckList(msg.address)
    if(listItem == None):
        print("pck does not exist")
        pck:Package = Package(msg.message)
        addToPckToSendList(pck, msg.address)
        print("responding to client from new")
        res = makeRequest([Requests.res.value], bytes())
        app_sendMsg(UDP_ss, res, msg.address)
    else:
        print("pck does exist")
        print(listItem[0].getPck())
        pck:Package = listItem[0]
        pck.list.append(msg.bytes)
        if(msg.pn == msg.pt):
            print("pn ", msg.pn, " same as pt ", msg.pt)
            m = convertToMsg(pck)
            msg.bytes = m
            msg.message = m.decode("utf-8")
            server_msgManager(msg)
            ToSendPackageList.remove(findInPckList(msg.address))
            # removeFromPckList(msg) # will send client fully received pck
        print("responding to client from existing")
        res = makeRequest([Requests.res.value], bytes())
        app_sendMsg(UDP_ss, res, msg.address)

def convertToMsg(pck: Package):
    total = bytes()
    for byte in pck.list:
        total += byte
    return total

# Initial Server-client handshake
def handshake(msg: RecvMsg):
    print("Client Has said buffer size is:", msg.message)
    req = makeRequest([Requests.handshake.value], c_buffer.to_bytes(2, "little"))
    app_sendMsg(UDP_ss, req, msg.address)

# givelist functionality
def givelist(msg: RecvMsg):
    sendListTo(msg.address)

# Request list of items from resources
def sendListTo(addr):
    list = listdir(resourcesPath)
    sendList = "\n" + '\n'.join(list)
    pck = Package(sendList)
    initPckHandshake(pck, addr)

# Request file to be read from resources
def filereq(msg:RecvMsg):
    print("requesting file: ", msg.message)
    f = readFile(resourcesPath + "/" + msg.message)
    pck = Package(f)
    initPckHandshake(pck, msg.address)

# Add package to the list of packages that need to be sent
# and keep it until fully sent (only 1 per client)
def initPckHandshake(pck:Package, addr):
    addToPckToSendList(pck,addr)
    res = makeRequest([Requests.res.value, 0, pck.pt], bytes())
    app_sendMsg(UDP_ss, res, addr)

# Add package to the potential packages to send
def addToPckToSendList(pck,addr):
    # !!! ToDo only one package can be requested by a client, so
    # each address can only be added once!
    ToSendPackageList.append((pck,addr))

# Request a packet from the package list
def pckRequest(msg:RecvMsg):
    pck:Package = findInPckList(msg.address)[0] # first in tuple is msg
    print("responding with pck ", msg.pn)
    res = makeRequest([Requests.res.value, msg.pn, pck.pt], pck.getListItem(msg.pn-1))
    app_sendMsg(UDP_ss, res, msg.address)

# Request for once client fully received to remove from the packet list
def removeFromPckList(msg:RecvMsg):
    print("removing from pck list and responding to client: ", msg.address)
    ToSendPackageList.remove(findInPckList(msg.address))
    req = makeRequest([Requests.fullyreceived.value], bytes())
    app_sendMsg(UDP_ss, req, msg.address)

# Find package in the package list
def findInPckList(addr):
    item:PckListItem
    for item in ToSendPackageList:
        if(item[1] == addr):
            return item
    return None







#******************************************************************#
#******************************************************************#
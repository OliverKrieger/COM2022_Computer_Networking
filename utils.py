import socket
import string
import math
from header import headerSize

bufferSize = 32
realMsgSize = bufferSize - headerSize

#####################################
#              Classes              #
#####################################
class RecvMsg:
    def __init__(self, msg):
        self.type = msg[0][0]
        self.pn = msg[0][1]
        self.pt = msg[0][2]
        self.chks = msg[0][3]
        self.message = msg[0][headerSize:].decode()
        self.bytes = msg[0][headerSize:]
        self.address = msg[1]
        self.port = self.address[1]
    
    def getRecvMsg(self):
        return self

class Package: # package
    def __init__(self, msg):
        self.pt = getPackageNumber(bytes(msg, "utf-8"))
        self.list = splitPackage(bytes(msg, "utf-8"))

    def getPck(self):
        return self

    def getListItem(self, index):
        return self.list[index]


#####################################
#        Basic Functionality        #
#####################################

def app_input():
    Msg = str(input())
    return Msg

def app_recvMsg(socket: socket.socket, bufferSize):
    return socket.recvfrom(bufferSize)

def app_sendMsg(socket: socket.socket, Msg: bytes, address: int):
    #SendMsg = str.encode(str(Msg))
    SendMsg = Msg
    socket.sendto(SendMsg, address)

#####################################
#          File Management          #
#####################################

def readFile(path):
    f = open(path, "r")
    return f.read()

#####################################
#              Utility              #
#####################################

def printCommands():
    print("givelist - receive a list of files from the connected user")

def getPackageNumber(package: bytes):
    packageNumber = int(math.ceil(len(package) / (bufferSize - headerSize)))
    return packageNumber

def splitPackage(pck):
    n = getPackageNumber(pck)
   
    return [pck[x*realMsgSize:(x+1)*realMsgSize] for x in range(n)]
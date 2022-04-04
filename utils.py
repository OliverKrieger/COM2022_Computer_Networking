import socket
from header import headerSize

#####################################
#              Classes              #
#####################################
class RecvMsg:
    def __init__(self, msg):
        self.type = msg[0][0]
        self.message = msg[0][headerSize:].decode()
        self.address = msg[1]
        self.port = self.address[1]
    
    def getRecvMsg(self):
        return self


#####################################
#        Basic Functionality        #
#####################################

def app_input():
    Msg = str(input())
    return Msg

def app_recvMsg(socket: socket.socket, bufferSize):
    return socket.recvfrom(bufferSize)

def app_sendMsg(socket: socket.socket, Msg: str, address: int):
    SendMsg = str.encode(str(Msg))
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
    print("31 - receive a list of files from the connected user")
import socket
#####################################
#              Classes              #
#####################################
class RecvMsg:
    def __init__(self, msg):
        self.message = msg[0].decode()
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
    SendMsg = str.encode(Msg)
    socket.sendto(SendMsg, address)

#####################################
#          File Management          #
#####################################

def readFile(path):
    f = open(path, "r")
    return f.read()
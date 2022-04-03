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

def app_recvMsg(socket: socket.socket, bufferSize):
    return socket.recvfrom(bufferSize)
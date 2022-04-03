import socket
import sys
from utils import RecvMsg, app_recvMsg, app_sendMsg, app_input

#******************************************************************#
                                #Global
#******************************************************************#

# Who are we connecting to
if(sys.argv[1]):
    ConnectionPort = int(sys.argv[1])
else:
    ConnectionPort = int(input("Enter server port you want to connect to: "))

# Setup Global Variables
Dest = "127.0.0.1"
ConnectionPort = (Dest, ConnectionPort)
bufferSize  = 256

print("Client: ", ConnectionPort)

# Create Client Socket
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)        

#******************************************************************#
                            #Program Start
#******************************************************************#

#####################################
#          Start Listening          #
#####################################
def client_init():
    while(True):
        input = app_input()
        app_sendMsg(UDPClientSocket, input, ConnectionPort)
        client_msgManager(input)

#####################################
#          Message Manager          #
#####################################
def client_msgManager(input):
    if(input == "givelist?"): givelist()

def givelist():
    receivedMsg = RecvMsg(app_recvMsg(UDPClientSocket, bufferSize)).getRecvMsg()
    print(f"{receivedMsg.port}: {receivedMsg.message}")

    # rewrite this into a header msg about what you want
    # and function maybe
    print("which item would you like (enter filename exactly)")
    input = app_input()
    app_sendMsg(UDPClientSocket, input, ConnectionPort)
    receivedMsg = RecvMsg(app_recvMsg(UDPClientSocket, bufferSize)).getRecvMsg()
    print(f"{receivedMsg.port}: {receivedMsg.message}")

#******************************************************************#
#******************************************************************#
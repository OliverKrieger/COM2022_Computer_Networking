import socket
import sys

from sympy import EX
from utils import RecvMsg, app_recvMsg, app_sendMsg, app_input, printCommands
from header import makeRequest, Requests

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
bufferSize  = 32

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
    handshake()
    while(True):
        input = app_input()
        client_msgManager(input)

#####################################
#          Message Manager          #
#####################################
def client_msgManager(input):
    if(input == Requests.givelist.name): givelist(Requests['givelist'].value)
    elif(input == "help"): printCommands()
    else: print("Input unrecognized. Please try again or type 'help' for commands.")

#####################################
#           Functionality           #
#####################################
def handshake():
    req = makeRequest(Requests.handshake.value, bufferSize)
    app_sendMsg(UDPClientSocket, req, ConnectionPort)
    
    UDPClientSocket.settimeout(1)
    try:
        receivedMsg = RecvMsg(app_recvMsg(UDPClientSocket, bufferSize)).getRecvMsg()
        print("Server Has said buffer size is:", receivedMsg.message)
    except Exception as e:
        print(e)
        handshake()

# Give list functionality
def givelist(input):
    req = makeRequest(input, "")
    app_sendMsg(UDPClientSocket, req, ConnectionPort)
    receivedMsg = RecvMsg(app_recvMsg(UDPClientSocket, bufferSize)).getRecvMsg()
    print(f"{receivedMsg.port}: {receivedMsg.message}")

    # rewrite this into a header msg about what you want
    # and function maybe
    print("which item would you like (enter filename exactly)")
    input = app_input()
    req = makeRequest(Requests.req.value, input)
    app_sendMsg(UDPClientSocket, req, ConnectionPort)
    receivedMsg = RecvMsg(app_recvMsg(UDPClientSocket, bufferSize)).getRecvMsg()
    print(f"{receivedMsg.port}: {receivedMsg.message}")  

#******************************************************************#
#******************************************************************#
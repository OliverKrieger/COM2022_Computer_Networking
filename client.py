import socket
import sys
from numpy import byte

from sympy import EX
from utils import RecvMsg, app_recvMsg, app_sendMsg, app_input, printCommands
from header import makeRequest, Requests
from constants import c_buffer, s_buffer

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
    req = makeRequest([Requests.handshake.value], s_buffer.to_bytes(2, "little"))
    app_sendMsg(UDPClientSocket, req, ConnectionPort)
    
    UDPClientSocket.settimeout(1)
    try:
        receivedMsg = RecvMsg(app_recvMsg(UDPClientSocket, c_buffer)).getRecvMsg()
        print("Server Has said buffer size is:", receivedMsg.message)
    except Exception as e:
        print(e)
        handshake()

# Give list functionality
def givelist(input):
    req = makeRequest([input], bytes()) # get list
    app_sendMsg(UDPClientSocket, req, ConnectionPort)
    ServerItemsList = RecvMsg(app_recvMsg(UDPClientSocket, c_buffer)).getRecvMsg()
    print(f"{ServerItemsList.port}: {ServerItemsList.message}")

    print("which item would you like (enter filename exactly)")
    input = app_input()
    # ToDo - check that input is in the list of items returned! Otherwise ask again

    recv_pck = receivePck(receivePckHandshake(input))
    print(f"{ServerItemsList.port}: {recv_pck}")

def receivePckHandshake(input):
    req = makeRequest([Requests.req.value], str.encode(input))
    app_sendMsg(UDPClientSocket, req, ConnectionPort)
    return RecvMsg(app_recvMsg(UDPClientSocket, c_buffer)).getRecvMsg()

#parse message
def receivePck(initPck: RecvMsg):
    UDPClientSocket.settimeout(10)
    totalMsg = bytes()
    pn = 0
    while(pn <= initPck.pt):
        print("client wait for next pck")
        rMsg = RecvMsg(app_recvMsg(UDPClientSocket, c_buffer)).getRecvMsg()
        print("client received pck nr ", rMsg.pn)
        totalMsg += rMsg.bytes
        if(pn != initPck.pt):
            res = makeRequest([Requests.res.value, rMsg.pn+1], bytes())
            print("client requesting pck nr ", rMsg.pn + 1)
            app_sendMsg(UDPClientSocket, res, ConnectionPort)

        pn = rMsg.pn + 1

    res = makeRequest([Requests.fullyreceived.value], bytes())
    app_sendMsg(UDPClientSocket, res, ConnectionPort)
    print("last received: ", rMsg.message)
    print("client msg complete")
    return totalMsg.decode("utf-8")



#******************************************************************#
#******************************************************************#
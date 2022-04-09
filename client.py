import socket
import sys
from urllib.request import Request
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
    UDPClientSocket.settimeout(10)
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
# Client to server handshake
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

# givelist functionality
def givelist(input):
    # get list
    req = makeRequest([input], bytes()) 
    ServerItemsList = receivePckFromServer(newReq(req, Requests.res.value))
    print(f"{ServerItemsList[1]}: {ServerItemsList[0]}")

    # Which item to get from server
    # !!! ToDo only be able to request items on list!
    print("which item would you like (enter filename exactly)")
    input = app_input()

    # request file from the server
    req = makeRequest([Requests.filereq.value], str.encode(input))
    recv_pck = receivePckFromServer(receivePckHandshake(req))
    print(f"{recv_pck[1]}: {recv_pck[0]}")

# Packet Handshake
def receivePckHandshake(req):
    app_sendMsg(UDPClientSocket, req, ConnectionPort)
    return RecvMsg(app_recvMsg(UDPClientSocket, c_buffer)).getRecvMsg()

# Loop until all packets received
def receivePckFromServer(initPck: RecvMsg):
    totalMsg = bytes()
    pn = 1
    while(pn <= initPck.pt):
        req = makeRequest([Requests.req.value, pn], bytes())
        totalMsg += newReq(req, Requests.res.value).bytes
        pn += 1

    req = makeRequest([Requests.fullyreceived.value], bytes())
    res = newReq(req, Requests.fullyreceived.value)

    return (totalMsg.decode("utf-8"), res.address)

# Request - Response functionality
def waitRes(res:Request, req) -> RecvMsg:
    try:
        rMsg = RecvMsg(app_recvMsg(UDPClientSocket, c_buffer)).getRecvMsg()
        if(rMsg.type == res):
            return rMsg
        else:   # received wrong response type from server!
            waitRes(res, req)
    except Exception as e: # failed to get in time, so request again
        print(e)
        newReq(req, res)

def newReq(req, res:Request) -> RecvMsg:
    app_sendMsg(UDPClientSocket, req, ConnectionPort)
    return waitRes(res, req)

#******************************************************************#
#******************************************************************#
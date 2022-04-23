from importlib.resources import Package
import socket
import sys
from urllib.request import Request
from numpy import byte
import math

from sympy import EX
from utils import RecvMsg, app_recvMsg, app_sendMsg, app_input, printCommands, Package
from header import makeRequest, Requests, headerSize, Req
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
    req = makeRequest([input]) 
    ServerItemsList = receivePckFromServer(newReq(req, Requests.res.value))
    print(f"{ServerItemsList[1]}: {ServerItemsList[0]}")

    # Which item to get from server
    print("which item would you like (enter filename exactly)")
    input = validateInput(app_input(), ServerItemsList[0])

    # request file from the server
    req = makeRequest([Requests.res.value, 0, getPtSize(input)], str.encode(input))
    recv_pck = receivePckFromServer(receivePckHandshake(req))
    print(f"{recv_pck[1]}: {recv_pck[0]}")

def validateInput(input, checkList):
    values = checkList.split("\n")
    while(True):
        for i in values:
            if(input == i):
                return input
        print("\nInput not in possible items list. Please enter (exactly) one of the following:", checkList)
        input = app_input()

# Packet Handshake
def receivePckHandshake(req):
    r = Req(req)
    pt = int.from_bytes(r.pt, "little")
    input = r.message
    pck:Package = Package(input)
    if(pt > 0):
        pn = 1
        while(pn <= pt):
            req = makeRequest([Requests.filereq.value, pn, getPtSize(input)], pck.getListItem(pn-1))
            print("next request")
            res = newReq(req, Requests.res.value)
            print("received pck", res.pn)
            pn += 1
        print("returning res")
        return res
    else:
        app_sendMsg(UDPClientSocket, req, ConnectionPort)
        return RecvMsg(app_recvMsg(UDPClientSocket, c_buffer)).getRecvMsg()

# Loop until all packets received
def receivePckFromServer(initPck: RecvMsg):
    print("start requesting package, total size ", initPck.pt)
    totalMsg = bytes()
    pn = 1
    while(pn <= initPck.pt):
        print("requesting pck ", pn)
        req = makeRequest([Requests.req.value, pn], bytes())
        totalMsg += newReq(req, Requests.res.value).bytes
        pn += 1

    print("package sending complete, waiting for server to confirm")
    req = makeRequest([Requests.fullyreceived.value], bytes())
    res = newReq(req, Requests.fullyreceived.value)

    print("server confirmed, printing msg", res)
    return (totalMsg.decode("utf-8"), res.address)

# Request - Response functionality
def waitRes(res:Request, req) -> RecvMsg:
    try:
        rMsg = RecvMsg(app_recvMsg(UDPClientSocket, c_buffer)).getRecvMsg()
        print("response received")
        print("waiting for ", res, ", received ", rMsg.type)
        if(rMsg.type == res):
            print("returning ", rMsg)
            return rMsg
        else:   # received wrong response type from server!
            return waitRes(res, req)
    except Exception as e: # failed to get in time, so request again
        print(e)
        newReq(req, res)

def newReq(req, res:Request) -> RecvMsg:
    app_sendMsg(UDPClientSocket, req, ConnectionPort)
    return waitRes(res, req)


def getPtSize(input):
    input = str.encode(input)
    if(len(input) > s_buffer - headerSize):
        return int(math.ceil(len(input) / (s_buffer-headerSize)))
    else:
        return 0

#******************************************************************#
#******************************************************************#
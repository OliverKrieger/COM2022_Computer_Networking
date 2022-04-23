import socket
import math

from message import SocketMsg, Msg
from requests import Req, create_req
from header import Header, headerSize
import config

#####################################
#              Classes              #
#####################################
class Socket_Manager:
    def __init__(self, socket:socket.socket, bfr_size:int):
        self.socket = socket
        self.bfr_size = bfr_size
        self.req_manager = ReqManager(self)

    def a_recvMsg(self):
        return SocketMsg(self.socket.recvfrom(self.bfr_size))

    def a_sendMsg(self, m: bytes, address: tuple):
        print("new request to address ", address)
        self.socket.sendto(m, address)

    def a_request_until_finished(self, head:Header, m:bytes(), addr):
        total = bytes()
        while(head.si != head.lsi):
            # ToDO if want to send multi packet messages, then MUST remake header (otherwise return always has greater last slice 
            # index, even though its supposed to be 0)
            res:Msg = self.req_manager.newReq(create_req(head, m), addr)
            print("res is", res)
            total += res.bytes
            head = res.header
            head.si = head.si + 1
            head.lsi = head.lsi + 1
        return total

    def get_socket_manager(self):
        return self

class ReqManager:
    def __init__(self, sm:Socket_Manager):
        self.sm = sm

    # Request - Response functionality
    def waitRes(self, r:Req, adr:tuple) -> Msg:
        try:
            rMsg = Msg(self.sm.a_recvMsg())
            print("response from server")
            return rMsg
        except Exception as e: # failed to get in time, so request again
            print(e)
            self.newReq(r, adr)

    def newReq(self, r:Req, adr:tuple) -> Msg:
        self.sm.a_sendMsg(r.get_bytes(), adr)
        return self.waitRes(r, adr)

class Package: # package
    def __init__(self, msg, bfr_size):
        self.msg_Size = bfr_size - headerSize
        self.pt = getPackageNumber(bytes(msg, "utf-8"), self.msg_Size)
        self.list = splitPackage(bytes(msg, "utf-8"), self.msg_Size)

    def getPck(self):
        return self

    def getListItem(self, index) -> bytes:
        return self.list[index]

def a_input():
    Msg = str(input()) # guarantees input is returned in string format
    return Msg

def a_input_validation(input:str, checkList:list):
    values = checkList.split("\n")
    while(True):
        for i in values:
            if(input == i):
                return input
        print("\nInput not in possible items list. Please enter (exactly) one of the following:", checkList)
        input = a_input()

def getPackageNumber(package: bytes, msg_Size:int) -> int:
    packageNumber:int = int(math.ceil(len(package) / msg_Size))
    return packageNumber

def splitPackage(pck:bytes, msg_Size:int) -> list:
    n:int = getPackageNumber(pck, msg_Size)
    return [pck[x*msg_Size:(x+1)*msg_Size] for x in range(n)]
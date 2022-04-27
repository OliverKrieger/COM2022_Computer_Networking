import socket
import math
import os

from message import SocketMsg, Msg
from requests import Req, create_req
from header import Header, headerSize
import config

FailureCount = 0

#####################################
#              Classes              #
#####################################
class Socket_Manager:
    def __init__(self, socket:socket.socket, bfr_size:int):
        self.socket = socket
        self.bfr_size = bfr_size
        self.req_manager = ReqManager(self)

    def a_recvMsg(self):
        res:SocketMsg = SocketMsg(self.socket.recvfrom(self.bfr_size))
        m = Msg(res)
        chks = calculateChks(res.msg[4:]) # calculate checksum to anything but checksum itself
        if(m.header.chks != chks):
            print("received chks", m.header.chks, "and calc chks ", chks)
            raise ValueError("package is corrupted, it has a wrong checksum.")
        return res

    def a_sendMsg(self, r: Req, address: tuple):
        print("new package to address ", address)
        chks = calculateChks(r.get_bytes()[4:]) # calculate checksum to anything but checksum itself
        print("calculated checksum ", chks)
        r.head.set_chks(chks)
        #FOR FAILURE TEST
        if(config.TestFileSaveOnError == True):
            if(r.head.si == 2):
                r.head.set_chks(0)
        #END TEST
        self.socket.sendto(r.get_bytes(), address)

    def a_request_until_finished(self, head:Header, m:bytes, addr) -> bytes:
        total = bytes()
        while(head.si != head.lsi):
            # ToDO if want to send multi packet messages, then MUST remake header (otherwise return always has greater last slice 
            # index, even though its supposed to be 0)
            try:
                res:Msg = self.req_manager.newReq(create_req(head, m), addr)
            except ConnectionError as e:
                print("Request Failure:", e)
                # ToDO - save the current received message and packge to request to file
                raise ConnectionError("failed to request file index", (":" + str(head.fi) + ":" + str(total)))
            print("res type is ", res.header.mt)
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
        global FailureCount
        try:
            rMsg = Msg(self.sm.a_recvMsg())
            print("response from server")
            FailureCount = 0 # reset failure count
            return rMsg
        except Exception as e: # failed to get in time, so request again OR wrong checksum, so requesting again
            print(e)
            FailureCount += 1 # increase failure count by 1
            if(FailureCount >= config.AllowedFailureTotal): # if cannot get within failure count, then assume connection dead or failure to get
                FailureCount = 0 # reset failure count
                raise ConnectionError("Exceeded failure count, unable to request")
            return self.newReq(r, adr)

    def newReq(self, r:Req, adr:tuple) -> Msg:
        self.sm.a_sendMsg(r, adr)
        return self.waitRes(r, adr)

class Package: # package
    def __init__(self, msg, bfr_size):
        self.msg_Size = bfr_size - headerSize
        self.pt = getPackageNumber(bytes(msg, "utf-8"), self.msg_Size)
        self.list = splitPackage(bytes(msg, "utf-8"), self.msg_Size)

    def getPck(self):
        return self

    def getListItem(self, index) -> bytes:
        if(index > len(self.list)):
            raise ValueError("Package list slice request out if bounds")
        return self.list[index]

def a_input():
    Msg = str(input()) # guarantees input is returned in string format
    return Msg

def a_input_validation(input:str, checkList:str):
    values = checkList.split("\n")
    while(True):
        for i in values:
            if(input == i):
                return input
        print("\nInput not in possible items list. Please enter (exactly) one of the following:", checkList)
        input = a_input()

def getPackageNumber(package: bytes, actual_bfr_size:int) -> int:
    packageNumber:int = int(math.ceil(len(package) / actual_bfr_size))
    return packageNumber

def splitPackage(pck:bytes, actual_bfr_size:int) -> list:
    n:int = getPackageNumber(pck, actual_bfr_size)
    return [pck[x*actual_bfr_size:(x+1)*actual_bfr_size] for x in range(n)]

def calculateChks(byte_arr:bytes):
    lrc = 0
    for b in byte_arr:
        lrc = (lrc+b) & 0xFFFFFFFF
    return ((lrc ^ 0xFFFFFFFF) + 1) & 0xFFFFFFFF

def createPaths():
    if not os.path.exists(config.resourcesPath):
        os.makedirs(config.resourcesPath)
    if not os.path.exists(config.resourceFailurePath):
        os.makedirs(config.resourceFailurePath)
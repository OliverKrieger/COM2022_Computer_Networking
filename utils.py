import socket
import math
import os

from zmq import MSG_T_SIZE

from message import SocketMsg, Msg
from requests import Req, create_req, Types
from header import Header, headerSize
import config
from encryption_manager import EncryptionManager

FailureCount = 0

##############################
# Utilities across all files #
##############################

#####################################
#              Classes              #
#####################################
class Socket_Manager:
    def __init__(self, socket:socket.socket, bfr_size:int):
        self.socket = socket
        self.bfr_size = bfr_size
        self.req_manager = ReqManager(self)

    def a_recvMsg(self, em:EncryptionManager = None):
        res:SocketMsg = SocketMsg(self.socket.recvfrom(self.bfr_size))
        chks = calculateChks(res.msg[4:]) 
        print("socket message received, em is", em)
        if(config.ExtensionMode == True and em is not None):
            print("receiving bytes ", res.msg[config.headerSize:])
            res.msg = res.msg[0:config.headerSize] + em.decrypt_message(res.msg[config.headerSize:], em.PrivateKey)
        m = Msg(res)
        print("converted to message")
        #FOR WRONG RESPONSE TEST
        if(config.TestUnknownRequest == True):
            m.header.set_mt(-1) # this should never be possible
        #END TEST
        if(validate_response(m) == False):
            raise ValueError("ERROR - Unknown response type!", m.header.mt)
        if(m.header.mt == Types.error.value):
            raise ValueError("ERROR - Server responded with an error, unable to process package!")
        # chks = calculateChks(res.msg[4:]) # calculate checksum to anything but checksum itself
        hchks = int.from_bytes(res.msg[0:4], "little")
        if(hchks != chks):
            print("received chks", hchks, "and calc chks ", chks)
            raise ValueError("ERROR - package is corrupted, it has a wrong checksum.")
        return res
        # if(m.header.chks != chks):
        #     print("received chks", m.header.chks, "and calc chks ", chks)
        #     raise ValueError("ERROR - package is corrupted, it has a wrong checksum.")
        # return res

    def a_sendMsg(self, r: Req, address: tuple):
        print("*--------------------------------------------------------------*")
        print("new package to address ", address)
        print("*--------------------------------------------------------------*\n")
        chks = calculateChks(r.get_bytes()[4:]) # calculate checksum to anything but checksum itself
        print("calculated checksum ", chks)
        r.head.set_chks(chks)
        #FOR FAILURE TEST
        if(config.TestFileSaveOnError == True):
            if(r.head.si == 2):
                r.head.set_chks(0)
        #END TEST
        print("*^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^*")
        print("sending bytes ", r.get_bytes())
        print("*^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^*\n")
        self.socket.sendto(r.get_bytes(), address)

    def a_request_until_finished(self, head:Header, m:bytes, addr, em:EncryptionManager = None) -> bytes:
        total:bytes = m
        rqType:int = head.mt
        if(len(m) > 0):
            print("starting total ", m.decode("utf-8"))
        while(head.si != head.lsi):
            # ToDO if want to send multi packet messages, then MUST remake header (otherwise return always has greater last slice 
            # index, even though its supposed to be 0)
            try:
                print("Client requesting next package...")
                res:Msg = self.req_manager.newReq(create_req(head, bytes()), addr, em)
            except ConnectionError as e:
                print("Request Failure:", e)
                raise CustomConnectionError("failed to request file index", head.fi, total)
            print("res type is ", res.header.mt)
            print("received message\n ", res.message)
            print("*************************************\n")
            total += res.bytes
            head = res.header
            head.mt = rqType
            head.si = head.si + 1
            head.lsi = head.lsi + 1
        return total

    def get_socket_manager(self):
        return self

class ReqManager:
    def __init__(self, sm:Socket_Manager):
        self.sm = sm

    # Request - Response functionality
    def waitRes(self, r:Req, adr:tuple, em:EncryptionManager = None) -> Msg:
        global FailureCount
        try:
            rMsg = Msg(self.sm.a_recvMsg(em))
            print("response from server ", rMsg.address)
            FailureCount = 0 # reset failure count
            return rMsg
        except Exception as e: # failed to get in time, so request again OR wrong checksum, so requesting again
            print(e)
            FailureCount += 1 # increase failure count by 1
            if(FailureCount >= config.AllowedFailureTotal): # if cannot get within failure count, then assume connection dead or failure to get
                FailureCount = 0 # reset failure count
                raise ConnectionError("Exceeded failure count, unable to request")
            return self.newReq(r, adr, em)

    def newReq(self, r:Req, adr:tuple, em:EncryptionManager = None) -> Msg:
        self.sm.a_sendMsg(r, adr)
        return self.waitRes(r, adr, em)

class Package: # package
    def __init__(self, msg, bfr_size):
        self.msg_Size = bfr_size - headerSize
        print("slice size will be limited to ", self.msg_Size)
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
        lrc = (lrc+b) & 0xFF
    return ((lrc ^ 0xFF) + 1) & 0xFF

def createPaths():
    if not os.path.exists(config.resourcesPath):
        os.makedirs(config.resourcesPath)
    if not os.path.exists(config.resourceFailurePath):
        os.makedirs(config.resourceFailurePath)

class CustomConnectionError(Exception):
    def __init__(self, *args):
        if args:
            self.error = args[0]
            self.fi = args[1]
            self.bytes = args[2]
        
    def __str__(self):
        if self.error:
            return "Custom connection error, {0}".format(self.error)
        else:
            return "Custom connection error"

def validate_response(m:Msg):
    for item in Types:
        if(m.header.mt == item.value):
            return True
    return False
from enum import Enum

from rsa import encrypt

#################################
# Manages constructing requests #
#################################

from header import Header, headerSize
#########################################
# Message Types
#########################################
class Types(Enum):
    req= 1
    res= 2
    error= 8
    exKeys= 9
    encryptReq= 10

class Req:
    def __init__(self, r:bytes):
        h = Header()
        h.set_header_bytes(r[0:headerSize])
        self.head = h
        self.msg = r[headerSize:]

    def get_bytes(self) -> bytes:
        print("[******************************************************]")
        print("Request Header bytes ", self.head.get_header_bytes())
        print("Request Message bytes ", self.msg)
        print("[******************************************************]\n")
        return self.head.get_header_bytes() + self.msg

def create_req(h:Header, m:bytes) -> Req:
    return Req(h.get_header_bytes() + m)
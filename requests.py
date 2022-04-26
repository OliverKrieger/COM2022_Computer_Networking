from enum import Enum

from header import Header, headerSize
#########################################
# Message Types
#########################################
class Types(Enum):
    req= 1
    res= 2
    error= 8

class Req:
    def __init__(self, r:bytes):
        h = Header()
        h.set_header_bytes(r[0:headerSize])
        self.head = h
        self.msg = r[headerSize:]

    def get_bytes(self) -> bytes:
        return self.head.get_header_bytes() + self.msg

def create_req(h:Header, m:bytes) -> Req:
    return Req(h.get_header_bytes() + m)
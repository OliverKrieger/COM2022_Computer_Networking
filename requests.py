from enum import Enum

from header import Header
#########################################
# Message Types
#########################################
class Types(Enum):
    req= 1
    res= 2

class Req:
    def __init__(self, r:bytes):
        self.bytes = r

    def get_bytes(self) -> bytes:
        return self.bytes

def create_req(h:Header, m:bytes) -> Req:
    return Req(h.get_header_bytes() + m)
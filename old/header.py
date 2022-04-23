from enum import Enum
from constants import c_buffer, s_buffer

bufferSize = 32

# total size
headerSize = 8

r_size = 1
pn_size = 1
pt_size = 1
chks_size = 1

r_pos = r_size
pn_pos = r_size + pn_size
pt_pos = r_size + pn_size + pt_size
chks_pos = r_size + pn_size + pt_size + chks_size

#########################################
# Requests
#########################################
class Requests(Enum):
    handshake= 1
    res= 2
    fullyreceived= 22
    req= 3
    givelist= 31
    filereq = 32

class Req:
    def __init__(self, req):
        self.type = req[0:r_pos]
        self.pn = req[r_pos:pn_pos]
        self.pt = req[pn_pos:pt_pos]
        self.chks = req[pt_pos:chks_pos]
        self.message = req[headerSize:].decode()
        self.bytes = req[headerSize:]
    
    def getRecvMsg(self):
        return self



#########################################
# Funcions
#########################################
#def makeRequest(r: int, pck: int, m: str) -> str:
def makeRequest(l: list, m: bytes = bytes()) -> bytes: # r = request, m = message
    cnt = 1 # counter to find correct byte value
    r = 0 # request
    pn = 0 # package number
    pt = 0 # package total number
    chks = 0 # checksum
    for i in l:
        if(cnt == 1) : r = i
        if(cnt == 2) : pn = i
        if(cnt == 3) : pt = i
        if(cnt == 4) : chks = i
        cnt += 1

    if(int(r) > 255):
        raise ValueError('Request message is', r, ' but maximum allowed size is: ', 255)
    
    zeros = 0
    # bufferSize
    req = (r.to_bytes(1, 'little') 
    + pn.to_bytes(1, 'little') 
    + pt.to_bytes(1, 'little') 
    + chks.to_bytes(1, 'little') 
    + zeros.to_bytes(headerSize-4, 'little'))
    return req + m


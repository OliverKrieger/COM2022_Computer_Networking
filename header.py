from enum import Enum

bufferSize = 32

# total size
headerSize = 8

#########################################
# Requests
#########################################
# 1 = handshake - message contains buffer size
# 2 = response - message contains response
    # 21 = message response received
# 3 = request - message contains request value
    # 31 = givelist - gives a list of files user has

class Requests(Enum):
    handshake: 1
    res: 2
    responsereceived: 21
    req: 3
    givelist: 31


#########################################
# Funcions
#########################################
def makeRequest(r: int, m: str) -> str: # r = request, m = message
    if(int(r) > 255):
        raise ValueError('Request message is', r, ' but maximum allowed size is: ', 255)
    
    zeros = 0
    req = r.to_bytes(1, 'little') + zeros.to_bytes(headerSize-1, 'little')# bufferSize
    return req.decode('UTF-8') + str(m)
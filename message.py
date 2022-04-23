from header import headerSize, Header

#####################################
# Classes
#####################################
class SocketMsg:
    def __init__(self, s_msg:tuple):
        self.msg = s_msg[0]
        self.adr = s_msg[1]

    def get_msg(self):
        return self

class Msg:
    def __init__(self, s_msg:SocketMsg):
        h = Header()
        h.set_header_bytes(s_msg.msg[0:headerSize])
        self.header = h
        self.message = s_msg.msg[headerSize:].decode()
        self.bytes = s_msg.msg[headerSize:]
        self.address = s_msg.adr
        self.port = self.address[1]
    
    def get_msg(self):
        return self
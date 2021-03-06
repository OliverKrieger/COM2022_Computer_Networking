from enum import Enum

import config

#############################################
# The file in charge of creating the header #
#############################################


headerSize = config.headerSize

#####################################
# Classes
#####################################
class Header:
    def __init__(self):
        self.chks = 0
        self.mt = 0
        self.si = 0
        self.lsi = 0
        self.fi = 0
        self.bl = 0
        self.bytes = 0

    def set_header_bytes(self, head:bytes):
        self.chks = int.from_bytes(head[0:4], "little")
        self.mt = int.from_bytes(head[4:5], "little")
        self.si = int.from_bytes(head[5:9], "little")
        self.lsi = int.from_bytes(head[9:13], "little")
        self.fi = int.from_bytes(head[13:17], "little")
        self.bl = int.from_bytes(head[17:19], "little")
        self.bytes = head

    def set_chks(self, v:int):
        self.chks = v

    def set_mt(self, v:int):
        self.mt = v

    def set_si(self, v:int):
        self.si = v

    def set_lsi(self, v:int):
        self.lsi = v

    def set_fi(self, v:int):
        self.fi = v
    
    def set_bl(self, v:int):
        self.bl = v

    def get_header_bytes(self) -> bytes:
        h:bytes = (self.chks.to_bytes(4, 'little') 
        + self.mt.to_bytes(1, 'little') 
        + self.si.to_bytes(4, 'little') 
        + self.lsi.to_bytes(4, 'little')
        + self.fi.to_bytes(4, 'little') 
        + self.bl.to_bytes(2, 'little'))
        print("*/////////////////////////////////*")
        print("Header bytes: ", h)
        print("*/////////////////////////////////*")
        return h

    def print_header(self) -> None:
        print("header is:\nchks ", self.chks, "\nmt ", self.mt, "\nsi ", self.si, "\nlsi ", self.lsi, "\nfi ", self.fi, "\nbl ", self.bl)
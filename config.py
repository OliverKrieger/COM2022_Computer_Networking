from typing import Optional
import math

######################
# All configurations #
######################

headerSize = 19
base_bfr_size:int = 400

ExtensionMode = False # to run extensions
EncryptionBitSize:int = 512 # 512 is in bits
EncryptionAllowedBufSize:int = math.ceil(EncryptionBitSize/8) # bytes will be 512 / 8, meaning 64
EncryptionHeldBits:int = 11 # 11 bits are held by encryption
EncryptionAllowedMessageSize:int = EncryptionAllowedBufSize - EncryptionHeldBits # meaning we can only use 64 - 11 bits for message, so 53

c_bfr_size:int = base_bfr_size
s_bfr_size:int = base_bfr_size

resourcesPath = "./resources"
resourceFailurePath = "./failures"

localIP:str = "127.0.0.1"
sendIP:str = "127.0.0.1"
# MyIP
# localIP:str = "10.77.38.136"
# Liam
# sendIP:str = "10.77.100.203"
# Lorinc
# sendIP:str = "10.77.63.64"
ConnectionPort:Optional[int] = None # port we are sending to
ConnectionAddress = (sendIP, ConnectionPort)
BindPort:Optional[int] = None # also local port
BindAddress = (localIP, BindPort)

AllowedFailureTotal = 5 # number of times a request-response can fail before stopping communications

# Tests
TestFileSaveOnError = False # test if we only receive one packet and save it. Also tests that checksum validation works
TestUnknownRequest = False # test a request not known by types
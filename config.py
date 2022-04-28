from typing import Optional

base_bfr_size:int = 400
c_bfr_size:int = base_bfr_size
s_bfr_size:int = base_bfr_size

resourcesPath = "./resources"
resourceFailurePath = "./failures"

localIP:str = "127.0.0.1"
sendIP:str = "127.0.0.1"
# localIP:str = "10.77.38.136"
# sendIP:str = "10.77.100.203"
ConnectionPort:Optional[int] = None # port we are sending to
ConnectionAddress = (sendIP, ConnectionPort)
BindPort:Optional[int] = None # also local port
BindAddress = (localIP, BindPort)

AllowedFailureTotal = 5 # number of times a request-response can fail before stopping communications

ExtensionMode = False # to run extensions

# Tests
TestFileSaveOnError = False # test if we only receive one packet and save it. Also tests that checksum validation works
TestUnknownRequest = False # test a request not known by types
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
# sendIP:str = "10.77.47.75"
ConnectionPort:Optional[int] = None
ConnectionAddress = (sendIP, ConnectionPort)
BindPort:Optional[int] = None
BindAddress = (localIP, BindPort)

AllowedFailureTotal = 1

# Tests
TestFileSaveOnError = False # test if we only receive one packet and save it. Also tests that checksum validation works
base_bfr_size:int = 48
c_bfr_size:int = base_bfr_size
s_bfr_size:int = base_bfr_size

resourcesPath = "./resources"

localIP:str = "127.0.0.1"
sendIP:str = "127.0.0.1"
ConnectionPort:str = None
ConnectionAddress = (sendIP, ConnectionPort)
BindPort:str = None
BindAddress = (localIP, BindPort)
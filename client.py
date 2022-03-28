import socket


# msgFromClient       = "Hello UDP Server"
# bytesToSend         = str.encode(msgFromClient)
# serverAddressPort   = ("127.0.0.1", 13769)
# bufferSize          = 256

# UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPClientSocket.sendto(bytesToSend, serverAddressPort) 
# msgFromServer = UDPClientSocket.recvfrom(bufferSize)

# msg = "Message from Server {}".format(msgFromServer[0])
# print(msg)

def client_init():
    Port = int(input("Enter Connection Port: "))
    Dest = "127.0.0.1"
    ConnectionPort = (Dest, Port)
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    while(True):
        Msg = str(input())
        SendMsg = str.encode(Msg)
        UDPClientSocket.sendto(SendMsg, ConnectionPort)
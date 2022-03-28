import socket
import sys

def client_init():
    if(sys.argv[1]):
        ConnectionPort = int(sys.argv[1])
    else:
        ConnectionPort = int(input("Enter Connection Port: "))

    Dest = "127.0.0.1"
    ConnectionPort = (Dest, ConnectionPort)

    print("Client: ", ConnectionPort)

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    while(True):
        Msg = str(input())
        SendMsg = str.encode(Msg)
        UDPClientSocket.sendto(SendMsg, ConnectionPort)
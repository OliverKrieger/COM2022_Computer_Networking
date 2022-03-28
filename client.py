import socket
import sys

print ('Argument List:', str(sys.argv))

def client_init():
    if(sys.argv[1]):
        Port = int(sys.argv[1])
    else:
        Port = int(input("Enter Connection Port: "))
    Dest = "127.0.0.1"
    ConnectionPort = (Dest, Port)
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    while(True):
        Msg = str(input())
        SendMsg = str.encode(Msg)
        UDPClientSocket.sendto(SendMsg, ConnectionPort)
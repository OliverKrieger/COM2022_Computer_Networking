import socket
import sys

def client_init():
    if(sys.argv[1]):
        ConnectionPort = int(sys.argv[1])
    else:
        ConnectionPort = int(input("Enter Connection Port: "))

    Dest = "127.0.0.1"
    ConnectionPort = (Dest, ConnectionPort)
    bufferSize  = 256

    print("Client: ", ConnectionPort)

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    while(True):
        Msg = str(input())
        SendMsg = str.encode(Msg)
        UDPClientSocket.sendto(SendMsg, ConnectionPort)
        if(Msg == "givelist?"):
            RecvMsg = UDPClientSocket.recvfrom(bufferSize)
            message = RecvMsg[0].decode()
            address = RecvMsg[1]
            port = address[1]
            print(f"{port}: {message}")

            # rewrite this into a header msg about what you want
            # and function maybe
            print("which item would you like (enter filename exactly)")
            Msg = str(input())
            SendMsg = str.encode(Msg)
            UDPClientSocket.sendto(SendMsg, ConnectionPort)
            RecvMsg = UDPClientSocket.recvfrom(bufferSize)
            message = RecvMsg[0].decode()
            print(f"{port}: {message}")
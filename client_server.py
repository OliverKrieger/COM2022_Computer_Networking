import socket

ip = "127.0.0.1" # localhost
bufferSize  = 256

print("Enter your port")
local_port = int(input())

print("Enter port to connect to")
send_port = int(input())

# Create a datagram socket
UDPSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPSocket.bind((ip, local_port))
print("Client at ", ip, " connected on port ", str(local_port))

msg                 = "Message from ", ip, ":", local_port
bytesToSend         = str.encode(msg)
UDPSocket.sendto(bytesToSend, send_port)
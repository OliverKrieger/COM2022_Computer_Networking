from client import client_loop
import socket
import config

def client_init():
    print("client initalisation called...")

    # Who are we connecting to
    print("Client: ", config.ConnectionAddress)

    # Create Client Socket
    UDP_cs:socket.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_cs.settimeout(1)

    print("client initalisation finish.")
    client_loop(UDP_cs)

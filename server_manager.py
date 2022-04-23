from server import server_loop
import socket
import config

def server_init():
    print("server initalisation called...")

    # What port are we binding to
    print("Server: ", config.BindAddress)

    # Create server socket
    UDP_ss = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDP_ss.bind(config.BindAddress)

    print("server initalisation finish.")
    server_loop(UDP_ss)
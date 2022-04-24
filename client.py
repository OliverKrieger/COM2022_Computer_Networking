import socket
from typing import * 

from utils import a_input, Socket_Manager
import config
import client_handlers

UDP_cs:Optional[socket.socket] = None
C_S_Manager:Optional[Socket_Manager] = None

def client_loop(socket:socket.socket):
    global UDP_cs
    global C_S_Manager

    UDP_cs = socket
    C_S_Manager = Socket_Manager(UDP_cs, config.s_bfr_size)

    print("Start client loop...")

    while(True):
        input:str = a_input()
        print("\n")
        if(input != "exit"):
            c_handle(input)
        else:
            break

    print("finished client loop...")

def c_handle(input:str):
    if(C_S_Manager is not None):
        if(input == "list"):
            client_handlers.handle_resource_listing(C_S_Manager)
        elif(input == "get"):
            client_handlers.handle_get_resource(C_S_Manager)
        else:
            print("Sorry, did not understand input\n")
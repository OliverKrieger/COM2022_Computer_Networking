# Python imports
import socket

# Application imports
from utils import Socket_Manager
import config
from message import Msg
import server_handlers

# global variables
UDP_ss:socket.socket = None
S_S_Manager:Socket_Manager = None

def server_loop(socket:socket.socket):
    global UDP_ss
    global S_S_Manager

    UDP_ss = socket
    S_S_Manager = Socket_Manager(UDP_ss, config.c_bfr_size)

    print("Start server loop...")

    while(True):
        s_handle(Msg(S_S_Manager.a_recvMsg()))

def s_handle(msg:Msg):
    if(msg.header.fi == 0):
        server_handlers.handle_file_request(S_S_Manager, msg)
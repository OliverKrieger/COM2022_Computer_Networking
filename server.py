# Python imports
import socket
from typing import *

# Application imports
from utils import Socket_Manager
import config
from message import Msg
import server_handlers
import requests

# global variables
UDP_ss:Optional[socket.socket] = None
S_S_Manager:Optional[Socket_Manager] = None

def server_loop(socket:socket.socket):
    global UDP_ss
    global S_S_Manager

    UDP_ss = socket
    S_S_Manager = Socket_Manager(UDP_ss, config.c_bfr_size)

    print("Start server loop...")
    
    while(True):
        try:
            s_handle(Msg(S_S_Manager.a_recvMsg()))
        except ValueError as e:
            print(e)


def s_handle(msg:Msg):
    print("New message received from ", msg.address)
    if(S_S_Manager is not None):
        if(msg.header.fi == 0 and (msg.header.mt == requests.Types.req.value or msg.header.mt == requests.Types.encryptReq.value) and msg.header.si > 0):
            server_handlers.handle_resources_request(S_S_Manager, msg)
        elif(msg.header.fi != 0 and (msg.header.mt == requests.Types.req.value or msg.header.mt == requests.Types.encryptReq.value) and msg.header.si > 0):
            server_handlers.handle_resource_index_request(S_S_Manager, msg)
        elif(msg.header.mt == requests.Types.exKeys.value):
            server_handlers.handle_key_exchange(S_S_Manager, msg)
        else:
            print("message arrived, but of unknown request type. Request index was ", msg.header.mt)

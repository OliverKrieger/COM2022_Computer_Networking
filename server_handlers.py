from os import listdir

from utils import Package, Socket_Manager
from header import Header
from requests import Req, Types, create_req
from message import Msg
import config

def handle_file_request(S_S_Manager:Socket_Manager, msg:Msg):
    print("File list request received")
    pck:Package = create_resource_list()
    head = Header()
    head.set_mt(Types.res.value)
    head.set_si(msg.header.si)
    head.set_fi(msg.header.fi)
    head.set_lsi(len(pck.list))
    req:Req = create_req(head, pck.getListItem(msg.header.si - 1))
    S_S_Manager.a_sendMsg(req.bytes, msg.address)

def create_resource_list() -> Package:
    list = listdir(config.resourcesPath)
    sendList:str = "\n" + '\n'.join(list)
    return Package(sendList, config.c_bfr_size)
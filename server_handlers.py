from os import listdir

from utils import Package, Socket_Manager
from header import Header
from requests import Req, Types, create_req
from message import Msg
import config
from file_manager import FileManager

fm:FileManager = FileManager()

def handle_resources_request(S_S_Manager:Socket_Manager, msg:Msg):
    print("File list request received")
    pck:Package = create_resource_list(fm.files_as_str)
    respond_slice(S_S_Manager, msg, pck)

def handle_resource_index_request(S_S_Manager:Socket_Manager, msg:Msg):
    print("Requesting resource number ", msg.header.fi, "for slice ", msg.header.si)
    pck:Package = fm.get_resource_as_pck(msg.header.fi-1, config.c_bfr_size)
    respond_slice(S_S_Manager, msg, pck)

def respond_slice(S_S_Manager:Socket_Manager, msg:Msg, pck:Package):
    head = Header()
    head.set_mt(Types.res.value)
    head.set_si(msg.header.si)
    head.set_fi(msg.header.fi)
    head.set_lsi(len(pck.list))
    req:Req = create_req(head, pck.getListItem(msg.header.si - 1))
    S_S_Manager.a_sendMsg(req.bytes, msg.address)

def create_resource_list(fl_list:str) -> Package:
    return Package(fl_list, config.c_bfr_size)
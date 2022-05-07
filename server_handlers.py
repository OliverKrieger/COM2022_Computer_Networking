from base64 import encode
from os import listdir

from utils import Package, Socket_Manager
from header import Header
from requests import Req, Types, create_req
from message import Msg
import config
from file_manager import FileManager
from encryption_manager import EncryptionManager

fm:FileManager = FileManager()
em:EncryptionManager = EncryptionManager()

def handle_resources_request(S_S_Manager:Socket_Manager, msg:Msg):
    print("File list request received, requesting file, ", msg.header.fi, "with slice ", msg.header.si)
    pck:Package = create_resource_list(fm.files_as_str)
    try:
        respond_slice(S_S_Manager, msg, pck)
    except Exception as e:
        print(e)
        return

def handle_resource_index_request(S_S_Manager:Socket_Manager, msg:Msg):
    print("Requesting resource number ", msg.header.fi, "for slice ", msg.header.si)
    try:
        pck:Package = fm.get_resource_as_pck(msg.header.fi-1, config.c_bfr_size)
        if(config.ExtensionMode == True):
            pck = fm.get_resource_as_pck(msg.header.fi-1, config.EncryptionAllowedMessageSize)
        respond_slice(S_S_Manager, msg, pck)
    except ValueError as e:
        print(e)
        error:str = "Requested slice " + str(msg.header.si) + " was out of bounds for resource index" + str(msg.header.fi)
        respond_error(S_S_Manager, error, msg.address)
    
def respond_slice(S_S_Manager:Socket_Manager, msg:Msg, pck:Package):
    head = Header()
    head.set_mt(Types.res.value)
    head.set_si(msg.header.si)
    head.set_fi(msg.header.fi)
    head.set_lsi(len(pck.list))
    p:bytes = pck.getListItem(msg.header.si - 1)
    head.set_bl(len(p))
    if(config.ExtensionMode == True and em is not None):
        print("Responding slice length ", len(p))
        p = em.encrypt_message(p, em.ConnectionFromClientKey)
        print("slice size after encryption", len(p))
        print("encrypted message ", p)
    r:Req = create_req(head, p)
    print("Server sending...")
    S_S_Manager.a_sendMsg(r, msg.address)
    

def create_resource_list(fl_list:str) -> Package:
    if(config.ExtensionMode == True):
        print("Allowed message size is ", config.EncryptionAllowedMessageSize)
        return Package(fl_list, config.EncryptionAllowedMessageSize)
    return Package(fl_list, config.c_bfr_size)

def respond_error(S_S_Manager:Socket_Manager, error:str, addr):
    head = Header()
    head.set_mt(Types.error.value)
    b:bytes = error.encode("utf-8")
    r:Req = create_req(head, b)
    S_S_Manager.a_sendMsg(r, addr)

def handle_key_exchange(S_S_Manager:Socket_Manager, msg:Msg):
    global em
    print("Server received key exchange request")
    if(config.ExtensionMode == True and em is not None):
        em.set_cck(msg.bytes)
        head = Header()
        head.set_mt(Types.res.value)
        r:Req = create_req(head, em.export_public_key())
        print("Server responding to key exchange request...")
        S_S_Manager.a_sendMsg(r, msg.address)


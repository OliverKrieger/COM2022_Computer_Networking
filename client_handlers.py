import requests
from utils import Socket_Manager, a_input
from message import Msg
from requests import Req, create_req
from header import Header
import config

def handle_resource_listing(s_manager:Socket_Manager) -> None:
    print("Requesting resource list...")
    msg = request_index(s_manager, 0)
    print("Resource list from server:\n", msg.decode("utf-8"))

def handle_get_resource(s_manager:Socket_Manager) -> None:
    print("Enter file index you would like to request: ")
    input:int = int(a_input())
    # ToDo stop being able to request file index 0!

    print("Requesting file index ", input)
    msg = request_index(s_manager, input)
    print("File Value:\n", msg.decode("utf-8"))

def request_index(s_manager:Socket_Manager, index:int) -> bytes:
    head = Header()
    head.set_mt(requests.Types.req.value)
    head.set_si(1)
    head.set_fi(index) 
    return s_manager.a_request_until_finished(head, bytes(), config.ConnectionAddress)
import requests
from utils import Socket_Manager
from message import Msg
from requests import Req, create_req
from header import Header
import config

def handle_resource_listing(s_manager:Socket_Manager) -> None:
    print("Requesting resource list...")
    head = Header()
    head.set_mt(requests.Types.req.value)
    head.set_si(1)
    head.set_fi(0) 
    msg = s_manager.a_request_until_finished(head, bytes(), config.ConnectionAddress)
    print("Resource list from server:\n", msg.decode("utf-8"))
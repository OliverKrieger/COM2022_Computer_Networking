from typing import *

import requests
from utils import Socket_Manager, a_input
from message import Msg
from requests import Req, create_req
from header import Header
import config
from validation import ValidationManager

validation_manager:Optional[ValidationManager] = None

def handle_resource_listing(s_manager:Socket_Manager) -> None:
    print("Requesting resource list...")
    try:
        msg = request_index(s_manager, 0)
        print("Resource list from server:\n", msg.decode("utf-8"))
    except ConnectionError as e:
        print(e)
        return

def handle_get_resource(s_manager:Socket_Manager) -> None:
    try:
        validate_validation_manager(s_manager)

        print("Enter file index you would like to request: ")
        input = a_input()
    
        while(True):
            global validation_manager
            if(validation_manager is not None):
                b = validation_manager.validate_file_index_input(input)
                if(b == True):
                    break
                else:
                    print("Sorry, this is not a valid input!")
                    input = a_input()

        in_val = int(input) # validated as an integer so can be converted
        print("Requesting file index ", in_val)
    
        msg = request_index(s_manager, in_val)
        print("should fail")
        print("File Value:\n", msg.decode("utf-8"))
    except ConnectionError as e:
        print(e)
        return

def request_index(s_manager:Socket_Manager, index:int) -> bytes:
    head = Header()
    head.set_mt(requests.Types.req.value)
    head.set_si(1)
    head.set_fi(index) 
    try:
        return s_manager.a_request_until_finished(head, bytes(), config.ConnectionAddress)
    except ConnectionError as e:
        print("request index", e)
        raise ConnectionError(e)

def validate_validation_manager(s_manager:Socket_Manager) -> None:
    global validation_manager
    if(validation_manager == None):
        try:
            msg:bytes = request_index(s_manager, 0)
            validation_manager = ValidationManager(msg.decode("utf-8"))
        except ConnectionError as e:
            print("validation manager ", e)
            raise ConnectionError(e)
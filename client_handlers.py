from typing import *

import requests
from utils import Socket_Manager, a_input
from header import Header
import config
from validation import ValidationManager
from file_manager import FailureFile

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
        print("File Value:\n", msg.decode("utf-8"))
    except ConnectionError as e:
        print(e)
        #ToDo save the remaining fail message chunk here, because have access to validation manager!
        print("Saving current retrieved message")
        val = str(e).split(":")
        print("split value ", val)
        if(len(val) == 3):
            if(validation_manager is not None):
                validation_manager.saveFileFailure(int(val[1]), val[2])
        return

def handle_re_request(s_manager:Socket_Manager):
    validate_validation_manager(s_manager)
    if(validation_manager is not None):
        ffl:List[FailureFile] = validation_manager.getFailureList()
        if(len(ffl) > 0):
            for i in ffl:
                print("[", i.index, "]", i.name, "failed on slice ", i.slice_failed_on)
        else:
            print("No files to re-request!")

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
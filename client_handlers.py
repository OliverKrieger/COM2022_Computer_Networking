from typing import *
import os

import requests
from utils import Socket_Manager, a_input, CustomConnectionError
from header import Header
import config
from validation import ValidationManager
from file_manager import File, FailureFile

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
                fl:List[File] = validation_manager.valid_file_list
                indexList:List[int] = []
                for file in fl:
                    indexList.append(file.index)
                b = validation_manager.validate_file_index_input(input, indexList)
                if(b == True):
                    break
                else:
                    print("Sorry, this is not a valid input!")
                    input = a_input()

        in_val = int(input) # validated as an integer so can be converted
        print("Requesting file index ", in_val)
    
        msg = request_index(s_manager, in_val)
        print("File Value:\n", msg.decode("utf-8"))
    except CustomConnectionError as e:
        print(e)
        saveOnFailure(e)
        return

def handle_re_request_check(s_manager:Socket_Manager):
    try:
        validate_validation_manager(s_manager)
        if(validation_manager is not None):
            ffl:List[FailureFile] = validation_manager.getFailureList()
            if(len(ffl) > 0):
                handle_re_request(s_manager, ffl)
            else:
                print("No files to re-request!")
    except ConnectionError as e:
        print(e)
        return

def handle_re_request(s_manager:Socket_Manager, ffl:List[FailureFile]):
    for i in ffl:
        print("[", i.index, "]", i.name, "failed on slice ", i.slice_failed_on)
    print("Which file would you like to re-request?")
    input = a_input()
    while(True):
        global validation_manager
        if(validation_manager is not None):
            indexList:List[int] = []
            for f in ffl:
                indexList.append(f.index)
            b = validation_manager.validate_file_index_input(input, indexList)
            if(b == True):
                break
            else:
                print("Sorry, this is not a valid input!")
                input = a_input()
                if(input == "exit"):
                    return

    try:
        in_val = int(input) # validated as an integer so can be converted
        try:
            failurefile:FailureFile = validation_manager.find_valid_failure_file(in_val)
            file:File = validation_manager.find_valid_file_by_name(failurefile.name)
        except FileNotFoundError as e:
            print(e)
            return
        print("Re-Requesting file index ", file.index, " with slice ", failurefile.slice_failed_on)

        msg = request_index(s_manager, file.index, failurefile.slice_failed_on, failurefile.contents)
        print("File Value:\n", msg.decode("utf-8"))
        # if re-requested successfully, delete the failure
        fp:str = config.resourceFailurePath + "/" + failurefile.name
        os.remove(fp)
    except CustomConnectionError as e:
        print(e)
        saveOnFailure(e)
        return



def request_index(s_manager:Socket_Manager, file_index:int, slice_index:int = 1, msg_start_total = bytes()) -> bytes:
    print("Request for resource ", file_index, " with start slice index ", slice_index)
    head = Header()
    head.set_mt(requests.Types.req.value)
    head.set_si(slice_index)
    head.set_fi(file_index) 
    try:
        return s_manager.a_request_until_finished(head, msg_start_total, config.ConnectionAddress)
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

def saveOnFailure(e:CustomConnectionError):
    print("Saving current retrieved message")
    if(validation_manager is not None):
        validation_manager.saveFileFailure(int(e.fi), e.bytes)
    else:
        print("unable to save fail failure!")


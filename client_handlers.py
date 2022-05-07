from typing import *
import os

from message import Msg
import requests
from utils import Socket_Manager, a_input, CustomConnectionError
from header import Header
import config
from validation import ValidationManager
from file_manager import File, FailureFile
from encryption_manager import *

validation_manager:Optional[ValidationManager] = None
em:Optional[EncryptionManager] = EncryptionManager()

def handle_resource_listing(s_manager:Socket_Manager) -> None:
    print("Requesting resource list...")
    try:
        msg = request_index(s_manager, 0)
        print("Resource list from server:\n", msg.decode("utf-8"))
    except ConnectionError as e:
        print(e)
        return

# get a resource from a server
def handle_get_resource(s_manager:Socket_Manager) -> None:
    try:
        handle_encrypt_exchange_keys(s_manager) # lazy request
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
        print("*************************************")
        print("Requesting file index ", in_val)
    
        msg = request_index(s_manager, in_val)
        print("Client Received All:\n", msg.decode("utf-8"))
    except CustomConnectionError as e:
        print(e)
        saveOnFailure(e)
        return

# make sure re-request files exist
def handle_re_request_check(s_manager:Socket_Manager):
    try:
        handle_encrypt_exchange_keys(s_manager) # lazy request
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

# re-request already requested resource
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
        print("Client Received All:\n", msg.decode("utf-8"))
        # if re-requested successfully, delete the failure
        fp:str = config.resourceFailurePath + "/" + failurefile.name
        os.remove(fp)
    except CustomConnectionError as e:
        print(e)
        saveOnFailure(e)
        return

# request a file with an index from a server
def request_index(s_manager:Socket_Manager, file_index:int, slice_index:int = 1, msg_start_total = bytes()) -> bytes:
    print("Request for resource ", file_index, " with start slice index ", slice_index)
    head = Header()
    head.set_mt(requests.Types.req.value)
    if(config.ExtensionMode == True and em is not None): # Specifically if we are in extension mode that does encryption!
        head.set_mt(requests.Types.encryptReq.value)
    head.set_si(slice_index)
    head.set_fi(file_index) 
    try:
        if(config.ExtensionMode == True and em is not None):
            print("request with encryption")
            print("Client starting to request all...")
            return s_manager.a_request_until_finished(head, msg_start_total, config.ConnectionAddress, em)
        return s_manager.a_request_until_finished(head, msg_start_total, config.ConnectionAddress)
    except ConnectionError as e:
        print("request index", e)
        raise ConnectionError(e)

# make sure we have validation manager
def validate_validation_manager(s_manager:Socket_Manager) -> None:
    global validation_manager
    if(validation_manager == None):
        try:
            msg:bytes = request_index(s_manager, 0)
            validation_manager = ValidationManager(msg.decode("utf-8"))
        except ConnectionError as e:
            print("validation manager ", e)
            raise ConnectionError(e)

# if we failed to get full package, save file failure
def saveOnFailure(e:CustomConnectionError):
    print("Saving current retrieved message")
    if(validation_manager is not None):
        validation_manager.saveFileFailure(int(e.fi), e.bytes)
    else:
        print("unable to save fail failure!")

# if we are trying encryption, handles key exchange
def handle_encrypt_exchange_keys(s_manager:Socket_Manager):
    global em
    if(config.ExtensionMode == True and em is not None and em.ConnectionFromServerKey == None):
        print("client requesting key exchange...")
        head = Header()
        head.set_mt(requests.Types.exKeys.value)
        print("exported public key size ", len(em.export_public_key()))
        msg:Msg = s_manager.req_manager.newReq(requests.create_req(head, em.export_public_key()), config.ConnectionAddress)
        print("client received key exchange response")
        em.set_sck(msg.bytes)
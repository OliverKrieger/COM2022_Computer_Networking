from asyncio import FastChildWatcher
from typing import *

from file_manager import File, FailureFile
import config
import os
from utils import getPackageNumber
from header import headerSize
from message import Msg
from requests import Types

#####################################
#              Classes              #
#####################################
class ValidationManager:
    def __init__(self, s:str):
        self.valid_file_list = self.split_into_list(s)

    def split_into_list(self, s:str) -> List[File]:
        s_l = s.split("\n") # split into a single list
        f_l:List[File] = []
        for sl in s_l:
            v = sl.split(":") # split single list into values
            if(len(v) == 3): # make sure we have all values, if more than 2, too many, if less than 2, too few
                print("split list is ", v)
                f_l.append(File(int(v[0]), int(v[1]), v[2]))
        return f_l

    def get_valid_file_list(self):
        return self.valid_file_list

    def validate_file_index_input(self, input:str, index_list:List[int]) -> bool:
        try:
            in_val = int(input)
            print("input is ", in_val)
            for i in index_list:
                print("is  ", i, "equal to", in_val)
                if(i == in_val):
                    print("is equal")
                    return True
            print("no values match")
            return False
        except ValueError as e:
            print(e)
            return False

    def find_valid_file(self, file_index:int):
        for i in self.valid_file_list:
            if(i.index == file_index):
                return i
        raise FileNotFoundError("Could not find file with index ", file_index)

    def find_valid_file_by_name(self, file_name:str):
        for i in self.valid_file_list:
            if(i.name == file_name):
                return i
        raise FileNotFoundError("Could not find file with name ", file_name)

    def find_valid_failure_file(self, file_index:int):
        ffl:List[FailureFile] = self.getFailureList()
        for i in ffl:
            if(i.index == file_index):
                return i
        raise FileNotFoundError("Could not find file with index ", file_index)

    def saveFileFailure(self, fi:int, msg:bytes) -> None:
        try:
            fl:File = self.find_valid_file(fi)
        except FileNotFoundError as e:
            print("failed to find file: ", e)
            return
        if(len(msg) == 0):
            print("nothing to save, as nothing was received!")
            return
        fl_path = config.resourceFailurePath + "/" + fl.name
        print("File path is: ", fl_path)
        with open(fl_path, "wb") as f:
            f.write(msg)

    def getFailureList(self) -> List[FailureFile]:
        l:List = os.listdir(config.resourceFailurePath)
        ffl:List[FailureFile] = []
        cnt = 0
        act_bfr_size = config.c_bfr_size - headerSize
        for i in l:
            fp:str = config.resourceFailurePath + "/" + i 
            s = open(fp, "r").read()
            print("current saved size", len(s))
            si = getPackageNumber(s.encode(), act_bfr_size) + 1 # slice index we stopped on, as will msg total will be current read msg. +1 for the next slice
            ffl.append(FailureFile(cnt,i,si,s.encode()))
        return ffl
import os
from typing import *

from utils import Package
import config

#####################################
# Classes
#####################################
class File:
    def __init__(self, i:int, s:int, n:str):
        self.index = i
        self.size = s
        self.name = n
        
class FileManager:
    def __init__(self):
        self.file_list = self.get_resources()
        self.files_as_str = self.list_as_str(self.file_list)

    def get_resources(self) -> List[File]:
        l:list = os.listdir(config.resourcesPath)
        fl:List[File] = list()
        cnt = 1
        for i in l:
            fp:str = config.resourcesPath + "/" + i #filepath
            fl.append(File(cnt,os.path.getsize(fp),i))
            cnt += 1
        print(fl)
        return fl

    def list_as_str(self, fl:List[File]) -> str:
        fl_str:str = ""
        i:File
        for i in fl:
            fl_str += str(i.index) + ":" + str(i.size) + ":" + str(i.name) + "\n"
        print(fl_str)
        return fl_str

    def get_resource_as_pck(self, res_index:int, bfr_size:int):
        f = readFile(config.resourcesPath + "/" + self.file_list[res_index].name)
        return Package(f, bfr_size)

    def get_fm(self):
        return self



def readFile(path:str) -> str:
    return open(path, "r").read()
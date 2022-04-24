import os
from typing import *

import config

#####################################
# Classes
#####################################
class FileManager:
    def __init__(self):
        self.file_list = self.get_resources()
        self.files_as_str = self.list_as_str(self.file_list)

    def get_resources(self) -> list:
        l:list = os.listdir(config.resourcesPath)
        fl:List[File] = list()
        cnt = 1
        for i in l:
            fp:str = config.resourcesPath + "/" + i #filepath
            fl.append(File(cnt,os.path.getsize(fp),i))
            cnt += 1
        print(fl)
        return fl

    def list_as_str(self, fl:list) -> str:
        fl_str:str = "\n"
        i:File
        for i in fl:
            fl_str += str(i.index) + ":" + str(i.size) + ":" + str(i.name) + "\n"
        print(fl_str)
        return fl_str

    def get_fm(self):
        return self

class File:
    def __init__(self, i:int, s:int, n:str):
        self.index = i
        self.size = s
        self.name = n
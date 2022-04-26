from typing import *

from file_manager import File

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

    def validate_file_index_input(self, input:str) -> bool:
        try:
            in_val = int(input)
            print("input is ", in_val)
            for i in self.valid_file_list:
                print("is  ", i.index, "equal to", in_val)
                if(i.index == in_val):
                    print("is equal")
                    return True
            print("no values match")
            return False
        except ValueError as e:
            print(e)
            return False
        
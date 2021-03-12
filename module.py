from component import *
from config import *
import os

class BaseModule:
    module_id = 0
    def __init__(self, id = 0):
        self.module_id = id
        self.name = "Base Module"
    def init(self):
        pass

    def propagate(self):
        pass

    def update(self):
        pass

    def connect(self, dependency):
        pass

    def getName(self):
        return self.name

    def getId(self):
        return self.module_id

    # For debugging, show all register values and names
    def showRegs(self):
        print("---" + self.getName() + "---")
        vv = list(vars(self).values())
        for i in vv:
            if type(i) is type(Register()):
                print(i)

    # For debugging, show all shared wires values and names
    def showSharedWires(self):
        print("---" + self.getName() + "---")
        vv = list(vars(self).values())
        for i in vv:
            if type(i) is type(Wire()):
                if i.shared == True:
                    print(i)

    # For debugging, show all wires values and names
    def showWires(self):
        print("---" + self.getName() + "---")
        vv = list(vars(self).values())
        for i in vv:
            if type(i) is type(Wire()):
                print(i)

    def __str__(self):
        return "[Module: " + str(self.getName()) + "; id = "+ str(self.getId()) +"]"


class NzeroFetch(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Non-Zero Fetch"


        self.ptr_odd_addr = Wire(shared=False,width=NUM_PE,name="ptr_odd_addr",value=4)
        self.ptr_even_addr = Wire(shared=False,width=NUM_PE,name="ptr_even_addr",value=3)
        self.index_flag = Wire(shared=False,width=NUM_PE,name="index_flag",value=2)
        self.empty = Wire(shared=False,width=NUM_PE,name="empty",value=1)
        self.value_output = Wire(shared=False,width=NUM_PE,name="value_output",value=22)




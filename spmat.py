from module import BaseModule
from component import *
from config import *
import os

class SpMatRead(BaseModule):
    def __init__(self, filename: str, value: int):
        self.unit_line = SPMAT_unit_line
        self.num_lines = SPMAT_num_lines
        self.index_bits = SPMAT_index_bits
        self.weight_bits = SPMAT_weight_bits

        super().__init__(value)
        self.name = "Sparse Matrix Read"
        # Registers
        self.patch_complete = Register(name="patch_complete", value=1)
        self.memory_shift = Register(name="memory_shift",value=0)
        self.memory_addr = Register(name="memory_addr",value=0)
        self.read_enable = Register(name="read_enable",value=0)
        self.value = Register(name="value",value=0)
        self.valid = Register(name="valid",value=0)

        # Wires
        self.index = Wire(name="index")
        self.code = Wire(name="code")
        self.valid_w = Wire(name="valid_w")
        self.value_w = Wire(name="value_w")
        self.patch_complete_w = Wire(name="patch_complete_w")
        self.data_read = Wire(width=SPMAT_unit_line*2, name="data_read",value=0)

        # Shared Wired
        self.patch_complete_D = None
        self.memory_shift_D = None
        self.memory_addr_D = None
        self.read_enable_D = None
        self.valid_D = None
        self.value_D = None

        # Memory
        self.WImem = Memory("WImem", PTRVEC_num_lines)

        if os.path.isfile(filename):
            with open(filename,'r') as f:
                values = f.read().splitlines()
                for i in range(0, len(values)):
                    self.WImem.data[i] = int(values[i])

                for i in range(0, 2*self.unit_line):
                    self.data_read.data[i] = self.WImem.data[i]
        
        # Others
        self.read_times = 0

    def connect(self, dependency):
        if dependency.getName() == "Pointer Read Unit" and dependency.getId() == self.getId():
            self.patch_complete_D = dependency.patch_complete
            dependency.patch_complete.shared = True
            self.memory_shift_D = dependency.memory_shift
            dependency.memory_shift.shared = True
            self.memory_addr_D = dependency.memory_addr
            dependency.memory_addr.shared = True
            self.read_enable_D = dependency.read_spmat
            dependency.read_spmat.shared = True
            self.valid_D = dependency.valid
            dependency.valid.shared = True
            self.value_D = dependency.value_w
            dependency.value_w.shared = True
        else:
            print("Error: Connection Error")
    

    def update(self):
        if self.valid_D != None:
            self.patch_complete = self.patch_complete_D
            self.memory_shift = self.memory_addr_D
            self.memory_addr = self.memory_addr_D
            self.value = self.value_D
        
        self.read_enable = self.read_enable_D
        self.valid = self.valid_D


    def propagate(self):
        
        # Memory access
        if self.read_enable.data != 0:
            for i in range(0, 2*self.unit_line):
                self.data_read.data[i] = self.WImem.data[i + self.memory_addr.data * (self.unit_line * 2)]
            self.read_times += 1
        
        self.code = self.data_read.data[self.memory_shift.data * 2]
        self.index = self.data_read.data[self.memory_shift.data * 2 + 1]

        self.value_w = self.value
        self.valid_w = self.valid
        self.patch_complete_w = self.patch_complete
        
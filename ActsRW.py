from module import BaseModule
from component import *
from config import *
import os
from enum import Enum
class InterState(Enum):
    Activations_k = 0,
    Bias1_k = 1,
    Empty_k = 2

class ActsRW(BaseModule):
    def __init__(self,filename):
        super().__init__()
        self.name = "Activation Read/Write"

        self.reg_addr_w = Wire(name="reg_addr_w")
        self.acts_per_bank_D = Wire(width=NUM_PE,name="acts_per_bank_D")

        # To Nonzero fetch Registers
        self.read_addr_reg = Register("read_addr_reg")
        self.end_addr_reg = Register(name="end_addr_reg")
        self.which = Register(name="which")
        self.internal_state = Register(name="internal_state")
        self.has_bias = Register(name='has_bias')

        # Wire
        self.reg_addr_w = Wire(name="reg_addr_w")
        self.read_addr_reg_D = Wire(name="read_addr_reg_D")
        self.internal_state_D = Wire(name="internal_state_D")
        self.acts_per_bank = Wire(width=NUM_PE,name="acts_per_bank")

        # Shared Wire
        self.next_reg_addr = None



        # To Arithmetic module
        self.read_addr_arithm = Register(width=NUM_PE,name="read_addr_arithm")
        self.write_addr_arithm = Register(width=NUM_PE,name="write_addr_arithm")
        self.write_data_arithm = Register(width=NUM_PE,name="write_data_arithm")
        self.write_enable = Register(width=NUM_PE,name="write_enable")

        # Wire
        self.read_data_arithm = Wire(width=NUM_PE,name="read_data_arithm")
        self.write_complete = Wire(name="write_complete")
        self.layer_complete = Wire(name="layer_complete")

        # SharedWire
        self.read_addr_arithm_D = Wire(shared=True,width=NUM_PE,name="read_addr_arithm_D")
        self.write_addr_arithm_D = Wire(shared=True,width=NUM_PE,name="write_addr_arithm_D")
        self.write_data_arithm_D = Wire(shared=True,width=NUM_PE,name="write_data_arithm_D")
        self.write_enable_D = Wire(shared=True,width=NUM_PE,name="write_enable_D")



        self.bank_size = (ACTRW_maxcapacity - 1) / NUM_PE + 1
        self.memory_size = self.bank_size * NUM_PE

        self.ACTmem = [Memory("ACTmem0", self.memory_size),Memory("ACTmem1", self.memory_size)]

        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                values = f.read().splitlines()
                for i in range(0, len(values)):
                    self.ACTmem[self.which.data] = int(values[i])


    def set_state(self, input_size_t, which_t, bias_t):
        self.which.data = which_t
        self.has_bias.data = bias_t
        if input_size_t > ACTRW_maxcapacity:
            print("Error: End address exceeds memory capacity")

        self.end_addr_reg.data = (input_size_t - 1) / NUM_PE

    def connect(self, dependency):
        if dependency.getName() == "Non-Zero Fetch":
            self.next_reg_addr.data = dependency.next_reg_addr.data
        elif dependency.getName() == "Arithm Unit":
            self.read_addr_arithm_D.data[dependency.getId()] = dependency.read_addr.data
            self.write_addr_arithm_D.data[dependency.getId()] = dependency.write_addr.data
            self.write_data_arithm_D.data[dependency.getId()] = dependency.write_data.data
            self.write_enable_D.data[dependency.getId()] = dependency.write_enable.data
        else:
            print("Error: Unknown module type!")

    def propagate(self):
        nzf_id = self.which.data
        arithm_id = 1 - self.which.data

        if self.internal_state.data == InterState.Activations_k:
            for i in range(NUM_PE):
                self.acts_per_bank.data[i] = self.ACTmem[nzf_id].data[self.read_addr_reg.data * NUM_PE + i]

                self.reg_addr_w.data = self.read_addr_reg.data
                self.read_addr_reg_D.data = self.read_addr_reg.data + 1

                next_state = 0
                if self.has_bias.data == 1:
                    next_state = InterState.Bias1_k
                else:
                    next_state = InterState.Empty_k

                if self.read_addr_reg.data == self.end_addr_reg.data:
                    self.internal_state_D.data = next_state
                else:
                    self.internal_state_D.data = InterState.Activations_k
        elif self.internal_state.data == InterState.Bias1_k:
            for i in range(NUM_PE):
                self.acts_per_bank.data[i] = 0

            self.acts_per_bank.data[0] = 1
            self.reg_addr_w.data = self.end_addr_reg.data + 1
            self.read_addr_reg_D.data = 0
            self.internal_state_D.data = InterState.Empty_k

        elif self.internal_state.data == InterState.Empty_k:
            for i in range(NUM_PE):
                self.acts_per_bank.data[i] = 0

            self.reg_addr_w.data = 0
            self.read_addr_reg_D.data = 0
            self.internal_state_D.data = InterState.Empty_k
        else:
            print("Error: unknown state")


        self.write_complete.data = 1
        for i in range(NUM_PE):
            self.read_data_arithm.data[i] = self.ACTmem[arithm_id].data[self.read_data_arithm.data[i] * NUM_PE + i]
            self.write_complete.data = int(self.write_complete.data and (not self.write_enable.data[i]))

        self.layer_complete.data = int(self.write_complete.data and (self.internal_state.data == InterState.Empty_k))

    def update(self):
        arithm_id = 1 - self.which.data

        if self.next_reg_addr.data == 1:
            self.read_addr_reg.data = self.read_addr_reg_D.data
            self.internal_state.data = self.internal_state_D.data

        for i in range(NUM_PE):
            if self.write_enable_D.data[i] == 1:
                self.ACTmem[arithm_id].data[self.write_addr_arithm_D.data[i]*NUM_PE + i] = self.write_data_arithm_D.data[i]

            self.read_addr_arithm.data[i] = self.read_addr_arithm_D.data[i]
            self.write_data_arithm.data[i] = self.write_data_arithm_D.data[i]
            self.write_addr_arithm.data[i] = self.write_addr_arithm_D.data[i]
            self.write_enable.data[i] = self.write_enable_D.data[i]
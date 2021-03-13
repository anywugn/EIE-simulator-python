from module import BaseModule
from component import *
from config import *
import os

class ArithmUnit(BaseModule):
    def __init__(self,filename: str, value: int):
        super().__init__(value)
        self.name = "Arithm Unit"

        # Phase 1 Registers
        self.patch_complete = Register(name="patch_complete")
        self.index = Register(name="index")
        self.value_code = Register(name="value_code")
        self.act_value = Register(name="act_value")
        self.valid = Register(name="valid")

        # Phase 2 registers
        self.read_addr_last = Register(name="read_addr_last")
        self.read_addr_p = Register(name="read_addr_p")
        self.value_decode = Register(name="value_decode")
        self.act_value_p = Register(name="act_value_p")
        self.valid_p = Register(name="valid_p")

        # Phase 3 Registers
        self.read_data = Register(name="read_data")
        self.result_mul = Register(name="result_mul")
        self.valid_p_p = Register(name="valid_p_p")
        self.read_addr_p_p = Register(name="read_addr_p_p")

        # Wires
        self.read_addr = Wire(name="read_addr")
        self.read_addr_last_D = Wire(name="read_addr_last_D")
        self.value_decode_D = Wire(name="value_decode_D")
        self.value_code_w = Wire(name="value_code_w")
        self.value_to_add = Wire(name="value_to_add")
        self.result_muladd = Wire(name="result_muladd")
        self.result_mul_D = Wire(name="result_mul_D")
        self.bypass = Wire(name="bypass")
        self.write_enable = Wire(name="write_enable")
        self.write_addr = Wire(name="write_addr")
        self.write_data = Wire(name="write_data")
        self.valid_w = Wire(name="valid_w")
        self.valid_p_w = Wire(name="valid_p_w")
        self.read_addr_p_w = Wire(name="read_addr_p_w")
        self.act_value_w = Wire(name="act_value_w")

        self.codebook = [0] * ARITHM_codebooksize

        if os.path.isfile(filename):
            with open(filename,'r') as f:
                values = f.read().splitlines()
                for i in range(0, len(values)):
                    self.codebook = float(values[i])


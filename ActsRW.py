from module import BaseModule
from component import *
from config import *
import os

class ActsRW(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "Activation Read/Write"

        self.reg_addr_w = Wire(name="reg_addr_w")
        self.acts_per_bank_D = Wire(width=NUM_PE,name="acts_per_bank_D")
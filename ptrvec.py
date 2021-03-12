from module import *

class PtrRead(BaseModule):
    def __init__():
        self.ptr_odd_addr = Register()
        self.ptr_even_addr = Register()
        self.index_flag = Register()
        self.value = Register()
        self.empty = Register()
        self.read_enable = Register()
    
        self.start_addr = Wire()
        self.end_addr = Wire()
        self.valid = Wire()
        self.value_w = Wire()
        self.index_odd = Wire()
        self.index_even = Wire()
    
    
        self.start_addr_p = Register()
        self.memory_addr_p = Register()
        self.patch_complete_p = Register()
    
        self.patch_complete = Wire()
        self.read_ptr = Wire()
        self.read_spmat = Wire()
        self.current_addr = Wire()
        self.memory_addr = Wire()
        self.memory_shift = Wire()
    
        self.ptr_odd_addr_D = SharedWire()
        self.ptr_even_addr_D = SharedWire()
        self.index_flag_D = SharedWire()
        self.value_D = SharedWire()
        self.empty_D = SharedWire()
    
        self.PTRmem = Memory()
    
        self.num_lines = 0
        self.unit_line = 0
        self.read_times = 0
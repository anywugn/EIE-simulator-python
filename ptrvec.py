from module import *

class PtrRead(BaseModule):
    ptr_odd_addr = Register()
    ptr_even_addr = Register()
    index_flag = Register()
    value = Register()
    empty = Register()
    read_enable = Register()

    start_addr = Wire()
    end_addr = Wire()
    valid = Wire()
    value_w = Wire()
    index_odd = Wire()
    index_even = Wire()


    start_addr_p = Register()
    memory_addr_p = Register()
    patch_complete_p = Register()
    
    patch_complete = Wire()
    read_ptr = Wire()
    read_spmat = Wire()
    current_addr = Wire()
    memory_addr = Wire()
    memory_shift = Wire()

    ptr_odd_addr_D = SharedWire()
    ptr_even_addr_D = SharedWire()
    index_flag_D = SharedWire()
    value_D = SharedWire()
    empty_D = SharedWire()

    PTRmem = Memory()

    num_lines = 0
    unit_line = 0
    read_times = 0
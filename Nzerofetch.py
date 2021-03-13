from module import BaseModule
from component import *
from config import *
import os

class NzeroFetch(BaseModule):
    def __init__(self):
        self.buffer_size = NZEROFETCH_buffersize
        super().__init__()
        self.name = "Non-Zero Fetch"


        # Nzero find Registers
        self.pack_addr_p = Register(name="pack_addr_p")
        self.reg_addr = Register(name="reg_addr")
        self.acts_per_bank = Register(width=NUM_PE, name="acts_per_bank")

        # Wires
        self.one_full = Wire(name="one_full")
        self.find = Wire(name="find")
        self.write_enable = Wire(name="write_enable")
        self.pack_addr = Wire(name="pack_addr")
        self.next_shift = Wire(name="next_shift")
        self.next_reg_addr = Wire(name="next_reg_addr")
        self.value_buffer = Wire(name="value_buffer")
        self.index_buffer = Wire(name="index_buffer")

        # Shared Wires
        self.reg_addr_D = None
        self.acts_per_bank_D = None

        # FIFO part Registers
        self.pos_read = Register(width=NUM_PE, name="pos_read")
        self.pos_write = Register(width=NUM_PE,name="pos_write")
        self.act_index = Register(width=NUM_PE, name="act_index")
        self.value = Register(width=NUM_PE, name="value")
        for i in range(NUM_PE):
            self.act_index.data[i] = [0]*NZEROFETCH_buffersize
            self.value.data[i] = [0]*NZEROFETCH_buffersize

        # Wires
        self.act_index_output = Wire(width=NUM_PE,name="act_index_output")
        self.value_output = Wire(width=NUM_PE,name="value_output")
        self.ptr_odd_addr = Wire(width=NUM_PE,name="ptr_odd_addr")
        self.ptr_even_addr = Wire(width=NUM_PE, name="ptr_even_addr")
        self.index_flag = Wire(width=NUM_PE,name="index_flag")
        self.empty = Wire(width=NUM_PE,name="empty")
        self.full = Wire(width=NUM_PE,name="full")
        self.pos_read_D = Wire(width=NUM_PE,name="pos_read_D")
        self.pos_write_D = Wire(width=NUM_PE,name="pos_write_D")

        # Shared Wires
        self.read_ptr = Wire(width=NUM_PE,name="read_ptr")

    def connect(self, dependency):
        if dependency.getName() == "Activation Read/Write":
            self.reg_addr_D = dependency.reg_addr_w
            dependency.reg_addr_w.shared = True
            self.acts_per_bank_D = dependency.acts_per_bank_D
            dependency.acts_per_bank_D.shared = True
        elif dependency.getName() == "Pointer Read Unit":
            self.read_ptr.data[dependency.getId()] = dependency.read_ptr
            dependency.read_ptr.shared = True
        else:
            print("Error: Connection Error!")


    def propagate(self):
        self.one_full.data = 0

        # FIFO read
        if NUM_PE > 1:
            for i in range(NUM_PE):
                self.pos_read_D.data[i] = (self.pos_read.data[i] + 1) % self.buffer_size
                self.pos_write_D.data[i] = (self.pos_write.data[i] + 1) % self.buffer_size

                self.full.data[i] = int(self.pos_write_D.data[i] == self.pos_read.data[i])
                self.empty.data[i] = int(self.pos_write.data[i] == self.pos_read.data[i])

                self.one_full.data = int(self.one_full.data or self.full.data[i])

                self.value_output.data[i] = self.value.data[i][self.pos_read.data[i]]
                self.act_index_output.data[i] = self.act_index.data[i][self.pos_read.data[i]]
                self.index_flag.data[i] = self.act_index_output.data[i] % 2
                self.ptr_odd_addr.data[i] = self.act_index_output.data[i] // 2
                self.ptr_even_addr.data[i] = (self.act_index_output.data[i] + 1) // 2

        # Find Non Zero entry
        self.find.data = 0
        for i in range((self.pack_addr_p.data+1)%NUM_PE, NUM_PE):
            self.pack_addr.data = i
            if self.acts_per_bank.data[self.pack_addr.data] > 0.0:
                self.find.data = 1
                break

        if self.find.data == 1:
            self.pack_addr.data = self.pack_addr.data
        else:
            self.pack_addr.data = NUM_PE - 1

        self.value_buffer.data = self.acts_per_bank.data[self.pack_addr.data]
        self.index_buffer.data = self.reg_addr.data * NUM_PE + self.pack_addr.data

        self.next_shift.data = int(not(self.one_full.data and self.find.data))
        self.next_reg_addr.data = int((not self.find) or((self.pack_addr.data == NUM_PE-1) and (not self.one_full.data)))

        self.write_enable.data = int(self.find.data and (not self.one_full.data))

    def update(self):
        if self.next_shift.data == 1:
            self.pack_addr_p.data = self.pack_addr.data

        if self.next_reg_addr.data == 1:
            self.reg_addr.data = self.reg_addr_D.data
            self.acts_per_bank.data = self.acts_per_bank_D.data

        if self.write_enable.data == 1:
            for i in range(NUM_PE):
                self.act_index.data[i][self.pos_write.data[i]] = self.index_buffer.data
                self.value.data[i][self.pos_write.data[i]] = self.value_buffer.data
                self.pos_write.data[i] = self.pos_write_D.data[i]

        for i in range(NUM_PE):
            if (not self.empty.data[i]) and self.read_ptr.data[i].data:
                self.pos_read.data[i] = self.pos_read_D.data[i]


    def showSharedWires(self):
        super(NzeroFetch, self).showSharedWires()
        for i in range(NUM_PE):
            print("PE",i,":",self.read_ptr.data[i])


from component import  *
from module import *
from ptrvec import *
from spmat import *
from Nzerofetch import *
from ActsRW import *

def testNzero():
    # test_pointer_read()
    PointerRead0 = PtrRead("file.txt", 0)
    PointerRead1 = PtrRead("file.txt", 1)
    PointerRead2 = PtrRead("file.txt", 2)
    PointerRead3 = PtrRead("file.txt", 3)
    acts = ActsRW()
    NZeroFetch = NzeroFetch()

    NZeroFetch.connect(acts)
    NZeroFetch.connect(PointerRead0)
    NZeroFetch.connect(PointerRead1)
    NZeroFetch.connect(PointerRead2)
    NZeroFetch.connect(PointerRead3)

    PointerRead0.connect(NZeroFetch)
    PointerRead1.connect(NZeroFetch)
    PointerRead2.connect(NZeroFetch)
    PointerRead3.connect(NZeroFetch)

    NZeroFetch.connect(acts)

    # cycle 0
    print("cycle 0")
    acts.acts_per_bank_D.data = [9, 2, 0, 4]
    acts.reg_addr_w.data = 0
    PointerRead0.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 1")
    acts.acts_per_bank_D.data = [9, 2, 0, 4]
    acts.reg_addr_w.data = 0
    PointerRead0.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 2")
    acts.acts_per_bank_D.data = [9, 2, 0, 4]
    acts.reg_addr_w.data = 0
    PointerRead0.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 3")
    acts.acts_per_bank_D.data = [10, 11, 0, 14]
    acts.reg_addr_w.data = 0
    PointerRead0.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 4")
    acts.acts_per_bank_D.data = [10, 11, 0, 14]
    acts.reg_addr_w.data = 1
    PointerRead0.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 5")
    acts.acts_per_bank_D.data = [10, 11, 0, 14]
    acts.reg_addr_w.data = 1
    PointerRead0.read_ptr.data = 1
    PointerRead1.read_ptr.data = 1
    PointerRead2.read_ptr.data = 1
    PointerRead3.read_ptr.data = 1

    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 6")
    acts.acts_per_bank_D.data = [10, 11, 0, 14]
    acts.reg_addr_w.data = 1
    PointerRead0.read_ptr.data = 1
    PointerRead1.read_ptr.data = 0
    PointerRead2.read_ptr.data = 0
    PointerRead3.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 7")
    acts.acts_per_bank_D.data = [10, 11, 0, 14]
    acts.reg_addr_w.data = 1
    PointerRead0.read_ptr.data = 1
    PointerRead1.read_ptr.data = 0
    PointerRead2.read_ptr.data = 0
    PointerRead3.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 8")
    acts.acts_per_bank_D.data = [10, 11, 0, 14]
    acts.reg_addr_w.data = 1
    PointerRead0.read_ptr.data = 1
    PointerRead1.read_ptr.data = 1
    PointerRead2.read_ptr.data = 1
    PointerRead3.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 9")
    acts.acts_per_bank_D.data = [10, 11, 0, 14]
    acts.reg_addr_w.data = 1
    PointerRead0.read_ptr.data = 1
    PointerRead1.read_ptr.data = 1
    PointerRead2.read_ptr.data = 1
    PointerRead3.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()

    print("cycle 10")
    acts.acts_per_bank_D.data = [10, 11, 0, 14]
    acts.reg_addr_w.data = 1
    PointerRead0.read_ptr.data = 1
    PointerRead1.read_ptr.data = 1
    PointerRead2.read_ptr.data = 1
    PointerRead3.read_ptr.data = 1
    NZeroFetch.propagate()
    NZeroFetch.update()
    NZeroFetch.showWires()
    NZeroFetch.showRegs()
def main():
    pointerRead = PtrRead("file.txt",0)
    pointerRead2 = PtrRead("file.txt",1)
    spmat = SpMatRead("spmat.txt",0)
    spmat2 = SpMatRead("spmat.txt",1)

    nzero = NzeroFetch()
    acts = ActsRW()


    nzero.connect(acts)
    nzero.connect(pointerRead)
    nzero.connect(pointerRead2)


    pointerRead.connect(nzero)
    pointerRead2.connect(nzero)
    spmat.connect(pointerRead)
    spmat2.connect(pointerRead2)

    print("cycle 0")
    acts.reg_addr_w.data = 0
    acts.acts_per_bank_D.data = [0,2]

    nzero.propagate()
    pointerRead.propagate()
    spmat.propagate()

    nzero.update()
    pointerRead.update()
    spmat.update()

    nzero.showEssential()
    pointerRead.showEssential()

    print("cycle 1")
    acts.reg_addr_w.data = 0
    acts.acts_per_bank_D.data = [0,2]

    nzero.propagate()
    pointerRead.propagate()
    spmat.propagate()

    nzero.update()
    pointerRead.update()
    spmat.update()

    print("cycle 2")
    acts.reg_addr_w.data = 0
    acts.acts_per_bank_D.data = [0,2]

    nzero.propagate()
    pointerRead.propagate()
    spmat.propagate()

    nzero.update()
    pointerRead.update()
    spmat.update()

    nzero.showEssential()
    pointerRead.showEssential()

    print("cycle 3")
    acts.reg_addr_w.data = 0
    acts.acts_per_bank_D.data = [0,2]

    nzero.propagate()
    pointerRead.propagate()
    spmat.propagate()

    nzero.update()
    pointerRead.update()
    spmat.update()

    nzero.showEssential()
    pointerRead.showEssential()

if __name__ == '__main__':
    main()



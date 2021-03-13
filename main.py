from component import  *
from module import *
from ptrvec import *
from spmat import *
from Nzerofetch import *
from ActsRW import *


def test_pointer_read():
    b = PtrRead("file.txt",0)
    c = NzeroFetch()
    b.connect(c)
    print("start")
    b.showRegs()
    print("cycle 0")
    b.propagate()
    b.update()
    b.showRegs()

    print("cycle 1")
    b.propagate()
    b.update()
    b.showRegs()

    print("cycle 2")
    c.ptr_odd_addr.data[0] = 3
    c.ptr_even_addr.data[0] = 3
    c.index_flag.data[0] = 0
    c.empty.data[0] = 1
    c.value_output.data[0] = 20
    b.showSharedWires()
    b.propagate()
    b.showWires()
    b.update()
    b.showRegs()

    print("cycle 3")
    c.empty.data[0] = 0
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()

    print("cycle 4")
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()

    print("cycle 5")
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()

    print("cycle 6")
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()

    print("cycle 7")
    c.ptr_odd_addr.data[0] = 4
    c.ptr_even_addr.data[0] = 4
    c.index_flag.data[0] = 0
    c.empty.data[0] = 1
    c.value_output.data[0] = 40
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()

    print("cycle 8")
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()

    print("cycle 9")
    c.empty.data[0] = 0
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()

    print("cycle 10")
    c.ptr_odd_addr.data[0] = 5
    c.ptr_even_addr.data[0] = 5
    c.empty.data[0] = 0
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()

    print("cycle 11")
    c.ptr_odd_addr.data[0] = 5
    c.ptr_even_addr.data[0] = 5
    c.empty.data[0] = 0
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()
    print("cycle 12")
    c.ptr_odd_addr.data[0] = 5
    c.ptr_even_addr.data[0] = 5
    c.empty.data[0] = 0
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()
    print("cycle 13")
    c.ptr_odd_addr.data[0] = 5
    c.ptr_even_addr.data[0] = 5
    c.empty.data[0] = 0
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()
    print("cycle 14")
    c.ptr_odd_addr.data[0] = 5
    c.ptr_even_addr.data[0] = 5
    c.empty.data[0] = 0
    b.propagate()
    b.update()
    b.showWires()
    b.showRegs()

    print("cycle 15")
    c.ptr_odd_addr.data[0] = 5
    c.ptr_even_addr.data[0] = 5
    c.empty.data[0] = 0
    b.propagate()
    b.update()
    b.showSharedWires()
    b.showRegs()
def main():
    #test_pointer_read()
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

    NZeroFetch.showSharedWires()

    print(5//2)
if __name__ == '__main__':
    main()



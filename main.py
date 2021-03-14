from component import  *
from module import *
from ptrvec import *
from spmat import *
from Nzerofetch import *
from ActsRW import *
from arithm import *

def cycle(value,acts,nzero,ptr0,ptr1,ptr2,ptr3):
    print("cycle ",value)
    print("----propagate----")
    acts.propagate()
    nzero.propagate()
    ptr0.propagate()
    ptr1.propagate()
    ptr2.propagate()
    ptr3.propagate()

    print("----update----")
    acts.update()
    nzero.update()
    ptr0.update()
    ptr1.update()
    ptr2.update()
    ptr3.update()

    print("\n")


def main():
    acts = ActsRW("activations.txt")
    acts.set_state(20,0,1) # no bias, input 20, which is 0

    nzero = NzeroFetch()

    acts.connect(nzero)
    nzero.connect(acts)

    ptr0 = PtrRead("file.txt", 0)
    ptr1 = PtrRead("file.txt", 1)
    ptr2 = PtrRead("file.txt", 2)
    ptr3 = PtrRead("file.txt", 3)
    nzero.connect(ptr0)
    nzero.connect(ptr1)
    nzero.connect(ptr2)
    nzero.connect(ptr3)
    ptr0.connect(nzero)
    ptr1.connect(nzero)
    ptr2.connect(nzero)
    ptr3.connect(nzero)

    cycle(0,acts,nzero,ptr0,ptr1,ptr2,ptr3)
    cycle(1, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(2, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(3, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(4, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(5, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(6, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(7, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(8, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(9, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(10, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(11, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(12, acts, nzero, ptr0, ptr1, ptr2, ptr3)
    cycle(13, acts, nzero, ptr0, ptr1, ptr2, ptr3)

if __name__ == '__main__':
    main()



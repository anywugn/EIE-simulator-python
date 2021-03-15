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

def testACTNzero():
    acts = ActsRW("activations.txt")
    acts.set_state(30, 0, 1)  # no bias, input 20, which is 0

    nzero = NzeroFetch()

    acts.connect(nzero)
    nzero.connect(acts)

    ptr0 = PtrRead("column_pointer.txt", 0)
    ptr1 = PtrRead("column_pointer.txt", 1)
    ptr2 = PtrRead("column_pointer.txt", 2)
    ptr3 = PtrRead("column_pointer.txt", 3)
    nzero.connect(ptr0)
    nzero.connect(ptr1)
    nzero.connect(ptr2)
    nzero.connect(ptr3)
    ptr0.connect(nzero)
    ptr1.connect(nzero)
    ptr2.connect(nzero)
    ptr3.connect(nzero)

    for i in range(40):
        cycle(i, acts, nzero, ptr0, ptr1, ptr2, ptr3)


def main():
    ptr0 = PtrRead("column_pointer.txt", 0)
    ptr1 = PtrRead("column_pointer.txt", 1)
    ptr2 = PtrRead("column_pointer.txt", 2)
    ptr3 = PtrRead("column_pointer.txt", 3)


    spm0 = SpMatRead("spmat.txt", 0)
    spm1 = SpMatRead("spmat.txt", 1)
    spm2 = SpMatRead("spmat.txt", 2)
    spm3 = SpMatRead("spmat.txt", 3)

    ari0 = ArithmUnit("weight.txt", 0)
    ari1 = ArithmUnit("weight.txt", 1)
    ari2 = ArithmUnit("weight.txt", 2)
    ari3 = ArithmUnit("weight.txt", 3)

    acts = ActsRW("activations.txt")
    acts.set_state(12,0,0)
    Nzero = NzeroFetch()

    ptr0.connect(Nzero)
    ptr1.connect(Nzero)
    ptr2.connect(Nzero)
    ptr3.connect(Nzero)


    spm0.connect(ptr0)
    spm1.connect(ptr1)
    spm2.connect(ptr2)
    spm3.connect(ptr3)

    ari0.connect(spm0)
    ari1.connect(spm1)
    ari2.connect(spm2)
    ari3.connect(spm3)

    ari0.connect(acts)
    ari1.connect(acts)
    ari2.connect(acts)
    ari3.connect(acts)

    acts.connect(ari0)
    acts.connect(ari1)
    acts.connect(ari2)
    acts.connect(ari3)

    acts.connect(Nzero)

    Nzero.connect(acts)
    Nzero.connect(ptr0)
    Nzero.connect(ptr1)
    Nzero.connect(ptr2)
    Nzero.connect(ptr3)


    cycle = 40
    for i in range(cycle):
        print("cycle",i)
        print("----propagate----")

        ptr0.propagate()
        ptr1.propagate()
        ptr2.propagate()
        ptr3.propagate()

        spm0.propagate()
        spm1.propagate()
        spm2.propagate()
        spm3.propagate()

        ari0.propagate()
        ari1.propagate()
        ari2.propagate()
        ari3.propagate()

        acts.propagate()
        Nzero.propagate()
        print("----update----")
        ptr0.update()
        ptr1.update()
        ptr2.update()
        ptr3.update()

        spm0.update()
        spm1.update()
        spm2.update()
        spm3.update()

        ari0.update()
        ari1.update()
        ari2.update()
        ari3.update()


        acts.update()
        Nzero.update()
        print(acts.layer_complete)
        print("\n")
    print(acts.ACTmem[1].data)

if __name__ == '__main__':
    main()
    # acts = ActsRW("activations.txt")
    # for i in range(5):
    #     acts.__setattr__("nigga"+str(i),Wire(name="nigga"+str(i)))
    # print(acts.nigga0)
    # print(acts.nigga2)
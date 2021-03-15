from component import  *
from module import *
from ptrvec import *
from spmat import *
from Nzerofetch import *
from ActsRW import *
from arithm import *

def assemble(NUM_PE,cycle):
    ptr = []
    spm = []
    ari = []

    acts = ActsRW("activations.txt")
    acts.set_state(13,0,0)
    nzero = NzeroFetch()

    for i in range(NUM_PE):
        ptr.append(PtrRead("column_pointer.txt",i))
        spm.append(SpMatRead("spmat.txt", i))
        ari.append(ArithmUnit("weight.txt", i))

    for i in range(len(ptr)):
        ptr[i].connect(nzero)

    for i in range(len(spm)):
        spm[i].connect(ptr[i])

    for i in range(len(ari)):
        ari[i].connect(spm[i])
        ari[i].connect(acts)

    for i in range(len(ari)):
        acts.connect(ari[i])
        nzero.connect(ptr[i])

    acts.connect(nzero)
    nzero.connect(acts)

    for i in range(cycle):
        print("cycle", i)
        print("----propagate----")
        for i in range(len(ptr)):
            ptr[i].propagate()
            spm[i].propagate()
            ari[i].propagate()
        acts.propagate()
        nzero.propagate()
        print("----update----")
        for i in range(len(ptr)):
            ptr[i].update()
            spm[i].update()
            ari[i].update()
        acts.update()
        nzero.update()
        print(acts.layer_complete)
        print("\n")
    print(acts.ACTmem[1].data)

def main():
    assemble(NUM_PE,50)
    # ptr0 = PtrRead("column_pointer.txt", 0)
    # ptr1 = PtrRead("column_pointer.txt", 1)
    # ptr2 = PtrRead("column_pointer.txt", 2)
    # ptr3 = PtrRead("column_pointer.txt", 3)
    #
    #
    # spm0 = SpMatRead("spmat.txt", 0)
    # spm1 = SpMatRead("spmat.txt", 1)
    # spm2 = SpMatRead("spmat.txt", 2)
    # spm3 = SpMatRead("spmat.txt", 3)
    #
    # ari0 = ArithmUnit("weight.txt", 0)
    # ari1 = ArithmUnit("weight.txt", 1)
    # ari2 = ArithmUnit("weight.txt", 2)
    # ari3 = ArithmUnit("weight.txt", 3)
    #
    # acts = ActsRW("activations.txt")
    # acts.set_state(13,0,0)
    # Nzero = NzeroFetch()
    #
    # ptr0.connect(Nzero)
    # ptr1.connect(Nzero)
    # ptr2.connect(Nzero)
    # ptr3.connect(Nzero)
    #
    #
    # spm0.connect(ptr0)
    # spm1.connect(ptr1)
    # spm2.connect(ptr2)
    # spm3.connect(ptr3)
    #
    # ari0.connect(spm0)
    # ari1.connect(spm1)
    # ari2.connect(spm2)
    # ari3.connect(spm3)
    #
    # ari0.connect(acts)
    # ari1.connect(acts)
    # ari2.connect(acts)
    # ari3.connect(acts)
    #
    # acts.connect(ari0)
    # acts.connect(ari1)
    # acts.connect(ari2)
    # acts.connect(ari3)
    #
    # acts.connect(Nzero)
    # Nzero.connect(acts)
    #
    #
    # Nzero.connect(ptr0)
    # Nzero.connect(ptr1)
    # Nzero.connect(ptr2)
    # Nzero.connect(ptr3)
    #
    #
    # cycle = 50
    # for i in range(cycle):
    #     print("cycle",i)
    #     print("----propagate----")
    #
    #     ptr0.propagate()
    #     ptr1.propagate()
    #     ptr2.propagate()
    #     ptr3.propagate()
    #
    #     spm0.propagate()
    #     spm1.propagate()
    #     spm2.propagate()
    #     spm3.propagate()
    #
    #     ari0.propagate()
    #     ari1.propagate()
    #     ari2.propagate()
    #     ari3.propagate()
    #
    #     acts.propagate()
    #     Nzero.propagate()
    #     print("----update----")
    #     ptr0.update()
    #     ptr1.update()
    #     ptr2.update()
    #     ptr3.update()
    #
    #     spm0.update()
    #     spm1.update()
    #     spm2.update()
    #     spm3.update()
    #
    #     ari0.update()
    #     ari1.update()
    #     ari2.update()
    #     ari3.update()
    #
    #
    #     acts.update()
    #     Nzero.update()
    #     print(acts.layer_complete)
    #     print("\n")
    # print(acts.ACTmem[1].data)

if __name__ == '__main__':
    main()
    # acts = ActsRW("activations.txt")
    # for i in range(5):
    #     acts.__setattr__("nigga"+str(i),Wire(name="nigga"+str(i)))
    # print(acts.nigga0)
    # print(acts.nigga2)
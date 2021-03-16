from component import  *
from module import *
from ptrvec import *
from spmat import *
from Nzerofetch import *
from ActsRW import *
from arithm import *

def assemble(folderpath,NUM_PE,cycle):
    ptr = []
    spm = []
    ari = []

    # acts = ActsRW("./alexNet (extract.me)/act.dat")
    # print()
    # ari = ArithmUnit("./alexNet (extract.me)/arithm.dat",0)
    # print()
    # ptr = PtrRead("./alexNet (extract.me)/ptr/ptr14.dat",0)
    # print()
    # spm = SpMatRead("./alexNet (extract.me)/spm/spm14.dat",0)
    #



    acts = ActsRW(folderpath+"/act.dat")
    print("Activation length:",acts.activation_length)
    acts.set_state(acts.activation_length,0,1)

    nzero = NzeroFetch()

    for i in range(NUM_PE):
        ptr.append(PtrRead(folderpath+"/ptr/ptr"+str(i)+".dat",i))
        spm.append(SpMatRead(folderpath+"/spm/spm"+str(i)+".dat", i))
        ari.append(ArithmUnit(folderpath+"/arithm.dat", i))

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

    j = 0
    while acts.layer_complete.data != 1:
        print("cycle", j)
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
        j+=1
    print(acts.ACTmem[1].data[0:4000])

def main():
    assemble("./alexNet (extract.me)",NUM_PE,100000)
    # acts = ActsRW("./alexNet (extract.me)/act.dat")
    # print()
    # ari = ArithmUnit("./alexNet (extract.me)/arithm.dat",0)
    # print()
    # ptr = PtrRead("./alexNet (extract.me)/ptr/ptr14.dat",0)
    # print()
    # spm = SpMatRead("./alexNet (extract.me)/spm/spm14.dat",0)


        # ind = 0
        # for i in flt:
        #     self.ACTmem[self.which.data].data[ind] = flt[ind]
        #     ind += 1


if __name__ == '__main__':
    main()

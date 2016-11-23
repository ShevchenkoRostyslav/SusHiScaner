import sys
sys.path.insert(0,'../project')
from lib.basis import *

if __name__ == '__main__':

    #dictionary with physicalbasis inside
    iput = {'basis' : 'physicalbasis', 'higgsType' : 11, 'thdmType' : '1', 'm12' : '100', 'tanBeta' : '20', \
            'mh' : '125','mH' : '250','mA' : 300,'mC' : '300','sinB_A' : '0.99999','lambda6' : '0','lambda7' : '0'}
    #Instance of Basis class:
    basis = Basis(iput)
    print basis
    #Instance of Basis class that call stat method:
    basis_stat = Basis.choose_basis(iput)
    print basis_stat



    # basis = Basis('physicalbasis', "1", '1', '1', '1', '1', '1', '1', '1', '1', '1', '1')
    # basis.choose_basis('physicalbasis')
    print basis

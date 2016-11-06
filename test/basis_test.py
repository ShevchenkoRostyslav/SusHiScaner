import sys
sys.path.insert(0,'../project')
from lib.basis import *

if __name__ == '__main__':

    #Instance of Basis class:
    basis = Basis.choose_basis('physicalbasis')
    # basis = Basis('physicalbasis', "1", '1', '1', '1', '1', '1', '1', '1', '1', '1', '1')
    # basis.choose_basis('physicalbasis')
    print basis

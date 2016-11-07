#!/usr/bin/python
import sys
'''
Basic class-container, to store information about basises
'''

def reiseAttributeError(list,ref_list):
    for l in list:
        if l not in ref_list:
            raise AttributeError('ERROR: '+ l + ' variable wasn`t provided in setInput.py. Please check spelling')

def checkInputValidity(iput):
    #Method to check whether all variables were properly named and provided
    general_list = ['basis','m12','higgsType','thdmType','tanBeta']
    physics_basis_list = ['mh','mH','mA','mC','sinB_A','lambda6','lambda7']
    lambda_basis_list = ['lambda1','lambda2','lambda3','lambda4','lambda5','lambda6','lambda7']
    reiseAttributeError(general_list, iput)
    if iput['basis'] == 'physicalbasis': reiseAttributeError(physics_basis_list, iput)
    elif iput['basis'] == 'lambdabasis': reiseAttributeError(lambda_basis_list, iput)
    else : AttributeError('ERROR: program doesn`t work with ' + iput['basis'] + ' yet. Please make a setup for physicalbasis or lambdabasis')

class Basis(object):
    """docstring for Basis ."""
    def __init__(self, iput):
        checkInputValidity(iput)
        self.iput = iput

    ''''''
    def __str__(self):
        return 'Basis container, with: \n higgsType = ' + self.iput['higgsType'] + \
        ' thdmType = ' + self.iput['thdmType'] + ' m12 = ' + self.iput['m12'] + ' tanBeta = ' + \
        self.iput['tanBeta'] + ' ' + self.iput['basis']

    def choose_basis(iput = None):
        iput = iput or self.iput
        basis = iput['basis']
        if basis == 'physicalbasis':
            return PhysicalBasis(iput)
        elif basis == 'lambdabasis':
            return LambdaBasis(iput)
        else:
            raise AttributeError('No basis called: ' + basis + 'exists.')
            return
    choose_basis = staticmethod(choose_basis)

class PhysicalBasis(Basis):
    def __init__(self, higgsType, thdmType, m12, tanBeta, mh, mH, mA, mC, sinB_A, lambda6, lambda7):
        super(PhysicalBasis, self).__init__(iput)
        self.basis = 'physicalbasis'
        self.mh = mh
        self.mH = mH
        self.mA = mA
        self.mC = mC
        self.sinB_A = sinB_A
        self.lambda6 = lambda6
        self.lambda7 = lambda7

    '''Constructor from dictionary'''
    def __init__(self,iput):
        super(PhysicalBasis, self).__init__(iput)
        self.basis = 'physicalbasis'
        self.mh = iput['mh']
        self.mH = iput['mH']
        self.mA = iput['mA']
        self.mC = iput['mC']
        self.sinB_A = iput['sinB_A']
        self.lambda6 = iput['lambda6']
        self.lambda7 = iput['lambda7']


    def __str__(self):
        basis_out = super().__str__()
        phys_out  = 'mh = ' + mh
        return basis_out + '\n' + phys_out



class LambdaBasis(Basis):
    def __init__(self, higgsType, thdmType, m12, tanBeta, lambda1, lambda2, lambda3, lambda4, lambda5, lambda6, lambda7):
        self.basis = 'lambdabasis'
        super(LambdaBasis, self).__init__()

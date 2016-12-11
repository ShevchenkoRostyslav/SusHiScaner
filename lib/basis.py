#!/usr/bin/python
import sys

__author__ = "Rostyslav Shevchenko"
__maintainer__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"

def raiseAttributeError(list,ref_list):
    """Function to compare one list with another and raise error.

    """
    for l in list:
        if l not in ref_list:
            raise AttributeError('ERROR: '+ l + ' variable wasn`t provided. Please check spelling')

def checkInputValidity(iput):
    """Method to check validity of the user input.

    """
    #List of general variables
    general_list = ['basis','m12','higgsType','thdmType','tanBeta']
    #List from physics basis
    physics_basis_list = ['mh','mH','mA','mC','sinB_A','lambda6','lambda7']
    #List from lambda basis
    lambda_basis_list = ['lambda1','lambda2','lambda3','lambda4','lambda5','lambda6','lambda7']
    raiseAttributeError(general_list, iput)
    if iput['basis'] == 'physicalbasis': raiseAttributeError(physics_basis_list, iput)
    elif iput['basis'] == 'lambdabasis': raiseAttributeError(lambda_basis_list, iput)
    else : raise AttributeError('ERROR: program doesn`t work with ' + iput['basis'] + ' yet. Please make a setup for physicalbasis or lambdabasis')

class Basis(object):
    """Class-container, to store information about basis.

    Designed within factory pattern.
    """
    def __init__(self, iput):
        """Constructor.
        @arguments:
            iput - input basis
        """
        checkInputValidity(iput)
        self.iput = iput

    def __str__(self):
        return 'Basis container, with: \n higgsType = ' + str(self.iput['higgsType']) + \
        ' thdmType = ' + str(self.iput['thdmType']) + ' m12 = ' + str(self.iput['m12']) + ' tanBeta = ' + \
        str(self.iput['tanBeta']) + ' ' + str(self.iput['basis'])

    def choose_basis(iput = None):
        """Method to choose basis accroding to input.

        Realisation of factory pattern.
        """
        iput = iput or self.iput
        #Define returned class by 'basis' from input dictionary
        basis = iput['basis']
        if basis == 'physicalbasis':
            return PhysicalBasis(iput)
        elif basis == 'lambdabasis':
            return LambdaBasis(iput)
        else:
            raise AttributeError('No basis called: ' + str(basis) + 'exists.')
            return
    choose_basis = staticmethod(choose_basis)

class PhysicalBasis(Basis):
    """Class-container, to store information about physical basis.

    """
    def __init__(self, higgsType, thdmType, m12, tanBeta, mh, mH, mA, mC, sinB_A, lambda6, lambda7):
        """Constructor from variables.

        @arguments:
            - higgsType : type of the higgs boson to be considered : 11 - light CP-even, 12 - massive CP-even, 21 - CP-odd
            - thdmType  : type of 2HDM model to be used : 1 - Type I, 2 - Type II, 3 - Flipped, 4 - Lepton Specific
            - m12       : mass mixing term
            - tanBeta   : tanBeta - ratio of vev for two states
            - mh        : mass of light CP-even Higgs
            - mH        : mass of heavy CP-even Higgs
            - mA        : mass of pseudo-scalar (CP-odd) Higgs
            - mC        : mass of charged Higgs
            - sinB_A    : sin(beta-alpha)
            - lambda6   : lambda6
            - lambda7   : lambda7
        """
        # Create dictionary from input variables
        self.iput = {'basis' : 'physicalbasis','m12' : m12,'higgsType' : higgsType,'thdmType' : thdmType,'tanBeta' : tanBeta ,\
                'mh' : mh,'mH' : mH,'mA' : mA,'mC' : mC,'sinB_A' : sinB_A,'lambda6' : lambda6,'lambda7' : lambda7}
        super(PhysicalBasis,self).__init__(iput)
        self.basis = 'physicalbasis'
        self.mh = mh
        self.mH = mH
        self.mA = mA
        self.mC = mC
        self.sinB_A = sinB_A
        self.lambda6 = lambda6
        self.lambda7 = lambda7
        self.higgsType = higgsType
        self.thdmType = thdmType
        self.m12 = m12
        self.tanBeta = tanBeta

    def __init__(self,iput):
        """Constructor from dictionary.

        @arguments:
            - iput      : dictionary that contains information about:
                -- higgsType : type of the higgs boson to be considered : 11 - light CP-even, 12 - massive CP-even, 21 - CP-odd
                -- thdmType  : type of 2HDM model to be used : 1 - Type I, 2 - Type II, 3 - Flipped, 4 - Lepton Specific
                -- m12       : mass mixing term
                -- tanBeta   : tanBeta - ratio of vev for two states
                -- mh        : mass of light CP-even Higgs
                -- mH        : mass of heavy CP-even Higgs
                -- mA        : mass of pseudo-scalar (CP-odd) Higgs
                -- mC        : mass of charged Higgs
                -- sinB_A    : sin(beta-alpha)
                -- lambda6   : lambda6
                -- lambda7   : lambda7
        """
        super(PhysicalBasis,self).__init__(iput)
        self.iput = iput
        self.basis = 'physicalbasis'
        self.mh = iput['mh']
        self.mH = iput['mH']
        self.mA = iput['mA']
        self.mC = iput['mC']
        self.sinB_A = iput['sinB_A']
        self.lambda6 = iput['lambda6']
        self.lambda7 = iput['lambda7']
        self.higgsType = iput['higgsType']
        self.thdmType = iput['thdmType']
        self.m12 = iput['m12']
        self.tanBeta = iput['tanBeta']

    def __str__(self):
        basis_out = super(PhysicalBasis,self).__str__()
        phys_out  = 'mh = ' + str(self.mh) + ' mH = ' + str(self.mH) + ' mA = ' + str(self.mA) + ' mC = ' + str(self.mC) + \
        'sinB_A = ' + str(self.sinB_A) + ' lambda6 = ' + str(self.lambda6) + ' lambda7 = ' + str(self.lambda7)
        return basis_out + '\n' + phys_out



class LambdaBasis(Basis):
    """Class-container, to store information about lambda basis.

    """

    def __init__(self, higgsType, thdmType, m12, tanBeta, lambda1, lambda2, lambda3, lambda4, lambda5, lambda6, lambda7):
        """Constructor from variables.

        @arguments:
            - higgsType : type of the higgs boson to be considered : 11 - light CP-even, 12 - massive CP-even, 21 - CP-odd
            - thdmType  : type of 2HDM model to be used : 1 - Type I, 2 - Type II, 3 - Flipped, 4 - Lepton Specific
            - m12       : mass mixing term
            - tanBeta   : tanBeta - ratio of vev for two states
            - lambda1   : lambda1
            - lambda2   : lambda2
            - lambda3   : lambda3
            - lambda4   : lambda4
            - lambda5   : lambda5
            - lambda6   : lambda6
            - lambda7   : lambda7
        """
        self.basis = 'lambdabasis'
        iput = {'basis' : 'lambdabasis','m12' : m12,'higgsType' : higgsType,'thdmType' : thdmType,'tanBeta' : tanBeta ,\
                'lambda1' : lambda1,'lambda2' : lambda2,'lambda3' : lambda3,'lambda4' : lambda4,'lambda5' : lambda5,'lambda6' : lambda6,'lambda7' : lambda7}
        super(LambdaBasis, self).__init__(iput)
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.lambda3 = lambda3
        self.lambda4 = lambda4
        self.lambda5 = lambda5
        self.lambda6 = lambda6
        self.lambda7 = lambda7
        self.higgsType = higgsType
        self.thdmType = thdmType
        self.m12 = m12
        self.tanBeta = tanBeta

    def __init__(self,iput):
        """Constructor from dictionary.

        @arguments:
            - iput      : input dictionary that contains information about:
                -- higgsType : type of the higgs boson to be considered : 11 - light CP-even, 12 - massive CP-even, 21 - CP-odd
                -- thdmType  : type of 2HDM model to be used : 1 - Type I, 2 - Type II, 3 - Flipped, 4 - Lepton Specific
                -- m12       : mass mixing term
                -- tanBeta   : tanBeta - ratio of vev for two states
                -- lambda1   : lambda1
                -- lambda2   : lambda2
                -- lambda3   : lambda3
                -- lambda4   : lambda4
                -- lambda5   : lambda5
                -- lambda6   : lambda6
                -- lambda7   : lambda7
        """
        super(LambdaBasis,self).__init__(iput)
        self.basis = 'lambdabasis'
        self.lambda1 = iput['lambda1']
        self.lambda2 = iput['lambda2']
        self.lambda3 = iput['lambda3']
        self.lambda4 = iput['lambda4']
        self.lambda5 = iput['lambda5']
        self.lambda6 = iput['lambda6']
        self.lambda7 = iput['lambda7']
        self.higgsType = iput['higgsType']
        self.thdmType = iput['thdmType']
        self.m12 = iput['m12']
        self.tanBeta = iput['tanBeta']

    def __str__(self):
        basis_out = super(LambdaBasis,self).__str__()
        phys_out  = 'lambda1 = ' + str(self.lambda1) + ' lambda2 = ' + str(self.lambda2) + ' lambda3 = ' + str(self.lambda3) + ' lambda4 = ' + str(self.lambda4) + \
        'lambda5 = ' + str(self.lambda5) + ' lambda6 = ' + str(self.lambda6) + ' lambda7 = ' + str(self.lambda7)
        return basis_out + '\n' + phys_out

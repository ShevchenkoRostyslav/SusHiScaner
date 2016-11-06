#!/usr/bin/python
import sys
'''
Basic class-container, to store information about basises
'''

class Basis(object):
    """docstring for Basis ."""
    def __init__(self, basis, higgsType, thdmType, m12, tanBeta, v1, v2, v3, v4, v5, v6, v7):
        self.basis = basis
        self.higgsType = higgsType
        self.thdmType = thdmType
        self.m12 = m12
        self.tanBeta = tanBeta
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.v5 = v5
        self.v6 = v6
        self.v7 = v7

    ''''''
    def __str__(self):
        return 'Basis container, with: \n higgsType = ' + self.higgsType + \
        ' thdmType = ' + self.thdmType + ' m12 = ' + self.m12 + ' tanBeta = ' + self.tanBeta + \
        ' \n' + self.basis + ' vars: v1 = ' + self.v1 + ' v2 = ' + self.v2 + ' v3 = ' + self.v3 + \
        ' v4 = ' + self.v4 + ' v5 = ' + self.v5 + ' v6 = ' + self.v6 + ' v7 = ' + self.v7

    def choose_basis(basis, higgsType, thdmType, m12, tanBeta, v1, v2, v3, v4, v5, v6, v7):
        higgsType = higgsType or self.higgsType
        thdmType = thdmType or self.thdmType
        m12 = m12 or self.m12
        tanBeta = tanBeta or self.tanBeta
        v1 = v1 or self.v1
        v2 = v2 or self.v2
        v3 = v3 or self.v3
        v4 = v4 or self.v4
        v5 = v5 or self.v5
        v6 = v6 or self.v6
        v7 = v7 or self.v7
        if basis == 'physicalbasis':
            return PhysicalBasis(higgsType, thdmType, m12, tanBeta, v1, v2, v3, v4, v5, v6, v7)
        elif basis == 'lambdabasis':
            return LambdaBasis(higgsType, thdmType, m12, tanBeta, v1, v2, v3, v4, v5, v6, v7)
        else:
            raise AttributeError('No basis called: ' + basis + 'exists.')
            return
    choose_basis = staticmethod(choose_basis)

class PhysicalBasis(Basis):
    def __init__(self, higgsType, thdmType, m12, tanBeta, v1, v2, v3, v4, v5, v6, v7):
        super(PhysicalBasis, self).__init__()
        print 'WTF'

class LambdaBasis(Basis):
    def __init__(self, higgsType, thdmType, m12, tanBeta, v1, v2, v3, v4, v5, v6, v7):
        super(LambdaBasis, self).__init__()
        print 'LOL'

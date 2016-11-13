#!/usr/bin/python
import logging
import math
import sys
sys.path.insert(0,'../project')
from lib.basis import *

#Method used to setup arrays of input vars
#Also parameters can be setupped via functions
#for example:
def getMA_Hhh(Mh,MH, SinBA):
    Z5 = -2
    CosBA = math.sqrt(1-float(SinBA)**2)
    MA2 = (MH**2)*(1-CosBA**2) + (Mh**2)*(CosBA**2) - Z5*((246.)**2)
    MA = math.sqrt(MA2)
    return MA

def getm12_Hhh(Mh,MH, SinBA,tanB,Z7):
    # assume MA=MC
    Z5 = -2
    Z4 = -2
    CosBA = math.sqrt(1-float(SinBA)**2)
    MA2 = (MH**2)*(1-CosBA**2) + (Mh**2)*(CosBA**2) - Z5*((246.)**2)
    MA = math.sqrt(MA2)
    MC = MA

    Z6 = (Mh**2-MH**2)*CosBA*math.sqrt(1-CosBA**2)
    Z6 /= (246.)**2

    Beta = math.atan(tanB)
    L5 = Z5+0.5*(Z6-Z7)*math.tan(2*Beta)
    if tanB > 1:
       m12sq = 0.5*math.sin(2*Beta)*(MA2+L5*(246.)**2)
    elif tanB == 1:
       m12sq = 0
    m12 = math.sqrt(m12sq)
    return m12

def setInputs():
    logging.debug('I`m in setInput::setInput')
    #Physical basis
    # Types of 2HDM to be processed 1 / 2 / 3 / 4
    thdmTypes = [1]
    #Types of higgs bosons
    higgsTypes = [11, 12, 21]#h,H,A
    #tanBetas
    tanBetas = [1.,2.]
    #H masses
    mH = [145.0, 145.5]
    #h masses
    mh = [125.]
    #sin(beta - alpha)
    sinB_As = [0.9949874]
    #A masses
    mA = []
    #m12 Parameter
    m12 = []

    basis = []
    for h in mh:
        for H in mH:
            for b_a in sinB_As:
                for t_b in tanBetas:
                    for ht in higgsTypes:
                        #A masses
                        A = getMA_Hhh(h, H, b_a)
                        mA.append(A)
                        # Charge H masses asuume to be equal to A
                        C = A
                        #m12 Parameter
                        m_12 = getm12_Hhh(h,H,b_a,t_b,0)
                        m12.append(m_12)
                        # Append valeus to Basis class
                        dic = {'basis':'physicalbasis','mh':h,'mH':H,'mA':A,'m12':m_12,'mC':A,'tanBeta':t_b,'thdmType':thdmTypes[0],\
                            'higgsType':ht,'lambda6':0,'lambda7':0,'sinB_A':b_a}
                        bas = Basis.choose_basis(dic)
                        basis.append(bas)


    return basis

#!/usr/bin/python
import logging
import math

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
    for h in mh:
        for H in mH:
            for b_a in sinB_As:
                #A masses
                mA.append(getMA_Hhh(h, H, b_a))

                for t_b in tanBetas:
                    #m12 Parameter
                    m12.append(getm12_Hhh(h,H,b_a,t_b,0))

    #mC mass
    mC = mA
    #Another basis
    lambda1 = []
    lambda2 = []
    lambda3 = []
    lambda4 = []
    lambda5 = []
    lambda6 = []
    lambda7 = []

    #used basis
    basis = 'physicalbasis'

    #return list
    iput = {'basis':basis,
            'mh':mh,'mH':mH,'mA':mA,'m12':m12,'mC':mC,
            'tanBetas':tanBetas,
            'thdmTypes':thdmTypes,'sinB_As':sinB_As,
            'higgsTypes':higgsTypes,
            'lambda6':lambda6, 'lambda7':lambda7}

    return iput

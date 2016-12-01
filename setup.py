#!/usr/bin/python
import logging
import math
import sys
import os
# sys.path.insert(0,'../project')
from lib.basis import *

#Method used to setup arrays of input vars
#Also parameters can be setupped via functions
#for example:

def getM12(MH,tanB):
    # Please specify here algorithm of m12 calculation
    Beta = math.atan(tanB)
    m12 = MH**2 * (math.sin(Beta)*math.cos(Beta))
    m12 = math.sqrt(m12)
    return m12

def setInputs():
    logging.debug('I`m in setInput::setInput')
    #Physical basis
    # Types of 2HDM to be processed 1 / 2 / 3 / 4
    thdmTypes = [3]
    #Types of higgs bosons
    higgsTypes = [21]#h,H,A
    #tanBetas
    tanBetaRange = [10.,100.]
    tanBetaStep = 0.25
    tanBetas = [ tanBetaRange[0]+tanBetaStep*i for i in range(int((tanBetaRange[1]-tanBetaRange[0])/tanBetaStep+1)) ]
    #H masses
    mH_range = [150,1300]
    mH_step = 50.
    #mH = [mH_range[0] + mH_step * i for i in range(int((mH_range[1] - mH_range[0])/mH_step + 1))]
    mH = [200,250,300,350,400,500,600,700,800,900,1100,1300]
    #h masses
    mh = [125.]
    #sin(beta - alpha)
    sinB_A_Range = [0.8,1]
    sinB_A_step = 0.002
    sinB_As = [sinB_A_Range[0] + sinB_A_step* i for i in range(int((sinB_A_Range[1] - sinB_A_Range[0])/sinB_A_step + 2))]
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
                        for thdmType in thdmTypes:
                            #A masses
                            A = H
                            # Charge H masses asuume to be equal to A
                            C = A
                            #m12 Parameter
                            m_12 = getM12(H,t_b)
                            # Append valeus to Basis class
                            dic = {'basis':'physicalbasis','mh':h,'mH':H,'mA':A,'m12':m_12,'mC':A,'tanBeta':t_b,'thdmType':thdmType,\
                            'higgsType':ht,'lambda6':0,'lambda7':0,'sinB_A':b_a}
                            bas = Basis.choose_basis(dic)
                            basis.append(bas)


    return basis

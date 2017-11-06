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

def TranslateCosB_To_sinA(cos_bins):
    """Function to trasfer cos(beta-alpha) binning in conv. B to sin(beta-alpha) in conv. A.

    convention B: 0 < beta-alpha < Pi
    convention A: -90 < beta-alpha < 90
    """
    sin_beta_alpha_A = []
    for p in cos_bins:
        #calculate the sin
        s_beta_alpha_B = math.sqrt(1 - p**2)
        #translate convention B to A
        s_beta_alpha_A = s_beta_alpha_B
        if p < 0:
            s_beta_alpha_A *= -1
        sin_beta_alpha_A.append(s_beta_alpha_A)
    return sin_beta_alpha_A

def getMC(mA,mW):
   #exact tree-level mssm
   mC = math.sqrt(mA**2 + mW**2)
   return mC

def getMH(mA,mZ,tanB):
    #exact tree-level mssm
    cos2B = 2./(tanB**2 + 1) - 1
    mH = 0.5 * (mA**2 + mZ**2 + math.sqrt((mA**2 + mZ**2)**2 - 4.*mA**2*mZ**2*cos2B**2))
    mH = math.sqrt(mH)
    return mH

def getM12(MH,tanB):
    # Please specify here algorithm of m12 calculation
    sin2B = 2. * tanB / (1. + tanB**2)
    Beta = math.atan(tanB)
    m12 = MH**2 * (math.sin(Beta)*math.cos(Beta))
    m12 = math.sqrt(m12)
    return m12

def setInputs():
    logging.debug('I`m in setInput::setInput')
    #Physical basis
    # Types of 2HDM to be processed 1 / 2 / 3 / 4
    thdmTypes = [1,2,3,4]
    #Types of higgs bosons
    higgsTypes = [12,21]#h,H,A
    #tanBetas
    tanBetaLowRange = [0.5,2]
    tanBetaLowStep  = 0.05
    tanBetasLow = [ tanBetaLowRange[0]+tanBetaLowStep*i for i in range(int((tanBetaLowRange[1]-tanBetaLowRange[0])/tanBetaLowStep)) ]
    tanBetaRange = [2.,100.]
    tanBetaStep = 0.5
    tanBetas = [ tanBetaRange[0]+tanBetaStep*i for i in range(int((tanBetaRange[1]-tanBetaRange[0])/tanBetaStep+1)) ]
    tanBetas = tanBetasLow + tanBetas
    #H masses
    mH_range = [150,1300]
    mH_step = 50.
    #mH = [mH_range[0] + mH_step * i for i in range(int((mH_range[1] - mH_range[0])/mH_step + 1))]
    mH = [200,250,300,350,400,500,600,700,800,900,1100,1300]
    #h masses
    mh = [125.]
    #sin(beta - alpha)
    #use cos(beta-alpha)
    cosB_A_Range = [0,1]
    cosB_A_step = 0.005
    cosB_As = [cosB_A_Range[0] + cosB_A_step* i for i in range(int((cosB_A_Range[1] - cosB_A_Range[0])/cosB_A_step + 1))]
    sinB_As = TranslateCosB_To_sinA(cosB_As)
    # sinB_A_Range = [-1,1]
    # sinB_A_step = 0.002
    # sinB_As = [sinB_A_Range[0] + sinB_A_step* i for i in range(int((sinB_A_Range[1] - sinB_A_Range[0])/sinB_A_step + 1))]
    #A masses
    mA = [200,250,300,350,400,500,600,700,800,900,1100,1300]
    # mA = [300,350,400,500,600,700,800,900,1100,1300]
    #m12 Parameter
    m12 = []
    #mass of Z boson:
    mZ = 91.1876 #from pdg
    mW = 80.385  #from pdg

    basis = []
    for h in mh:
        for A in mA:
            for b_a in sinB_As:
                for t_b in tanBetas:
                    for ht in higgsTypes:
                        for thdmType in thdmTypes:
                            #A masses
                            H = A
                            # Charge H masses asuume to be equal to A
                            C = A
                            #m12 Parameter
                            m_12 = getM12(A, t_b)
                            # Append valeus to Basis class
                            dic = {'basis':'physicalbasis','mh':h,'mH':H,'mA':A,'m12':m_12,'mC':C,'tanBeta':t_b,'thdmType':thdmType,\
                            'higgsType':ht,'lambda6':0,'lambda7':0,'sinB_A':b_a}
                            bas = Basis.choose_basis(dic)
                            basis.append(bas)


    return basis

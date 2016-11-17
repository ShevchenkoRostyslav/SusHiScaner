#!/usr/bin/python
'''
Functions to read and modify the datacards
'''
from subprocess import call

def modifyDataCard(path, Hmass, tanbeta, sinb_a, thdmType, higgsType, HAMass, HCMass, m12): #run sushi with multiple mass, tanbeta, sin points, get input from file that submit jobs

    name = '2HDMC_physicalbasis' 
    templateInput = path + name + '.in'

    tempInput  = 'type' + thdmType + '_mH' + Hmass + '_tanB' + tanbeta + '_sinBA' + sinb_a + '_A' + HAMass + '_Hp' + HCMass + '_xs' + higgsType + '.in'
    tempOutput = 'type' + thdmType + '_mH' + Hmass + '_tanB' + tanbeta + '_sinBA' + sinb_a + '_A' + HAMass + '_Hp' + HCMass + '_xs' + higgsType + '.out'
    tempLog    = 'type' + thdmType + '_mH' + Hmass + '_tanB' + tanbeta + '_sinBA' + sinb_a + '_A' + HAMass + '_Hp' + HCMass + '_xs' + higgsType + '.log'

    call('cp ' + templateInput + ' ' + tempInput, shell=True)
    call("sed -i 's/HMASS/" + Hmass + "/g' " + tempInput, shell=True)
    call("sed -i 's/TANBETA/" + tanbeta + "/g' " + tempInput, shell=True)
    call("sed -i 's/SINB_A/" + sinb_a + "/g' " + tempInput, shell=True)
    call("sed -i 's/THDMTYPE/" + thdmType + "/g' " + tempInput, shell=True)
    call("sed -i 's/HIGGSTYPE/" + higgsType + "/g' " + tempInput, shell=True)
    call("sed -i 's/HAMASS/" + HAMass + "/g' " + tempInput, shell=True)
    call("sed -i 's/HCMASS/" + HCMass + "/g' " + tempInput, shell=True)
    call("sed -i 's/M12/" + m12 + "/g' " + tempInput, shell=True)
     
    call('./sushi ' + tempInput + ' ' + tempOutput + ' > ' + tempLog, shell=True)
    call('cat 2HDMC.out >> ' + tempOutput, shell=True)
    
def modifyDataCard(path, thdmType, tanbeta, m12, lambda1, lambda2, lambda3, lambda4, lambda5, lambda6, lambda7):
    
    name = '2HDMC_lambdabasis' 
    templateInput = name + '.in'
# 
#     tempInput  = 'type' + thdmType + '_mH' + Hmass + '_tanB' + tanbeta + '_sinBA' + sinb_a + '_A' + HAMass + '_Hp' + HCMass + '_xs' + higgsType + '.in'
#     tempOutput = 'type' + thdmType + '_mH' + Hmass + '_tanB' + tanbeta + '_sinBA' + sinb_a + '_A' + HAMass + '_Hp' + HCMass + '_xs' + higgsType + '.out'
#     tempLog    = 'type' + thdmType + '_mH' + Hmass + '_tanB' + tanbeta + '_sinBA' + sinb_a + '_A' + HAMass + '_Hp' + HCMass + '_xs' + higgsType + '.log'
# 
#     call('cp ' + templateInput + ' ' + tempInput, shell=True)
#     call("sed -i 's/HMASS/" + Hmass + "/g' " + tempInput, shell=True)
#     call("sed -i 's/TANBETA/" + tanbeta + "/g' " + tempInput, shell=True)
#     call("sed -i 's/SINB_A/" + sinb_a + "/g' " + tempInput, shell=True)
#     call("sed -i 's/THDMTYPE/" + thdmType + "/g' " + tempInput, shell=True)
#     call("sed -i 's/HIGGSTYPE/" + higgsType + "/g' " + tempInput, shell=True)
#     call("sed -i 's/HAMASS/" + HAMass + "/g' " + tempInput, shell=True)
#     call("sed -i 's/HCMASS/" + HCMass + "/g' " + tempInput, shell=True)
#     call("sed -i 's/M12/" + m12 + "/g' " + tempInput, shell=True)
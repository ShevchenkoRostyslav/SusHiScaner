from subprocess import call, Popen, PIPE
import argparse
import time

start_time = time.time()

def ParseOption():

    parser = argparse.ArgumentParser(description='setup for submit')

    parser.add_argument('-m', dest='mass', type=str, help='H mass')
    parser.add_argument('--tanBeta', dest='tanBeta', type=str, help='tanBeta')
    parser.add_argument('--sinB_A', dest='sinB_A', type=str, help='sin(beta-alpha)')
    parser.add_argument('--thdmType', dest='thdm', type=str, help='2hdm type')
    parser.add_argument('--higgsType', dest='higgsType', type=str, help='higgs type, 11 = light Higgs (h), 12 = heavy Higgs (H), 21 = pseudoscalar (A)')
    parser.add_argument('--mA', dest='massA', type=str, help='massA')
    parser.add_argument('--mHp', dest='massHp', type=str, help='massHp')
    parser.add_argument('--m12', dest='m12', type=str, help='m12')

    global args
    args = parser.parse_args()

def runSushi(Hmass, tanbeta, sinb_a, thdmType, higgsType, HAMass, HCMass, m12): #run sushi with multiple mass, tanbeta, sin points, get input from file that submit jobs

    name = '2HDMC_physicalbasis'
    templateInput = name + '.in'

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

ParseOption()
runSushi(args.mass, args.tanBeta, args.sinB_A, args.thdm, args.higgsType, args.massA, args.massHp, args.m12)

print("--- %s seconds ---" % (time.time() - start_time))

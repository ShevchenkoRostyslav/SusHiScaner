#!/usr/bin/python
import argparse
import os, sys
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from setInput import *
import submitter

def reiseAttributeError(list,ref_list):
    for l in list:
        if l not in ref_list:
            raise AttributeError('ERROR: '+ l + ' variable wasn`t provided in setInput.py. Please check spelling')

def checkInputValidity(iput):
    #Method to check whether all variables were properly named and provided
    general_list = ['bais','m12','higgsTypes','thdmTypes','tanBetas']
    physics_basis_list = ['mh','mH','mA','mC','sinB_As','lambda6','lambda7']
    lambda_basis_list = ['lambda1','lambda2','lambda3','lambda4','lambda5','lambda6','lambda7']
    reiseAttributeError(general_list, iput)
    if iput['basis'] == 'physicalbasis': reiseAttributeError(physics_basis_list, iput)
    elif iput['basis'] == 'lambdabasis': reiseAttributeError(lambda_basis_list, iput)
    else : AttributeError('ERROR: program doesn`t work with ' + iput['basis'] + ' yet. Please make a setup for physicalbasis or lambdabasis')

def chooseInput(args):
    logging.debug('I`m in parseInput::chooseInput')
    #Read input from setInput file
    iput = setInputs()
    #check validity of the input
    checkInputValidity(iput)
    #output list
    oput = {}
    #fill output array:
    if( args.submitter == 'physicalbasis'):
        oput = {'basis':args.submitter,
                'm12':args.m12,'higgsTypes':args.higgsType,'thdmTypes':args.thdmType,'tanBetas':args.tanBeta,
                'mh':args.mh,'mH':args.mH,'mA':args.mA,'mC':args.mC,
                'sinB_As':args.sinB_A,
                'lambda6':args.lambda6, 'lambda7':args.lambda7}
    elif( args.submitter == 'lambdabasis'):
        oput = {'basis':args.submitter,
                'm12':args.m12,'higgsTypes':args.higgsType,'thdmTypes':args.thdmType,'tanBetas':args.tanBeta,
                'lambda1':args.lambda1,'lambda2':args.lambda2,'lambda3':args.lambda3,'lambda4':args.lambda4,'lambda5':args.lambda5,
                'lambda6':args.lambda6, 'lambda7':args.lambda7}
    else:
        oput = iput

    if (not 'queue' in oput and args.queue != None): oput['queue'] = args.queue
    if not 'pointsPerJob' in oput: oput['pointsPerJob'] = args.pointsPerJob
    if not 'name' in oput: oput['name'] = args.name
    if args.submitter == 'naf' or args.submitter == 'lxplus': oput['processor'] = args.submitter
    else: oput['processor'] = 'shell'

    return oput

def ParseOption():

    parser = argparse.ArgumentParser(description='submit sushi+2hdmc to lxplus')
    parser.add_argument('-name', dest='name', type=str, help='name of this job, include 2hdm type, submission date/queue')
    parser.add_argument('-v',dest='verbose', help="verbosity level, default - WARNING",default='WARNING',choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-i',dest='input_ini', type=str, help='input SusHi datacard (.ini)',default='../datacards/2HDMC_physicalbasis.in')
    parser.add_argument('-o',dest='ouput_dir', type=str, help='output dir path',default='../output')

    #add subparsers for different basis and run options
    subparsers = parser.add_subparsers(dest='submitter')

    #create parser for the "physicalbasis"
    parser_physbas = subparsers.add_parser('physicalbasis',help='arguments for physical basis')
    parser_physbas.add_argument('--higgsType', dest='higgsType', type=str, help='higgs type, 11 = light Higgs (h), 12 = heavy Higgs (H), 21 = pseudoscalar (A)',default=None)
    parser_physbas.add_argument('--thdmType', dest='thdmType', type=str, help='2hdm type',default=None)
    parser_physbas.add_argument('--tanBeta', dest='tanBeta', type=str, help='tanBeta',default=None)
    parser_physbas.add_argument('--m12', dest='m12', type=str, help='m12' ,default='100')
    parser_physbas.add_argument('--mh',dest='mh',type=str,help='h mass',default='125')
    parser_physbas.add_argument('--mH', dest='mH', type=str, help='H mass',default=None)
    parser_physbas.add_argument('--mA', dest='mA', type=str, help='A mass',default=None)
    parser_physbas.add_argument('--mC', dest='mC', type=str, help='Charge higgs mass',default=None)
    parser_physbas.add_argument('--sinB_A', dest='sinB_A', type=str, help='sin(beta-alpha)',default=None)
    parser_physbas.add_argument('--lambda6', dest='lambda6', type=str, help='lambda6',default='0')
    parser_physbas.add_argument('--lambda7', dest='lambda7', type=str, help='lambda7',default='0')

    #create parser for the 'lambdabasis
    parser_lambdbas = subparsers.add_parser('lambdabasis',help='arguments for lambda basis')
    parser_lambdbas.add_argument('--higgsType', dest='higgsType', type=str, help='higgs type, 11 = light Higgs (h), 12 = heavy Higgs (H), 21 = pseudoscalar (A)',default=None)
    parser_lambdbas.add_argument('--thdmType', dest='thdmType', type=str, help='2hdm type',default=None)
    parser_lambdbas.add_argument('--tanBeta', dest='tanBeta', type=str, help='tanBeta',default=None)
    parser_lambdbas.add_argument('--m12', dest='m12', type=str, help='m12' ,default=None)
    parser_lambdbas.add_argument('--lambda1', dest='lambda1', type=str, help='lambda1',default=None)
    parser_lambdbas.add_argument('--lambda2', dest='lambda2', type=str, help='lambda2',default=None)
    parser_lambdbas.add_argument('--lambda3', dest='lambda3', type=str, help='lambda3',default=None)
    parser_lambdbas.add_argument('--lambda4', dest='lambda4', type=str, help='lambda4',default=None)
    parser_lambdbas.add_argument('--lambda5', dest='lambda5', type=str, help='lambda5',default=None)
    parser_lambdbas.add_argument('--lambda6', dest='lambda6', type=str, help='lambda6',default='0')
    parser_lambdbas.add_argument('--lambda7', dest='lambda7', type=str, help='lambda7',default='0')

    #create parser to run jobs inciated in setinput at lxplus machines
    parser_lxplus = subparsers.add_parser('lxplus',help='arguments to run jobs at lxplus')
    parser_lxplus.add_argument('--q', dest='queue', required=True, type=str, help='submission queue(1nh,8nh,1nd...)',default=None)
    parser_lxplus.add_argument('--n', dest='pointsPerJob', type=int, help='Number of points per job', default=1)

    #create parser to run jobs iniciated in setinput at naf machines
    parser_naf = subparsers.add_parser('naf',help='arguments to run jobs at naf')
    parser_naf.add_argument('--n', dest='pointsPerJob', type=int, help='Number of points per job', default=1)

    args = parser.parse_args()

    return args

def pushInput(args):
    logging.debug('I`m in parseInput::pushInput')
    #Choose inputs: cmd or setInput.py file
    input = chooseInput(args)
    #TODO: develop 'prepareworkdir' and submitter.

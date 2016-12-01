#!/usr/bin/python
import argparse
import os, sys
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from setup import *
from printer import *

def chooseInput(args):
    logging.debug('I`m in parseInput::chooseInput')
    #Read input Basis from setInput file
    iput = setInputs()
    #output array of Basis
    oput = []
    #fill output array:
    if( args.submitter == 'physicalbasis'):
        dic = {'basis':args.submitter,
                'm12':args.m12,'higgsType':args.higgsType,'thdmType':args.thdmType,'tanBeta':args.tanBeta,
                'mh':args.mh,'mH':args.mH,'mA':args.mA,'mC':args.mC,
                'sinB_A':args.sinB_A,
                'lambda6':args.lambda6, 'lambda7':args.lambda7}
        args.submitter = 'shell'
        oput.append(Basis.choose_basis(dic))
    elif( args.submitter == 'lambdabasis'):
        dic = {'basis':args.submitter,
                'm12':args.m12,'higgsType':args.higgsType,'thdmType':args.thdmType,'tanBeta':args.tanBeta,
                'lambda1':args.lambda1,'lambda2':args.lambda2,'lambda3':args.lambda3,'lambda4':args.lambda4,'lambda5':args.lambda5,
                'lambda6':args.lambda6, 'lambda7':args.lambda7}
        args.submitter = 'shell'
        oput.append(Basis.choose_basis(dic))
    else:
        oput = iput

    return oput

def ParseOption():

    parser = argparse.ArgumentParser(description='submit sushi+2hdmc to lxplus')
    parser.add_argument('-name', dest='name', type=str, help='name of this job, include 2hdm type, submission date/queue')
    parser.add_argument('-v',dest='verbose', help="verbosity level, default - WARNING",default='WARNING',choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('-i',dest='input_ini', type=str, help='input SusHi datacard (.ini)',default='datacards/2HDMC_physicalbasis.in')
    parser.add_argument('-o,output_dir',dest='output_dir', type=str, help='output dir path',default='output')
    parser.add_argument('-r,resubmit',dest='resubmit',action='store_true',help='if specified - resubmission of job will be done')

    #add subparsers for different basis and run options
    subparsers = parser.add_subparsers(dest='submitter')

    #create parser for the "physicalbasis"
    parser_physbas = subparsers.add_parser('physicalbasis',help='arguments for physical basis')
    parser_physbas.add_argument('--higgsType', dest='higgsType',required=True, type=int, help='higgs type, 11 = light Higgs (h), 12 = heavy Higgs (H), 21 = pseudoscalar (A)',default=None)
    parser_physbas.add_argument('--thdmType', dest='thdmType', required=True, type=int, help='2hdm type',default=None)
    parser_physbas.add_argument('--tanBeta', dest='tanBeta', required=True, type=float, help='tanBeta',default=None)
    parser_physbas.add_argument('--m12', dest='m12', type=float, help='m12' ,default=100)
    parser_physbas.add_argument('--mh',dest='mh',type=float,help='h mass',default=125)
    parser_physbas.add_argument('--mH', dest='mH', required=True, type=float, help='H mass',default=None)
    parser_physbas.add_argument('--mA', dest='mA', required=True, type=float, help='A mass',default=None)
    parser_physbas.add_argument('--mC', dest='mC', required=True, type=float, help='Charge higgs mass',default=None)
    parser_physbas.add_argument('--sinB_A', dest='sinB_A', required=True, type=float, help='sin(beta-alpha)',default=None)
    parser_physbas.add_argument('--lambda6', dest='lambda6', type=float, help='lambda6',default=0)
    parser_physbas.add_argument('--lambda7', dest='lambda7', type=float, help='lambda7',default=0)

    #create parser for the 'lambdabasis
    parser_lambdbas = subparsers.add_parser('lambdabasis',help='arguments for lambda basis')
    parser_lambdbas.add_argument('--higgsType', dest='higgsType', required=True, type=int, help='higgs type, 11 = light Higgs (h), 12 = heavy Higgs (H), 21 = pseudoscalar (A)',default=None)
    parser_lambdbas.add_argument('--thdmType', dest='thdmType', required=True, type=int, help='2hdm type',default=None)
    parser_lambdbas.add_argument('--tanBeta', dest='tanBeta', required=True, type=float, help='tanBeta',default=None)
    parser_lambdbas.add_argument('--m12', dest='m12', required=True, type=float, help='m12' ,default=100)
    parser_lambdbas.add_argument('--lambda1', dest='lambda1', required=True, type=float, help='lambda1',default=None)
    parser_lambdbas.add_argument('--lambda2', dest='lambda2', required=True, type=float, help='lambda2',default=None)
    parser_lambdbas.add_argument('--lambda3', dest='lambda3', required=True, type=float, help='lambda3',default=None)
    parser_lambdbas.add_argument('--lambda4', dest='lambda4', required=True, type=float, help='lambda4',default=None)
    parser_lambdbas.add_argument('--lambda5', dest='lambda5', required=True, type=float, help='lambda5',default=None)
    parser_lambdbas.add_argument('--lambda6', dest='lambda6', type=float, help='lambda6',default=0)
    parser_lambdbas.add_argument('--lambda7', dest='lambda7', type=float, help='lambda7',default=0)

    #create parser to run jobs inciated in setinput at lxplus machines
    parser_lxplus = subparsers.add_parser('lxplus',help='arguments to run jobs at lxplus')
    parser_lxplus.add_argument('--q', dest='queue', required=True, type=int, help='submission queue(1nh,8nh,1nd...)')
    parser_lxplus.add_argument('--n', dest='pointsPerJob', type=int, help='Number of points per job', default=1)
    parser_lxplus.add_argument('-d,dir_to_resubmit',  dest='JobDirToResubmit',type=str, help='Job directory to resubmit',default=None)
    parser_lxplus.add_argument('--submission_pars', dest='submission_pars',type=str,help='Parameters that will be used with bsub',default=None)

    #create parser to run jobs iniciated in setinput at naf machines
    parser_naf = subparsers.add_parser('naf',help='arguments to run jobs at naf')
    parser_naf.add_argument('--n', dest='pointsPerJob', type=int, help='Number of points per job', default=1)
    parser_naf.add_argument('-d,dir_to_resubmit',  dest='JobDirToResubmit',type=str, help='Job directory to resubmit',default=None)
    parser_naf.add_argument('--submission_pars', dest='submission_pars',type=str,help='Parameters that will be used with bsub',default='-cwd -V -l h_rt=24:00:00 -l h_vmem=4G')

    args = parser.parse_args()
    # convert output_dir to absolute path
    args.output_dir = os.path.abspath(os.path.join(os.getcwd(), args.output_dir))
    # convert dir for resubmission to absolute path if specified
    if not args.JobDirToResubmit == None:
        args.JobDirToResubmit = os.path.abspath(os.path.join(os.getcwd(), args.JobDirToResubmit)) + '/'
    # Add folder to the output
    args.output_dir += '/sushi_out/'

    return args

def pushInput(args):
    logging.debug('I`m in parseInput::pushInput')
    #Choose inputs: cmd or setInput.py file
    input = chooseInput(args)
    # Use printer to show the input
    printInput(input, args)
    # return input that will be used
    return input;

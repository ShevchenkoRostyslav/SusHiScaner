#!/usr/bin/python

'''Class for submission jobs to naf/lxplus/shell

'''

import sys, os, commands
import logging
from subprocess import call,Popen
import uuid
from tools import *
from shutil import copyfile
import fileinput

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../' # full path of ROOT folder


class submitter(object):
    def __init__(self,type,command = '',parameters = ''):
        self.type = type
        self._command = command
        self._parameters = parameters

    def choose_cluster(type,parameters = ''):
        if type == 'naf':
            return naf(parameters)
        elif type == 'lxplus':
            return lxplus(parameters)
        elif type == 'shell':
            return shell(parameters)
        assert 0, 'Wrong cluster selected: ' + type
    choose_cluster = staticmethod(choose_cluster)

    def submit(self,cmd_args,basis_arr):
        """The main method.

        Used to submit jobs to naf/lxplus/shell use private methods that
        are overwritten in the derived classes
        """
        #check whether output exists:
        if not os.path.exists(cmd_args.output_dir):
            os.makedirs(cmd_args.output_dir)
        os.chdir(cmd_args.output_dir)

        # Count number of processed points:
        points = 0
        # Loop over the basises
        for basis in basis_arr:
            job = int(points/cmd_args.pointsPerJob) + 1

            if( self._StartNewJob(points, cmd_args.pointsPerJob) or points == 0):
                out_csh = self.PrepareWorkDir(job,basis)

            self.AddOnePoint(job, basis, out_csh)
            if( self._StartNewJob(points+1, cmd_args.pointsPerJob) or points == len(basis_arr) - 1):
                # Delete output of the 2HDMC
                command3 = 'rm 2HDMC.out'
                out_csh.write(command3 + '\n')
                self.SubmitJob('job_' + str(job))
                out_csh.close()

            points += 1

        print 'Submission DONE!'

    def PrepareWorkDir(self,job,par_set):
        """Method used to prepare working directory for farm usage.

        Also .csh scripts and datacards.in are prepared
        """

        root_dir = os.getcwd()
        # clear directory with the same name
        MakeCleanDir('job_' + str(job))
        os.chdir('job_' + str(job))#go to job_i

        # copy binary
        self.CopyFile(ROOT_DIR + 'bin', '.', 'sushi')
        # copy template .in file
        self.CopyFile(ROOT_DIR + 'datacards','.','2HDMC_' + str(par_set.basis) + '.in')

        #prepare new csh file to run at the farm
        newCsh = 'job_'+str(job)+'.csh'
        outCsh = open(newCsh, 'w')
        outCsh.write('#!/bin/csh' + '\n')
        # Add permissions to the .csh file
        MakeFileExecutable(newCsh)

        job_dir = os.getcwd()
        command1 = 'cd ' + job_dir
        outCsh.write(command1 + "\n")
        # Get back to the parent directory:
        os.chdir(root_dir)

        return outCsh

    def AddOnePoint(self, job, par_set, out_csh):
        """Method that doesn't create a directory but modify the csh.

        """
        root_dir = os.getcwd()
        # Change directory
        os.chdir('job_' + str(object=job))
        # Modify datacard with current set of parameters
        card_name = self._UpdateDataCard(par_set)
        # Check whether csh script exists:
        if not os.path.exists(out_csh.name):
            raise AttributeError("ERROR: No .csh file found at " + os.getcwd())
        command = './sushi ' + card_name + '.in ' + card_name + '.out' + ' > ' + card_name + '.log'
        out_csh.write(command + '\n')
        # Cat 2HDMC output in the same .out
        command2 = 'cat 2HDMC.out >> ' + card_name + '.out'
        out_csh.write(command2 + '\n')
        # Delete output of the 2HDMC:
        # command3 = 'rm 2HDMC.out'
        # out_csh.write(command3 + '\n')
        # Get back to the parent directory:
        os.chdir(root_dir)

    def _StartNewJob(self,points, pointsPerJob):
        """Private method to Check whether a folder for new job should be created.

        """
        flag = False
        if (points)%pointsPerJob == 0:
            flag = True
        return flag

    def SubmitJob(self, job_dir):
        """Method to submit single job by job_dir.

        """
        root_dir = os.getcwd()
        # Get base_dir name:
        base_dir_name = os.path.basename(os.path.relpath(job_dir))
        # Change directory
        os.chdir(job_dir)
        thisCsh = base_dir_name + '.csh'
        cmd = self._command + ' ' + self._parameters + ' ' + thisCsh
        # print 'cmd: ' + cmd
        proc = Popen(cmd,shell=True)
        # Get back to the parent directory:
        os.chdir(root_dir)

    # def SubmitJob(self, job=10000000):
    #     """Method to submit single job by job_id.
    #
    #     """
    #     self.SubmitJob('job_' + str(job))

    def processCmd(cmd, quite = 0):
        """Method to process cmd command for submission.

        """
        status, output = commands.getstatusoutput(cmd)
        if (status !=0 and not quite):
            print 'Error in processing command:\n   ['+cmd+']'
            print 'Output:\n   ['+output+'] \n'

    def CopyFile(self,oldLoc, newLoc, oldName, newName = ''):
        """Method to copy file from one directory to another.

        """
        #check whether directory exists
        if not os.path.exists(oldLoc):
            raise AttributeError("ERROR: Location " + oldLoc + " doens't exist. Please check spelling")

        # check if it's end with '/'
        if not oldLoc.endswith('/'):
            oldLoc += '/'

        #check whether input file exist:
        if not os.path.exists(oldLoc+oldName):
            raise AttributeError("ERROR: File " + oldName + " doens't exist at " + oldLoc + ". Please check spelling")

        # check whether new directory exists
        if not os.path.exists(newLoc):
            raise AttributeError("ERROR: Location " + newLoc + " doens't exist. Please check spelling")

        if not newLoc.endswith('/'):
            newLoc += '/'

        # check whether newName should be the same as old Name:
        if newName == '': newName = oldName

        #copy file:
        # copyfile(oldLoc + oldName, newLoc + newName) #doesn't work because permissions to the file are not coppied :(
        call('cp ' + oldLoc + oldName + ' ' + newLoc + newName, shell=True)

    def _UpdateDataCard(self,basis):
        """Methods to update the datacard with current configuration with physical basis.

        """
        if basis.basis == 'physicalbasis':
            temp_name = self._UpdatePhysicalbasisDataCard(basis.higgsType, basis.thdmType, basis.tanBeta, basis.m12, basis.mh, basis.mH, basis.mA, basis.mC, basis.sinB_A, basis.lambda6, basis.lambda7)
        elif basis.basis == 'lambdabasis':
            temp_name = self._UpdateLambdabasisDataCard(basis.higgsType, basis.thdmType, basis.tanBeta, basis.m12, basis.lambda1, basis.lambda2, basis.lambda3, basis.lambda4, basis.lambda5, basis.lambda6, basis.lambda7)
        return temp_name

    def _UpdatePhysicalbasisDataCard(self,higgsType,thdmType,tanBeta,m12,mh,mH,mA,mC,sinB_A,lambda6,lambda7):
        # Input data card
        name = '2HDMC_physicalbasis'
        templateInput = name + '.in'

        # Redefine the name of the input datacard and output
        tempInputName = 'type' + str(int(thdmType)) + '_Htype_' + str(int(higgsType)) + '_' + str(object=uuid.uuid1()) #Couldn't use meaningfull name because of limitation on the string size fomr sushi side
        tempInput = tempInputName + '.in';

        # Check whether input datacard exists:
        if not os.path.exists(templateInput): raise BaseException('ERROR:PROBLEM in submitter::_UpdatePhysicalbasisDataCard - wrong dir')

        # Copy initial.in file to new name and replace strings line-by-line
        with open(templateInput) as infile, open(tempInput, 'w') as outfile:
            for line in infile:
                line = line.replace('HLOWM', str(mh))
                line = line.replace('HCAPM', str(mH))
                line = line.replace('HAMASS', str(mA))
                line = line.replace('HCMASS', str(mC))
                line = line.replace('SINB_A', str(sinB_A))
                line = line.replace('L6', str(lambda6))
                line = line.replace('L7', str(lambda7))
                line = line.replace('THDMTYPE', str(thdmType))
                line = line.replace('HIGGSTYPE', str(higgsType))
                line = line.replace('TANBETA', str(tanBeta))
                line = line.replace('M12', str(m12))
                outfile.write(line)

        return tempInputName

    def _UpdateLambdabasisDataCard(self,higgsType,thdmType,tanBeta,m12,lambda1,lambda2,lambda3,lambda4,lambda5,lambda6,lambda7):
        """with lambda basis.

        """
        # Input data card
        name = '2HDMC_lambdabasis'
        templateInput = name + '.in'

        # Redefine the name of the input datacard and output
        tempInputName = 'type' + str(int(thdmType)) + '_Htype_' + str(int(higgsType)) + '_' + str(object=uuid.uuid1())
        tempInput = tempInputName + '.in';

        # Check whether input datacard exists:
        if not os.path.exists(templateInput): raise BaseException('ERROR:PROBLEM in submitter::_UpdateLambdabasisDataCard - wrong dir')

        # Copy initial.in file to new name and replace strings line-by-line
        with open(templateInput) as infile, open(tempInput, 'w') as outfile:
            for line in infile:
                line = line.replace('L1', str(lambda1))
                line = line.replace('L2', str(lambda2))
                line = line.replace('L3', str(lambda3))
                line = line.replace('L4', str(lambda4))
                line = line.replace('L5', str(lambda5))
                line = line.replace('L6', str(lambda6))
                line = line.replace('L7', str(lambda7))
                line = line.replace('THDMTYPE', str(thdmType))
                line = line.replace('HIGGSTYPE', str(higgsType))
                line = line.replace('TANBETA', str(tanBeta))
                line = line.replace('M12', str(m12))
                outfile.write(line)

        return tempInputName

class naf(submitter):
    def __init__(self,parameters = "-cwd -V"):
        submitter.__init__(self,'naf',"qsub",parameters)
        self._parameters = parameters

    def __str__(self):
        return 'Naf: ' + self._command + self._parameters


class lxplus(submitter):
    def __init__(self,parameters = "-cwd -V"):
        # TODO: test lxplus version!!!!!
        submitter.__init__(self,'lxplus',"bsub",parameters)
        self._parameters = parameters

    def __str__(self):
        return 'lxplus used for submission'

class shell(submitter):
    def __init__(self):
        submitter.__init__(self,'shell')

    def __str__(self):
        return 'shell used for submission'

    # Redefine submit method
    def submit(self,cmd_args,basis_arr):
        #check whether output exists:
        if not os.path.exists(cmd_args.output_dir):
            os.makedirs(cmd_args.output_dir)
        os.chdir(cmd_args.output_dir)

        # copy binary
        self.CopyFile(ROOT_DIR + 'bin', '.', 'sushi')
        # Copy new datacard
        self.CopyFile(ROOT_DIR + 'datacards','.','2HDMC_' + str(basis_arr[0].basis) + '.in')
        # Modify datacard with current set of parameters
        card_name = self._UpdateDataCard(basis_arr[0])
        # Run sushi
        command = './sushi ' + card_name + '.in ' + card_name + '.out' + ' > ' + card_name + '.log'
        call(command,shell=True)

        print 'Submission DONE!'

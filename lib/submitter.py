#!/usr/bin/python

'''Class for submission jobs to naf/lxplus/shell

'''

import sys, os, commands
from subprocess import call,Popen
import uuid
from tools import *

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../' # full path to ROOT folder


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
            return shell()
        elif type == 'condor':
            return condor(parameters)
        assert 0, 'Wrong cluster selected: ' + type
    choose_cluster = staticmethod(choose_cluster)

    def submit(self,cmd_args,basis_arr):
        """The main method.

        Used to submit jobs to naf/lxplus/shell use private methods that
        are overwritten in the derived classes
        """
        # Make clean directory
        MakeCleanDir(cmd_args.output_dir)
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
                # Tar the ini files:
                self._TarIniFiles(job)
                # Tar the output files:
                self._TarOutFiles(out_csh,job,cmd_args.output_dir)
                # Submit current job
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
        self._UpdateCshFile(outCsh, '#!/bin/csh')
        # Work with tars:
        # Block if run is not local:
        if '-cwd' not in self._parameters:
            # Copy tar
            self._UpdateCshFile(outCsh,'cp ' + root_dir + '/in_' + str(job) + '.tgz .')
            # Untar
            self._UpdateCshFile(outCsh,'tar zxvf in_' + str(job) + '.tgz')
            # chdir
            self._UpdateCshFile(outCsh,'cd job_' + str(job))
        # clean dir
        self._UpdateCshFile(outCsh,'rm *.out *.log')
        # Add permissions to the .csh file
        MakeFileExecutable(newCsh)
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
        self._UpdateCshFile(out_csh, './sushi ' + card_name + '.in ' + card_name + '.out') # + ' > ' + card_name + '.log') #TODO: don't froget to switch on this
        # Cat 2HDMC output in the same .out
        self._UpdateCshFile(out_csh,'cat 2HDMC.out >> ' + card_name + '.out')
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
        """Methods to update the datacard with current configuration according to basis.

        """
        if basis.basis == 'physicalbasis':
            temp_name = self._UpdatePhysicalbasisDataCard(basis)
        elif basis.basis == 'lambdabasis':
            temp_name = self._UpdateLambdabasisDataCard(basis)
        return temp_name

    def _UpdatePhysicalbasisDataCard(self,basis):
        """Methods to update the datacard with current configuration with physical basis.

        """
        # Input data card
        name = '2HDMC_physicalbasis'
        templateInput = name + '.in'

        # Redefine the name of the input datacard and output
        tempInputName = 'type' + str(int(basis.thdmType)) + '_Htype_' + str(int(basis.higgsType)) + '_' + str(object=uuid.uuid1()) #Couldn't use meaningfull name because of limitation on the string size fomr sushi side
        tempInput = tempInputName + '.in';

        # Check whether input datacard exists:
        if not os.path.exists(templateInput): raise BaseException('ERROR:PROBLEM in submitter::_UpdatePhysicalbasisDataCard - wrong dir')

        # Copy initial.in file to new name and replace strings line-by-line
        with open(templateInput) as infile, open(tempInput, 'w') as outfile:
            for line in infile:
                line = line.replace('HLOWM', str(basis.mh))
                line = line.replace('HCAPM', str(basis.mH))
                line = line.replace('HAMASS', str(basis.mA))
                line = line.replace('HCMASS', str(basis.mC))
                line = line.replace('SINB_A', str(basis.sinB_A))
                line = line.replace('L6', str(basis.lambda6))
                line = line.replace('L7', str(basis.lambda7))
                line = line.replace('THDMTYPE', str(basis.thdmType))
                line = line.replace('HIGGSTYPE', str(basis.higgsType))
                line = line.replace('TANBETA', str(basis.tanBeta))
                line = line.replace('M12', str(basis.m12))
                outfile.write(line)

        return tempInputName

    def _UpdateLambdabasisDataCard(self,basis):
        """Methods to update the datacard with current configuration with lambda basis.

        """
        # Input data card
        name = '2HDMC_lambdabasis'
        templateInput = name + '.in'

        # Redefine the name of the input datacard and output
        tempInputName = 'type' + str(int(basis.thdmType)) + '_Htype_' + str(int(basis.higgsType)) + '_' + str(object=uuid.uuid1())
        tempInput = tempInputName + '.in';

        # Check whether input datacard exists:
        if not os.path.exists(templateInput): raise BaseException('ERROR:PROBLEM in submitter::_UpdateLambdabasisDataCard - wrong dir')

        # Copy initial.in file to new name and replace strings line-by-line
        with open(templateInput) as infile, open(tempInput, 'w') as outfile:
            for line in infile:
                line = line.replace('L1', str(basis.lambda1))
                line = line.replace('L2', str(basis.lambda2))
                line = line.replace('L3', str(basis.lambda3))
                line = line.replace('L4', str(basis.lambda4))
                line = line.replace('L5', str(basis.lambda5))
                line = line.replace('L6', str(basis.lambda6))
                line = line.replace('L7', str(basis.lambda7))
                line = line.replace('THDMTYPE', str(basis.thdmType))
                line = line.replace('HIGGSTYPE', str(basis.higgsType))
                line = line.replace('TANBETA', str(basis.tanBeta))
                line = line.replace('M12', str(basis.m12))
                outfile.write(line)

        return tempInputName

    def _UpdateCshFile(self,csh_file,what):
        """Method to update .csh file.

        """
        csh_file.write(str(what)+'\n')

    def _TarIniFiles(self,job):
        """Method to tar ini files.

        """
        call('tar czf in_' + str(job) + '.tgz job_' + str(job) + '/*.in job_' + str(job) + '/sushi',shell=True)

    def _TarOutFiles(self,out_csh,job,output_dir):
        """Method to tar out files.

        """
        # Delete output of the 2HDMC
        self._UpdateCshFile(out_csh,'rm 2HDMC.out')
        # Tar the output
        self._UpdateCshFile(out_csh,'tar czf out_' + str(job) + '.tgz *.out *.log')
        # Copy results
        if not '-cwd' in self._parameters:
            self._UpdateCshFile(out_csh,'mv out_' + str(job) + '.tgz ' + output_dir + 'job_' + str(job) + '/.')
        # clean *in files
        self._UpdateCshFile(out_csh, 'rm ' + output_dir + 'in_' + str(job) + '.tgz')

class naf(submitter):
    def __init__(self,parameters = " -V"):
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

class condor(submitter):
    def __init__(self,parameters = "-V"):
        submitter.__init__(self,'condor',"condor_submit",parameters)
        self._parameters = parameters

    def __str__(self):
        return 'condor used for submission'

    # Redefine submit file
    def SubmitJob(self, job_dir):
        """Method to submit single job by job_dir.

        """
        root_dir = os.getcwd()
        # Get base_dir name:
        base_dir_name = os.path.basename(os.path.relpath(job_dir))
        # Change directory
        os.chdir(job_dir)
        thisCsh = base_dir_name + '.csh'
        # create and modify condor submission file:
        condor_sub_file_name = self._createSubmitionFile(root_dir,root_dir + "/" + job_dir,base_dir_name)
        #self._modifySubmitionFile(condor_sub_file_name,base_dir_name)
        # command to submit
        cmd = self._command + ' ' + self._parameters + ' ' + condor_sub_file_name
        # print 'cmd: ' + cmd
        print(cmd)
        proc = Popen(cmd,shell=True)
        # Get back to the parent directory:
        os.chdir(root_dir)

    def _createSubmitionFile(self,root_dir,job_dir,job_name):
        """Method to create .sub condor fileself.

        """
        # template file
        temp_file_name = "condor_submit_template.sub"

        # output submission file Name
        out_sub = "condor_submit_" + job_name + ".sub"
        #copy template file to the job directory
        #self.CopyFile(root_dir + "/../../input/",job_dir,temp_file_name,out_sub)
        with open(root_dir + "/../../input/" + temp_file_name,'r') as f_in:
            with open(job_dir + '/' + out_sub,'w') as f_out:
                for line in f_in:
                    n_line = line.replace("$EXE_NAME$",job_name)
                    if "$LD_LIBRARY_PATH$" in line :
                        n_line = line.replace("$LD_LIBRARY_PATH$",os.getenv("LD_LIBRARY_PATH"))
                    f_out.write(n_line)

        return out_sub

    def _modifySubmitionFile(self,file_name,job_name):
        """Method to modify submission file according to parameters.

        """
        with open(file_name,'r') as f:
            txt = f.read().replace("$EXE_NAME$",job_name)

        with open(file_name,'w') as f:
            f.write(txt)


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
        #run sushi
        command = './sushi ' + card_name + '.in ' + card_name + '.out' + ' > ' + card_name + '.log'
        call(command,shell=True)

#!/usr/bin/python
import os
import glob
from subprocess import call
from tools import *
from getInfoFromSusHiOutput import *

# Module to untar output of submission to one place
def untarSusHiOutput(output_dir):
    # Check whether directory exists
    if not os.path.exists(output_dir):
        raise AttributeError("ERROR: Wrong dir name " + output_dir + " was provided to tools::untarSusHiOutput")
    # Create folder for untar files:
    MakeCleanDir(output_dir + '/Untar_files/')

    # Check the output_dir
    if len(glob.glob(output_dir + 'sushi_out/job_*')) == 0:
        raise AttributeError("ERROR: Wrong dir name " + output_dir + " was provided to tools::untarSusHiOutput")
    # Iterate through the job_i folders from SusHi output
    for job in glob.glob(output_dir + 'sushi_out/job_*'):
        # use only the name of the folder
        job_i = os.path.basename(os.path.normpath(job))
        # tar name
        tar = job + '/out_' + job_i + '.tar.gz'
        if not os.path.exists(tar):
            raise AttributeError("ERROR: No .tar.gz file at " + tar)
        # Only through folders with 'job_i'
        untar_dir = output_dir + '/Untar_files/' + job_i
        os.makedirs(untar_dir)
        # Untar
        call('tar -xvzf ' + tar + ' -C ' + untar_dir,shell=True)

# Module to make readable txt file
def makeReadableGrid(output_dir):
    # higgsType and 2HDM types
    higgsType = ['A', 'h', 'H', 'extra']
    types2HDM = ['type1', 'type2','type3','type4']
    # create directory for txt files:
    txtDir = MakeCleanDir(output_dir + '/txtFiles/')
    # and for root files
    rootDir = MakeCleanDir(output_dir + '/rootFiles/')
    for higgs in higgsType:
        for type2HDM in types2HDM:
            getInfoFromSusHiOutput(output_dir + '/Untar_files/',output_dir,type2HDM,higgs)

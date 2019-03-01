#!/usr/bin/env python
"""Module to check submission output.

   Submission output should be checked for existance and completeness
"""

import os,sys
import glob
import warnings
from printer import UserDecision

__author__ = "Rostyslav Shevchenko"
__maintainer__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"

def CheckBriefLog(input_dir):
    """Method to check the overall status of the output.

       This method shows the overall status of the output, in particular -
       number of the points that was correctly processed (not zero output)
       in comparison to the total number of submitted points.
    """
    total_not_empty_outs = 0
    total_ins = 0
    # Loop over all directories
    for i_dir in glob.glob(input_dir + 'job*'):
        # Add all *in files to get the total amount of in files
        total_ins += len(glob.glob(i_dir + '/*.in')) - 1
        for i_out in glob.glob(i_dir + '/*.out'):
            # Get number of outputs
            if '2HDMC' not in i_out and os.stat(i_out).st_size != 0:
                total_not_empty_outs += 1
    # Print the log message
    print('Number of .in files: ' + str(total_ins) + ', number of .out files: ' + str(total_not_empty_outs))
    # Make decision:
    if total_ins != total_not_empty_outs:
        return UserDecision('Continue without this files (y) or see more detailed output (n): `y` or `n` ')
    else:
        return True

def CheckIfDirExists(input_dir):
    """Method to check whether directory exists.

       Raise error if not.
    """
    if not os.path.exists(input_dir):
        raise AttributeError('Provided folder: ' + input_dir + ' doesn`t exist')

def ShowSingleLog(input_file):
    """Method to show log of a particular file.

    """
    # Check file extension
    filename, file_extension = os.path.splitext(input_file)
    if not file_extension == '.log':
        file_extension = '.log'
    # Form file_name again
    input_file = filename + file_extension
    if not os.path.exists(input_file):
        warnings.warn('No log file ' + input_file + ' has been found.')
    else:
        with open(file_name[0], mode='r', buffering=None) as fin:
            print fin.read(size=None)

def CheckOutSize(input_dir):
    """Method to check whether .out files are not empty.

    """
    number_of_failed_files = 0
    for out_file in glob.glob(input_dir + "*.out"):
        if os.stat(out_file).st_size == 0:
            number_of_failed_files += 1
    # Raise warning
    if number_of_failed_files == 0: return
    warnings.warn('In ' + input_dir + ' ' + str(number_of_failed_files) + ' output files from ' + str(len(glob.glob(input_dir + "*.out"))) + ' are empty')
    # Ask whether user wants to delete this files and continue
    if UserDecision('Continue without this files? Empty files will be deleted. Please type `y` or `n` '):
        for out_file in glob.glob(input_dir + "*.out"):
            if os.stat(out_file).st_size == 0:
                os.remove(out_file)
    else:
        sys.exit()

def CheckNoutEqualToNin(input_dir):
    """Method to check whether number of *.out files are equal to *.in.

    """
    if len(glob.glob(input_dir + "*.out")) != (len(glob.glob(input_dir + "*.in")) - 1): # -1 for template_basis.in
        warnings.warn( str(len(glob.glob(input_dir + "*.out"))) + ' files were processed instead of ' + str(len(glob.glob(input_dir + "*.in")) - 1) + ' in ' + input_dir + '\n')
        if not UserDecision('Continue without this files? Please type `y` or `n` '):
            sys.exit()
        # TODO resubmission should be asked here as well!


def CheckIfOutExists(input_dir):
    """Method to check whether .out files exists.

    """
    if len(glob.glob(input_dir + "*.out")) == 0:
        raise EnvironmentError('No output files in ' + input_dir + '. Check .e* for more details.')

def CheckIfCshExists(job_dir):
    """Method to check whether .csh file exists.

    """
    # Check whether right dir was provided:
    CheckIfDirExists(job_dir)
    # Check if .csh file is inside
    file_name = job_dir + '/' + os.path.basename(os.path.relpath(job_dir))
    if not os.path.exists(file_name + '.csh') and not os.path.exists(file_name + '.sh'):
        raise AttributeError('Provided folder: ' + job_dir + ' doesn`t contain .csh file: ' + file_name)

def CheckSubmissionDir(input_dir):
    """Function to check files in a single job dir

    """
    # Check whether .csh file exists inside
    CheckIfCshExists(input_dir)
    # First check whether any of .out exists:
    CheckIfOutExists(input_dir)
    # Check whether number of .out is equal to .in
    CheckNoutEqualToNin(input_dir)
    # Check whether .out are empty or not
    CheckOutSize(input_dir)

def CheckSubmissionOutput(input_dir):
    """Main function to check submission output.

    """
    print 'Check output...'
    # Check whether input_dir exists:
    CheckIfDirExists(input_dir)
    # Check if we are in correct folder
    if(len(glob.glob(input_dir + 'job*')) == 0):
        raise AttributeError('No job* folders in ' + input_dir)
    # Make brief overview:
    if CheckBriefLog(input_dir): return
    # Start loop over the DIRs with ouput of the SusHi
    for i_dir in glob.glob(input_dir + 'job*'):
        CheckSubmissionDir(i_dir + '/')

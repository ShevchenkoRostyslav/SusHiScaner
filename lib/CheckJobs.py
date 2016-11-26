#!/usr/bin/env python
"""Module to check submission output.

   Submission output should be checked for existance and completeness
"""

import os
import glob
import warnings
from printer import UserDecision

__author__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"

def CheckOutSize(input_dir):
    """Method to check whether .out files are not empty.

    """
    number_of_failed_files = 0
    for out_file in glob.glob(input_dir + "*.out"):
        if os.stat(out_file).st_size == 0:
            number_of_failed_files += 1
    # Raise warning
    warnings.warn(number_of_failed_files + ' output files from' + len(glob.glob(input_dir + "*.out")) + ' are empty', category=None, stacklevel=1)
    if printer.UserDecision('Continue without this files? Empty files will be deleted. Please type `y` or `n`'):
        for out_file in glob.glob(input_dir + "*.out"):
            if os.stat(out_file).st_size == 0:
                os.remove(out_file)

def CheckNoutEqualToNin(input_dir):
    """Method to check whether number of *.out files are equal to *.in.

    """
    if len(glob.glob(input_dir + "*.out")) != (len(glob.glob(input_dir + "*.in")) - 1): # -1 for template_basis.in
        warnings.warn(len(glob.glob(input_dir + "*.out")) + ' files were processed instead of ' + len(glob.glob(input_dir + "*.in")) - 1 + ' in ' + input_dir + '\n' \
        , category=None, stacklevel=1)
        printer.UserDecision('Continue without this files? Please type `y` or `n`')
        # TODO resubmission should be asked here as well!


def CheckIfOutExists(input_dir):
    """Method to check whether .out files exists.

    """
    if len(glob.glob(input_dir + "*.out")) == 0:
        raise EnvironmentError('No output fiels in ' + input_dir + '. Check .e* for more details.')

def CheckSubmissionDir(input_dir):
    """Function to check files in a single job dir

    """
    # First check whether any of .out exists:
    CheckIfOutExists(input_dir)
    # Check whether number of .out is equal to .in
    CheckNoutEqualToNin(input_dir)
    # Check whether .out are empty or not
    CheckOutSize(input_dir)


def CheckSubmissionOutput(input_dir):
    """Main function to check submission output.

    """
    # Check whether input_dir exists:
    if not os.path.exists(input_dir):
        raise AttributeError("ERROR: Folder " + input_dir + " doesn't exist")
    # Start loop over the DIRs with ouput of the SusHi
    for i_dir in glob.glob(input_dir + 'job*'):
        CheckSubmissionDir(i_dir)

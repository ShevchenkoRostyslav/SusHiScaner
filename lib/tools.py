#!/usr/bin/python

"""Module with usefull tools

"""

import os
import shutil # for rmtree function
import stat

__author__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"

# Get absolute path to the file/dir
def getAbsPath(path_to_file):
    return os.path.abspath(os.path.join(os.getcwd(), path_to_file))

# If directory exist - remove and create new
def MakeCleanDir(path_to_dir):
    if os.path.exists(path_to_dir):
        shutil.rmtree(path_to_dir)
        # create new one
    os.makedirs(path_to_dir)
    # return the path
    return path_to_dir

def MakeFileExecutable(path_to_file):
    st = os.stat(path_to_file)
    os.chmod(path_to_file, st.st_mode | stat.S_IEXEC)

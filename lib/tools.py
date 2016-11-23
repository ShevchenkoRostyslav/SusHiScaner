#!/usr/bin/python
import os
import shutil # for rmtree function

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

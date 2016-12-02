#!/usr/bin/python
import argparse
from lib.tools import *
from lib.getInfoFromSusHiOutput import *
from lib.CheckJobs import *

# read output of thw submission --> input for post-processing
def ParseOption():
    parser = argparse.ArgumentParser(description='Convert the output of the sushi+2HDMC to .root + .txt format')
    parser.add_argument('-i',       dest='input_dir', type=str, help='path with output of the submission tool')
    parser.add_argument('--check_output',dest='check_output', action=True, help='If used - output of the SusHi will be checked')
    args = parser.parse_args()
    # convert input to absolute path
    args.input_dir  = getAbsPath(args.input_dir) + '/'
    return args

if __name__ == '__main__':
    # Read user input:
    cmd_args = ParseOption()
    # First - check jobs if required:
    if(cmd_args.check_output):
        CheckSubmissionOutput(cmd_args.input_dir + 'sushi_out/')
    # make .txt and .root files
    makeReadableGrid(cmd_args.input_dir)

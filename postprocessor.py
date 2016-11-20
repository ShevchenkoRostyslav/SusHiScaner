#!/usr/bin/python
import argparse
from lib.tools import *
from lib.makeReadableGrid import *

# read output of thw submission --> input for post-processing
def ParseOption():
    parser = argparse.ArgumentParser(description='Convert the output of the sushi+2HDMC to .root + .txt format')
    parser.add_argument('-i',dest='input_dir', type=str, help='path with output of the submission tool')
    parser.add_argument('-o',dest='output', type=str, help='output root file name',default='output')
    args = parser.parse_args()
    # convert input to absolute path
    args.input_dir  = getAbsPath(args.input_dir) + '/'
    return args

if __name__ == '__main__':
    # Read user input:
    cmd_args = ParseOption()
    untarSusHiOutput(cmd_args.input_dir)
    makeReadableGrid(cmd_args.input_dir)

#!/usr/bin/python
import argparse
import sys
sys.path.insert(0,'../')
from lib.tools import *
from lib.makeReadableGrid import *
import cProfile

if __name__ == '__main__':
    # Read user input:
    input_dir = '../output/test4/'
    input_dir = getAbsPath(input_dir) + '/'

    untarSusHiOutput(input_dir)
    # Optimise performance with cProfile:
    cProfile.run('makeReadableGrid(input_dir)')
    # makeReadableGrid(input_dir)

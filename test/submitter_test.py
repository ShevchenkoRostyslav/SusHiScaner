#!/usr/bin/python

"""Unit test for submitter class.

"""

import sys
sys.path.insert(0,'../')
from lib.submitter import *
from lib.parseInput import *
import cProfile

__author__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"

if __name__ == '__main__':
    # Read comand line arguments
    cmd_args = ParseOption()
    logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%d/%m/%Y %H:%M:%S',level=getattr(logging,cmd_args.verbose))
    # Process user input
    in_args = pushInput(cmd_args)
    # Start submitting the jobs
    proc = submitter.choose_cluster(cmd_args.submitter)
    cProfile.run('proc.submit(cmd_args,in_args)')

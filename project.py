#!/usr/bin/python
import logging
import sys
from lib.parseInput import *
from lib.submitter import *
from lib.Resubmission import Resubmit

if __name__ == '__main__':
    # Read comand line arguments
    cmd_args = ParseOption()
    # Declare logging
    logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%d/%m/%Y %H:%M:%S',level=getattr(logging,cmd_args.verbose))
    # Check if resubmission shoudl be done:
    if cmd_args.resubmit:
        Resubmit(cmd_args)
    # Process user input
    in_args = pushInput(cmd_args)
    # Choose submitter type
    proc = submitter.choose_cluster(cmd_args.submitter,cmd_args.submission_pars)
    # Start submitting the jobs
    proc.submit(cmd_args,in_args)

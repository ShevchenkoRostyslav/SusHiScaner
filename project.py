#!/usr/bin/python
import logging
from lib.parseInput import *
from lib.submitter import *

if __name__ == '__main__':
    # Read comand line arguments
    cmd_args = ParseOption()
    logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%d/%m/%Y %H:%M:%S',level=getattr(logging,cmd_args.verbose))
    # Process user input
    in_args = pushInput(cmd_args)
    # Start submitting the jobs
    proc = submitter.choose_cluster(cmd_args.submitter)
    proc.submit(cmd_args,in_args)

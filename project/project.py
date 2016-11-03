#!/usr/bin/python
import logging
import sys
sys.path.insert(0,'../project')
# from lib.parseInput import *
from lib.parseInput import *

if __name__ == '__main__':
    cmd_args = ParseOption()
    logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%d/%m/%Y %H:%M:%S',level=getattr(logging,cmd_args.verbose))
    pushInput(cmd_args)
    # if not len(sys.argv) > 1: logging.info('no arguments were provided')

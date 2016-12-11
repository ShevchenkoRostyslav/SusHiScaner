#!/usr/bin/python
"""Main macro to submit SusHi jobs.

Main macro to run SusHi using naf/lxplus/(other batch)/shell. Also resubmission
of failed jobs can be done using this macro.

Usage:
python project.py -h # Global help menu
positional arguments:
  {physicalbasis,lambdabasis,lxplus,naf}
    physicalbasis       arguments for physical basis
    lambdabasis         arguments for lambda basis
    lxplus              arguments to run jobs at lxplus
    naf                 arguments to run jobs at naf

optional arguments:
  -h, --help            show this help message and exit
  -o,output_dir OUTPUT_DIR
                        output dir path
  -r,resubmit           if specified - resubmission of job will be done

To submit with naf:
python project.py naf -h
  -h, --help            show this help message and exit
  --n POINTSPERJOB      Number of points per job
  -d,dir_to_resubmit JOBDIRTORESUBMIT
                        Job directory to resubmit
  --submission_pars SUBMISSION_PARS
                        Parameters that will be used with bsub

To submit with lxplus:
python project.py lxplus -h
  -h, --help            show this help message and exit
  --n POINTSPERJOB      Number of points per job
  -d,dir_to_resubmit JOBDIRTORESUBMIT
                        Job directory to resubmit
  --submission_pars SUBMISSION_PARS
                        Parameters that will be used with bsub

To run SusHi job using shell:
python project.py physicalbasis -р
python project.py lambdabasis -р
"""

import sys
from lib.parseInput import *
from lib.submitter import *
from lib.Resubmission import Resubmit

__author__ = "Rostyslav Shevchenko"
__credits__ = ["Hualin Mei"]
__version__ = "1.0.0"
__maintainer__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"
__status__ = "Production"

if __name__ == '__main__':
    # Read comand line arguments
    cmd_args = ParseOption()
    # Check if resubmission should be done:
    if cmd_args.resubmit:
        Resubmit(cmd_args)
    # Process user input
    in_args = pushInput(cmd_args)
    # Choose submitter type
    proc = submitter.choose_cluster(cmd_args.submitter,cmd_args.submission_pars)
    # Start submitting the jobs
    proc.submit(cmd_args,in_args)

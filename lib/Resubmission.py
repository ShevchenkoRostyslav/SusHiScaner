#!/usr/bin/env python
"""Module to resubmit failed/corrupted jobs.

"""

import os
import CheckJobs
import submitter

__author__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"

def Resubmit(job_dir,submitter):
    """Main method to resubmit particular job.

    """
    # Check if .csh file is inside
    CheckJobs.CheckIfCshExists(job_dir)
    # submit
    submitter.SubmitJob(job_dir)

# TODO: Implement resubmission for all folders failed while CheckJobs.py

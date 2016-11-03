#!/usr/bin/python
import sys
sys.path.insert(0,'../project')
from lib.submitter import *

s = submitter.choose_cluster('naf')
print s

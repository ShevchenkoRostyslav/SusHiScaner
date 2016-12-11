#!/usr/bin/env python
"""Make a .root file from .txt file with grid from SusHi output.

"""
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from array import array

__author__ = "Rostyslav Shevchenko"
__maintainer__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"

def CreateTBranch(dictionary,tree):
    """Method to create TBranch for TTree from dictionary.

    """
    for v in dictionary:
        tree.vars[str(v)] = array('f', [0.])
        tree.Branch(str(v),tree.vars[str(v)],str(v) + '/F')

def FillTTree(dictionary,sub_line,tree):
    """Method to fill TBranches by values in the sub-line.

    Attention!!!! Order has to match order of the line was filled.
    see getInfoFromSusHiOutput::GetLineWithOutput function
    """
    for v, f in zip(dictionary, sub_line):
        tree.vars[str(v)][0] = float(f)

def MakeTTree(dict_scan,dict_sushi,dict_2hdmc):
    """Method to create TTree object accroding to input higgs type.

    """
    tree = ROOT.TTree('tree','2HDM parameter space')
    # Assign a dic to this tree
    tree.vars = {}
    # Iterate over the Scan vars
    [CreateTBranch(d,tree) for d in (dict_scan,dict_sushi,dict_2hdmc)]

    return tree

def MakeTFile(name):
    """Method that creates the root file according to the name.

    """
    file_root = ROOT.TFile(name,'recreate')
    return file_root

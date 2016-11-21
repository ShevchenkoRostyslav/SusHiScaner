#!/usr/bin/env python
"""Make a .root file from .txt file with grid from SusHi output.

"""

from ROOT import TTree
from array import array

__author__ = "Rostyslav Shevchenko"
__credits__ = ["Hualin Mei", "Stefano Lacaprara"]
__version__ = "1.0.0"
__maintainer__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"
__status__ = "Production"

def MakeTTree(dictHiggs):
    """Method to create TTree object accroding to input higgs type.

    """
    dict_sushi = dictHiggs[0]   # sushi output
    dict_2hdmc = dictHiggs[1]   # 2hdmc output
    # See skype chat from Gregor
    vars = array('f', ofanotherarray)
    tree = TTree('tree','2HDM parameter space')

    for v in dict_sushi:
        tree.Branch(str(v),)

        # I want dynamically fill the TTree, line-by-line. Ask Gregor :D

def

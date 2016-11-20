# SusHiScaner
Author:     "Rostyslav Shevchenko"
Credits:    "Hualin Mei and Stefano Lacaprara"
Version:    "1.0.0"
Maintainer: "Rostyslav Shevchenko"
Email:      "rostyslav.shevchenko@desy.de"
            "shevchenko.rostislav@gmail.com"
            "rostyslav.shevchenko@cern.ch"
Status:     "Beta-test"

SusHiScaner is designed for comfortable reading and processing of SusHi and
2HDMC output and converting it to the human readable format - .txt and
analysis-usage format - .root

PRE-REQUEST
SusHi(Supersymmetric Higgs) package should be installed and interfaced
with 2HDMC:
1. Instructions to install SusHi(http://sushi.hepforge.org/manual.html ) can be
found elsewhere: http://sushi.hepforge.org/manual/SusHi150.pdf
2. 2HDMC calculator(https://2hdmc.hepforge.org) should be installed as well.
One can follow instructions under: https://arxiv.org/abs/0902.0851
3. To install everything in one goal instructions at doc/installation.txt
can be considered(Thanks to Stefano Lacaprara)

INSTRUCTIONS FOR INSTALLATION
Clone the head (branch master) of the repository
git clone git@github.com:ShevchenkoRostyslav/SusHiScaner.git .

HOW TO USE
Help menu: python project.py -h/--help
1. SusHi can be ran both:
- interactively (with cmd) specifying all arguments in the command line:
  python project.py physicalbasis/lambdabasis -h
- using lxplus. Input parameters should be specified in setup.py,
  while number of points per job should be specified interactively as well as
  queue
  python project.py lxplus -h/--help
- for DESY (naf-cms) users - naf can be used as well, with the same strategy as
  lxplus

2. To produce .txt and .root file - postprocessor.py should be used
Help menu: python postprocessor.py -h/--help

#Have fun
All bug reports/ questions/ suggestions etc should be sent to the Maintainer

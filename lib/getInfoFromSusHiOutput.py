#!/usr/bin/python
"""Get an information from the SusHi output and store it.

"""

import os, time
import glob
from subprocess import Popen,PIPE,call
from gridSaveOrder import *
from makeRootFromTxt import *
from ROOT import TTree,TFile

__author__ = "Rostyslav Shevchenko"
__credits__ = ["Hualin Mei", "Stefano Lacaprara"]
__version__ = "1.0.0"
__maintainer__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"
__status__ = "Production"

def GetFromSushiOut(fileName, tag):
    """Method to grep SusHi part of the output.

    Method to grep SusHi part of the output to get information
    about cross-sections and bosons masses
    grep is done using the tags defined in gridSaveOrder
    which is basically just a description of the line in the SusHi output
    """

    # Search for a tag (i.e. tan(beta)/sin(beta-alpha) etc) in a file
    proc = Popen('grep "' + str(tag) + '" ' + fileName, shell=True, stdout=PIPE)
    # Store output of the search in variable
    stdout_value = proc.communicate()[0]
    # Split the line, to the: NUMBER     <<VALUE>>      # TAG
    if tag != 'Charged Higgs decays':
       value = stdout_value.split()[1]
    else:
       value = stdout_value.split()[2]
    return value

def GetBRFrom2HDMCOut(fileName, init1, init2, final):
    """Method to grep 2HDMC part of the output.

    Method to grep 2HDMC part of the output to get information
    about cross-sectiopns and bosons masses
    work can be illustrated on the following example:
    User is looking for a BR(h->xx), then in the ouput of the 2HDMC:
    DECAY  25     1.38459668e-02   # h1 decays, lightest CP-even Higgs  <-- searched by grep -A
            BR          NDA    ID1   ID2
      2.52859182e-04     2       3    -3
      9.12317911e-03     2       4    -4
      6.15529252e-01     2       5    -5
      1.54235930e-09     2      11   -11
      6.59403917e-05     2      13   -13
      1.86258247e-02     2      15   -15
      2.38631375e-01     2      22    22
      7.50305354e-03     2      23    23
      6.03752180e-02     2      24   -24
      1.89122675e-02     2      23    22
      3.09810297e-02     2      21    21
    DECAY  35     3.82311395e+05   # h2 decays, heaviest CP-even Higgs   <-- searched by grep -B
    """
    # grep the upper boundary of the output
    Init1 = 'grep -A 30 "DECAY  ' + init1 + '" '
    if init2 != '#':
    # grep the lower boundary
     Init2 = ' | grep -B 30 "DECAY  ' + init2 + '" | '
    else:
     Init2 = ' | grep -B 30 "#" | '

    proc = Popen(Init1 + fileName + Init2 + final, shell=True, stdout=PIPE)
    # Store output of the search in variable
    stdout_value = (proc.communicate()[0])
    # If no such decay - return 0
    if len(stdout_value.split()) > 0:
     value = stdout_value.split()[0]
    elif len(stdout_value.split()) == 0:
     value = str(0)
    return value

def UseThisFile(fileName, type2hdm, higgs):
    """Method to decide whether current file should be used or not according to the 2hdm type and higgs boson type.

    """

    if not type2hdm in fileName: return False
    if higgs == 'h': higgs_type = '11'
    elif higgs == 'H': higgs_type = '12'
    elif higgs == 'A': higgs_type = '21'
    if not higgs == 'extra' and not '_Htype_' + higgs_type in fileName: return False

    return True

def GetLineWithOutput(fileName,dictHiggs,dict_scan,tree):
    """Method that returnes single line with combined output from SusHi and 2HDMC.

    This method extract the list of numbers according to it position at SusHi / 2HDMC output
    Also - it fills the TTree created before with this list.
    """
    dict_sushi = dictHiggs[0]   # sushi output
    dict_2hdmc = dictHiggs[1]   # 2hdmc output
    h1 = dictHiggs[2]           # pdg particle code for particle of interests, i.e. for BR(h->xx) this is 25
    h2 = dictHiggs[3]           # pdg particle code for next Higgs in the 2HDMC output.i.e for BR(h->xx) this would be 35
    # First get values of pois
    pois = [GetFromSushiOut(fileName, dict_scan[k]) for k in dict_scan]
    FillTTree(dict_scan, pois, tree)
    # Sushi ouput
    fromSushi = [GetFromSushiOut(fileName, dict_sushi[k]) for k in dict_sushi]
    FillTTree(dict_sushi, fromSushi, tree)
    # 2HDMC output
    from2hdmc = [GetBRFrom2HDMCOut(fileName, h1,  h2,  dict_2hdmc[k]) for k in dict_2hdmc]
    FillTTree(dict_2hdmc, from2hdmc, tree)
    tree.Fill()
    # Make a single line in the future output .txt file
    line = ' '.join(pois + fromSushi + from2hdmc)
    return line

def getInfoFromSusHiOutput(input_dir,output_dir,type2HDM,higgs):
    """Method to parse output of the SusHi to create a grid and store in .txt and .root

    """


    # get information from dictionary associated to higgs:
    dictHiggs = dict_higgs[higgs]
    dict_sushi = dictHiggs[0]   # sushi output
    dict_2hdmc = dictHiggs[1]   # 2hdmc output
    h1 = dictHiggs[2]           # pdg particle code for particle of interests, i.e. for BR(h->xx) this is 25
    h2 = dictHiggs[3]           # pdg particle code for next Higgs in the 2HDMC output.i.e for BR(h->xx) this would be 35
    xsHiggs = dictHiggs[4]      # xsection

    # .txt and .root names:
    fileNames = type2HDM + '_m' + higgs
    tmpTxt   = output_dir + '/txtFiles/' + fileNames + '.txt'
    # Get starting time to estimate the total time:
    start_time = time.time()
    # Create TTree
    tfile = MakeTFile(output_dir + '/rootFiles/' + fileNames + '.root')
    tree = MakeTTree(dict_scan, dict_sushi, dict_2hdmc)
    create_root_file = True
    # Get pois
    _keys_scan = [i for i in dict_scan]
    print '_keys_scan', _keys_scan
    # Assign reference strings from sushi output
    _keys_sushi = [i for i in dict_sushi]
    # Assign reference 'greps' from 2HDMC output
    _keys_2hdmc = [i for i in dict_2hdmc]
    # Join all together
    keys = ' '.join(_keys_scan + _keys_sushi + _keys_2hdmc)
    # Start loop over the DIRs with ouput of the SusHi
    i = 0
    for dir in glob.glob(input_dir + 'job*'):
        # Start loop over the FILEs in the DIR
        for file in glob.glob(dir + '/*out'):
            if i > 20 : break
            i += 1
            # Check whether this file contains specified 2hdm type and higgs boson
            if not UseThisFile(file, type2HDM, higgs):
                create_root_file = False
                continue
            # Get output from SusHi and 2HDMC
            line = GetLineWithOutput(file,dictHiggs,dict_scan,tree)
            # Save the output
            if os.path.isfile(tmpTxt):
                call('echo "' + line + '" >>  ' + tmpTxt, shell=True)
            else:
                call('echo "' + keys + '" > ' + tmpTxt, shell=True)
    tfile.Write()
    tfile.Close()
    # Hardcoded soultion to remove root file if it's empty
    if not create_root_file: call('rm ' + output_dir + '/rootFiles/' + fileNames + '.root',shell=True)
    print("--- %s seconds ---" % (time.time() - start_time))

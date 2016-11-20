#!/usr/bin/python
import os, time
import glob
from subprocess import Popen,PIPE,call
from gridSaveOrder import *

# Method to grep SusHi part of the output to get information
# about cross-sections and bosons masses
# grep is done using the tags defined in gridSaveOrder
# which is basically just a description of the line in the SusHi output
def GetFromSushiOut(fileName, tag):
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

# Method to grep 2HDMC part of the output to get information
# about cross-sectiopns and bosons masses
# work can be illustrated on the following example:
# User is looking for a BR(h->xx), then in the ouput of the 2HDMC:
# DECAY  25     1.38459668e-02   # h1 decays, lightest CP-even Higgs  <-- searched by grep -A
#            BR          NDA    ID1   ID2
#   2.52859182e-04     2       3    -3
#   9.12317911e-03     2       4    -4
#   6.15529252e-01     2       5    -5
#   1.54235930e-09     2      11   -11
#   6.59403917e-05     2      13   -13
#   1.86258247e-02     2      15   -15
#   2.38631375e-01     2      22    22
#   7.50305354e-03     2      23    23
#   6.03752180e-02     2      24   -24
#   1.89122675e-02     2      23    22
#   3.09810297e-02     2      21    21
#DECAY  35     3.82311395e+05   # h2 decays, heaviest CP-even Higgs   <-- searched by grep -B
def GetBRFrom2HDMCOut(fileName, init1, init2, final):
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
    if not type2hdm in fileName: return False
    if higgs == 'h': higgs_type = '11'
    elif higgs == 'H': higgs_type = '12'
    elif higgs == 'A': higgs_type = '21'
    if not higgs == 'extra' and not '_Htype_' + higgs_type in fileName: return False

    return True

# Main method to parse output of the SusHi to create a grid
def getInfoFromSusHiOutput(input_dir,output_dir,type2HDM,higgs):
    # get information from dictionary associated to higgs:
    dictHiggs = dict_higgs[higgs]
    dict_sushi = dictHiggs[0]   # sushi output
    dict_2hdmc = dictHiggs[1]   # 2hdmc output
    h1 = dictHiggs[2]           # pdg particle code for particle of interests, i.e. for BR(h->xx) this is 25
    h2 = dictHiggs[3]           # pdg particle code for next Higgs in the 2HDMC output.i.e for BR(h->xx) this would be 35
    xsHiggs = dictHiggs[4]      # xsection

    # Get starting time to estimate the total time:
    start_time = time.time()

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
    for dir in glob.glob(input_dir + 'job*'):
        # Start loop over the FILEs in the DIR
        for file in glob.glob(dir + '/*out'):
            # Check whether this file contains specified 2hdm type and higgs boson
            # if not type2HDM == 'type' + GetFromSushiOut(file, '2HDM type'): continue
            # if not higgs == 'extra' and not xsHiggs == 'xs' + GetFromSushiOut(file, '11=h, 12=H, 21=A'): continue
            if not UseThisFile(file, type2HDM, higgs): continue
            # if not UseThisFile(file, type2HDM, xsHiggs) and not higgs == 'extra': continue
            # First get values of pois
            pois = [GetFromSushiOut(file, dict_scan[k]) for k in dict_scan]
            # Sushi ouput
            fromSushi = [GetFromSushiOut(file, dict_sushi[k]) for k in dict_sushi]
            # 2HDMC output
            from2hdmc = [GetBRFrom2HDMCOut(file, h1,  h2,  dict_2hdmc[k]) for k in dict_2hdmc]
            # Make a single line in the future output .txt file
            line = ' '.join(pois + fromSushi + from2hdmc)
            # Save the output
            txtName = type2HDM + '_m' + higgs + '.txt'
            tmpTxt = output_dir + '/' + txtName
            if os.path.isfile(tmpTxt):
                call('echo "' + line + '" >>  ' + tmpTxt, shell=True)
            else:
                call('echo "' + keys + '" > ' + tmpTxt, shell=True)

    print("--- %s seconds ---" % (time.time() - start_time))

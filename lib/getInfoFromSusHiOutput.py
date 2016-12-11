#!/usr/bin/python
"""Get an information from the SusHi output and store it.

"""

import os, time
import glob
from subprocess import Popen,PIPE,call
from gridSaveOrder import *
from makeRootFromTxt import *
from tools import *
import re # for grep in the file
from printer import printProgress
import tarfile

__author__ = "Rostyslav Shevchenko"
__maintainer__ = "Rostyslav Shevchenko"
__email__ = "rostyslav.shevchenko@desy.de"

def ReplaceSpecChar(string):
    """Method to replace special characters in string.

    """
    temp_string = string
    for i in "!@#$%^&*()[]{};:,.<>?|`~-=_+":
        if i in temp_string:
            temp_string = temp_string.replace(i , '\\'+i)
    return temp_string

def GetFromSushiOut(file_stream, tag):
    """Method to grep SusHi part of the output.

    Method to grep SusHi part of the output to get information
    about cross-sections and bosons masses
    grep is done using the tags defined in gridSaveOrder
    which is basically just a description of the line in the SusHi output
    """
    # Construct temp string with special characters if there:
    temp_tag = ReplaceSpecChar(tag)
    # Search for a tag (i.e. tan(beta)/sin(beta-alpha) etc) in a file
    # Take into account only the first evidance to avoid duplication ->[0]
    values = re.findall("\n(.*?)" + temp_tag,file_stream)[0]
    # Split the line, to the: NUMBER     <<VALUE>>      # TAG
    if tag != 'Charged Higgs decays':
       value = values.split()[1]
    else:
       value = values.split()[2]
    return value

def GetBRFrom2HDMCOut(file_stream, init1, init2, id1, id2):
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
    # define the upper bound of the output
    start = '^DECAY\s*' + init1 + '.*$'
    # define the lower bound
    if init2 != '#':
        end = '^DECAY\s*' + init2 + '.*$'
    else:
        end = '^\#$'
    # constract regexp:
    obj = re.compile("^\s*(?P<value>[0-9,\.,e,\-]*)\s*(?P<arg1>[-,0-9]*)\s*"+ id1 + "\s*" + id2 + ".*")
    # compile:
    re_start = re.compile(start)
    re_end = re.compile(end)
    # search:
    A_START = 1
    A_PROCESS = 2
    action = A_START
    value = None
    for line in file_stream.split('\n'):
        if action == A_START:
            begin = re_start.search( line )
            if begin is not None:
                action = A_PROCESS
        elif action == A_PROCESS:
            item = obj.search( line )
            if item is None:
                if re_end.search( line ) is not None:
                    action = A_START
            else:
                value = item.group('value')
    # If no such decay - return 0
    if value == None:
        value = '0'
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

def GetLineWithOutput(file_string,dictHiggs,dict_scan,tree):
    """Method that returnes single line with combined output from SusHi and 2HDMC.

    This method extract the list of numbers according to it position at SusHi / 2HDMC output
    Also - it fills the TTree created before with this list.
    """
    dict_sushi = dictHiggs[0]   # sushi output
    dict_2hdmc = dictHiggs[1]   # 2hdmc output
    h1 = dictHiggs[2]           # pdg particle code for particle of interests, i.e. for BR(h->xx) this is 25
    h2 = dictHiggs[3]           # pdg particle code for next Higgs in the 2HDMC output.i.e for BR(h->xx) this would be 35
    # First get values of pois
    pois = [GetFromSushiOut(file_string, dict_scan[k]) for k in dict_scan]
    FillTTree(dict_scan, pois, tree)
    # Sushi ouput
    fromSushi = [GetFromSushiOut(file_string, dict_sushi[k]) for k in dict_sushi]
    FillTTree(dict_sushi, fromSushi, tree)
    # 2HDMC output
    from2hdmc = [GetBRFrom2HDMCOut(file_string, h1,  h2,  dict_2hdmc[k].split()[0],dict_2hdmc[k].split()[1]) for k in dict_2hdmc]
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
    out_txt_f = open(tmpTxt, 'w')
    # Get starting time:
    start_time = time.time()
    # Create TTree
    tfile = MakeTFile(output_dir + '/rootFiles/' + fileNames + '.root')
    tree = MakeTTree(dict_scan, dict_sushi, dict_2hdmc)
    create_root_file = True
    # Get pois
    _keys_scan = [i for i in dict_scan]
    # Assign reference strings from sushi output
    _keys_sushi = [i for i in dict_sushi]
    # Assign reference 'greps' from 2HDMC output
    _keys_2hdmc = [i for i in dict_2hdmc]
    # Join all together
    keys = ' '.join(_keys_scan + _keys_sushi + _keys_2hdmc)
    # Write keys to the file:
    out_txt_f.write(keys + '\n')
    # Add progress bar:
    i = 0
    input_dirs = glob.glob(input_dir + 'job*')
    printProgress(i, len(input_dirs))
    # Start loop over the DIRs with ouput of the SusHi
    for dir in input_dirs:
        # Start loop over the FILEs in the DIR
        for file in glob.glob(dir + '/*out'):
            # Check whether this file contains specified 2hdm type and higgs boson
            if not UseThisFile(file, type2HDM, higgs):
                create_root_file = False
                continue
            # Open the file:
            file_string = open(file, mode='r').read()
            # Get output from SusHi and 2HDMC
            line = GetLineWithOutput(file_string,dictHiggs,dict_scan,tree)
            # Save the output
            out_txt_f.write(line + '\n')
            create_root_file = True
        # Update Progress bar:
        time.sleep(0.1)
        i += 1
        printProgress(i, len(input_dirs))
    # Close .txt file:
    out_txt_f.close()
    # Write and Close root file:
    tfile.Write()
    tfile.Close()
    # Hardcoded soultion to remove root file if it's empty
    if not create_root_file:
        os.remove(output_dir + '/rootFiles/' + fileNames + '.root')
        os.remove(output_dir + '/txtFiles/' + fileNames + '.txt')
    print fileNames + ' DONE'
    print("--- %s seconds ---" % (time.time() - start_time))

def makeReadableGrid(output_dir):
    """Module to make a .txt and .root files.

    """
    # higgsType and 2HDM types
    higgsType = ['A', 'h', 'H']
    types2HDM = ['type3','type4']
    # create directory for txt files:
    txtDir = MakeCleanDir(output_dir + '/txtFiles/')
    # and for root files
    rootDir = MakeCleanDir(output_dir + '/rootFiles/')
    for higgs in higgsType:
        for type2HDM in types2HDM:
            getInfoFromSusHiOutput(output_dir + '/sushi_out/',output_dir,type2HDM,higgs)

def untarSusHiOutput(output_dir):
    """Method to untar SusHi output.

    """
    # Check whether directory exists
    if not os.path.exists(output_dir):
        raise AttributeError("ERROR: Wrong dir name " + output_dir + " was provided to tools::untarSusHiOutput")
    # Check the output_dir
    if len(glob.glob(output_dir + 'sushi_out/job_*')) == 0:
        raise AttributeError("ERROR: Wrong dir name " + output_dir + " was provided to tools::untarSusHiOutput")
    # Iterate through the job_i folders from SusHi output
    for job in glob.glob(output_dir + 'sushi_out/job_*'):
        # use only the name of the folder
        job_i = os.path.basename(os.path.normpath(job))
        # extract job_id:
        regex = re.compile(r'\d+')
        job_id = regex.search(job_i).group(0)
        # tar name
        tar_names = glob.glob(job + '/out_' + job_id + '.*gz*')# + '.tgz'
        if len(tar_names) == 0:
            raise AttributeError("ERROR: No .tgz file at " + job + '/out_' + job_id + '.*gz*')
        # Untar
        tar = tarfile.open(tar_names[0])
        tar.extractall(job)
        tar.close()

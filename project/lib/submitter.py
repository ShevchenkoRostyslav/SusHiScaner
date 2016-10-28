#!/usr/bin/python
import sys

'''
Class for submission jobs to naf/lxplus/shell
'''

class submitter(object):
    def choose_cluster(type):
        if type == 'naf':
            return naf()
        elif type == 'lxplus':
            return lxplus()
        elif type == 'shell':
            return shell()
        assert 0, 'Wrong cluster selected: ' + type
    choose_cluster = staticmethod(choose_cluster)
            
        
    def command(self):
        return str('')
    
    def addParameters(self,parameters):
        self.parameters = parameters
    
class naf(submitter):
    def __init__(self):
        self.name = 'naf'
    
    def command(self):
        return 'qsub ' + self.parameters

class lxplus(submitter):
    def __init__(self):
        self.name = 'lxplus'
        
    def command(self):
        return 'bsub ' + self.parameters
        
class shell(submitter):
    def __init__(self):
        self.name = 'shell'

        
    
#!/usr/bin/python
import sys

'''
Class for submission jobs to naf/lxplus/shell
'''

class submitter(object):
    def __init__(self,type = '',command = '',parameters = ''):
        self.type = type
        self._command = command
        self._parameters = parameters
    
    def choose_cluster(type):
        if type == 'naf':
            return naf()
        elif type == 'lxplus':
            return lxplus()
        elif type == 'shell':
            return shell()
        assert 0, 'Wrong cluster selected: ' + type
    choose_cluster = staticmethod(choose_cluster)
            
    def addParameters(self,parameters):
        self._parameters += parameters
        
class naf(submitter):
    def __init__(self):
        submitter.__init__(self,'naf','qsub')
    
    def __str__(self):
        return 'Naf: ' + self._command + self._parameters
    

class lxplus(submitter):
    def __init__(self):
        self.type = 'lxplus'
        
    def __str__(self):
        return 'lxplus used for submission'
        
class shell(submitter):
    def __init__(self):
        self.type = 'shell'

    def __str__(self):
        return 'shell used for submission'
    
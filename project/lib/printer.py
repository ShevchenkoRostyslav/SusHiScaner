import sys

def differentVals(vals,name):
    unique = []
    for v in vals:
        if round(v.iput[name],2) not in unique: unique.append(round(v.iput[name],2))
    return unique

def printInput(basis_ar,iput):
    print '====================INPUT===================='
    print 'Processor: ', iput.submitter
    if iput.submitter == 'lxplus': print 'Queue: ', iput.queue
    print 'Number of points: ', len(basis_ar)
    if iput.submitter != 'shell':
        print 'Number of points / job:', iput.pointsPerJob

    print 'Higgs types: ', differentVals(basis_ar, 'higgsType')
    print '2HDM type: ', differentVals(basis_ar, 'thdmType')
    print 'tanBeta: ', differentVals(basis_ar, 'tanBeta')
    print 'm12: ', differentVals(basis_ar, 'm12')
    if basis_ar[0].basis == 'lambdabasis':
        print 'Lambda Basis was selected'
        print 'lambda1: ', differentVals(basis_ar, 'lambda1')
        print 'lambda2: ', differentVals(basis_ar, 'lambda2')
        print 'lambda3: ', differentVals(basis_ar, 'lambda3')
        print 'lambda4: ', differentVals(basis_ar, 'lambda4')
        print 'lambda5: ', differentVals(basis_ar, 'lambda5')
        print 'lambda6: ', differentVals(basis_ar, 'lambda6')
        print 'lambda7: ', differentVals(basis_ar, 'lambda7')
    elif basis_ar[0].basis == 'physicalbasis':
        print 'Physical Basis was selected'
        print 'mh: ', differentVals(basis_ar, 'mh')
        print 'mH: ', differentVals(basis_ar, 'mH')
        print 'mA: ', differentVals(basis_ar, 'mA')
        print 'mC: ', differentVals(basis_ar, 'mC')
        print 'sin(beta-alpha): ', differentVals(basis_ar, 'sinB_A')
        print 'lambda6: ', differentVals(basis_ar, 'lambda6')
        print 'lambda7: ', differentVals(basis_ar, 'lambda7')
    # decide whether u want to continue or not
    while True:
        continueSubmission = raw_input('Continue to submit to' + iput.submitter + ' ? Type y or n:\n')
        if continueSubmission in ['n','y']: break
        else:
            print('That is not a valid option! Please specify `y` or `n`')
    if continueSubmission == 'n': sys.exit()

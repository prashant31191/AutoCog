#!/bin/python

import json, os




def parsetxt(respath):
    maindict={}
    apkName=''
    label=''


    f=open(respath,'r')
    lines=f.readlines()
    f.close()
    for l in lines:
        l=l.strip()
        if l.endswith('.apk'):
            apkName=l
            continue
        if len(l)==0 and len(apkName)>0 and len(label)>0:
            if apkName not in maindict:
                if label=='true':
                    maindict[apkName]=True
                elif label=='false':
                    maindict[apkName]=False
            apkName=''
            label=''
            continue
        if l=='true' or l=='false':
            label=l
            continue
    return maindict


def checkres(goodapps, badapps, allresdict):
    

    TP=0
    FP=0
    TN=0
    FN=0
    fplst=[]
    fnlst=[]
    for eachapp in goodapps:
        if eachapp not in allresdict:
            print "Good Missing app: "+eachapp
            continue
        if allresdict[eachapp]==True:
            TP=TP+1
        elif allresdict[eachapp]==False:
            FN=FN+1
            fnlst.append(eachapp)
    for eachapp in badapps:
        if eachapp not in allresdict:
            print "Bad Missing app: "+eachapp
            continue
        if allresdict[eachapp]==True:
            FP=FP+1
            fplst.append(eachapp)
        elif allresdict[eachapp]==False:
            TN=TN+1
        


    print "%s\t"%TP+'%s\t'%FP+'%s\t'%FN+'%s\n'%TN
    print 'FP: \n\n'
    print fplst

    print 'FN: \n\n'
    print fnlst
    if TP+FP==0 or TP+FN==0:
        return -1

    Precision=TP*1.0/(TP+FP)
    Recall=TP*1.0/(TP+FN)

    if Precision+Recall==0:
        return -1

    Fscore=2*Precision*Recall/(Precision+Recall)
    Accuracy=(TP+TN)*1.0/(TP+TN+FP+FN)


    print '%s\t'%Precision+'%s\t'%Recall+'%s\t'%Fscore+'%s'%Accuracy


def parseapps(filename):
    apps=[]
    f=open(filename)
    lines=f.readlines()
    for l in lines:
        l=l.strip()
        if len(l)<2:
            continue
        if l.endswith('.apk'):
            if l in apps:
                print l
            apps.append(l)
            continue
        elif not l.endswith('.apk'):
            if l+'.apk' in apps:
                print l+'.apk'
            apps.append(l+'.apk')
            continue
    return apps

proj_path=os.path.abspath('../..')
respath=proj_path+'/evaluation/49183res/'
validpath=proj_path+'/evaluation/valiation/'

rootDir=respath
list_dirs=os.walk(rootDir)

allresdict={}

for root, dirs, files in list_dirs:
        for d in dirs:
            targetperm=d
            if targetperm!='android.permission.READ_CALENDAR':
                continue
            print d
            level2rootDir=os.path.join(root, d)
            newroot=rootDir+d+'/'
            new_list_dirs=os.walk(newroot)
            for Nroot, Ndirs, Nfiles in new_list_dirs:
                for Nfile in Nfiles:
                   # if Nfile.find('oldnew')>=0:
                        #continue
                    respath=newroot+Nfile
                    detectdict=parsetxt(respath)
                    for apkName in detectdict:
                        if apkName not in allresdict:
                            allresdict[apkName]=detectdict[apkName]
                        elif apkName in allresdict:
                            print apkName

            print len(allresdict)
            goodapps=[]
            badapps=[]




            if targetperm=='android.permission.READ_CALENDAR':
                goodapps=parseapps('good_read_calendar.txt')
                badapps=parseapps('bad_read_calendar.txt')

            for eachapp in goodapps:
                if eachapp in badapps:
                    print "Mut app: "+eachapp

            for eachapp in allresdict:
                if eachapp not in goodapps and eachapp not in badapps:
                    print "tag: "+eachapp


            checkres(goodapps,badapps,allresdict)
            allresdict={}



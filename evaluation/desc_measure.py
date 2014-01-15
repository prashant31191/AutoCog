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


def checkres(detectdict, validset,groundtruth,targetperm, fold):
    
    finalpath=proj_path+'/evaluation/performance/'+targetperm
    command='mkdir '+finalpath
    os.system(command)
    destpath=finalpath+'/fold%s.txt'%fold

    TP=0
    FP=0
    TN=0
    FN=0

    for eachapk in validset:

        if eachapk not in detectdict:
            continue
        detectlabel=detectdict[eachapk]
        haslabel=targetperm in groundtruth[eachapk]

        if detectlabel==True and haslabel==True:
            TP=TP+1
            #print 'TP '+eachapk
        
        if detectlabel==True and haslabel==False:
            FP=FP+1
            #print 'FP '+eachapk

        if detectlabel==False and haslabel==True:
            FN=FN+1
            #print eachapk

        if detectlabel==False and haslabel==False:
            TN=TN+1



    if FP+TN==0 or TP+FN==0:
        return -1

    overtell=FP*1.0/(FP+TN)
    undertell=FN*1.0/(FN+TP)

    print '%s\t'%overtell+'%s'%undertell

proj_path=os.path.abspath('..')


f=open(proj_path+'/data/22458_apps_permdict.json','r')
groundtruth=json.load(f)
f.close()

respath=proj_path+'/evaluation/newres/'
validpath=proj_path+'/evaluation/valiation.10fold/'

rootDir=respath
list_dirs=os.walk(rootDir)

for root, dirs, files in list_dirs:
        for d in dirs:
            targetperm=d

            level2rootDir=os.path.join(root, d)
            newroot=rootDir+d+'/'
            new_list_dirs=os.walk(newroot)
            for Nroot, Ndirs, Nfiles in new_list_dirs:
                for Nfile in Nfiles:
                    respath=newroot+Nfile
                    detectdict=parsetxt(respath)

                    fold=Nfile.replace('newout','')
                    fold=fold.replace('.txt','')
                    if Nfile.find('old')>=0:
                        continue
                    print respath
                    validfilename=validpath+targetperm+'/validset'+fold+'.json'
                    file_in=open(validfilename,'r')
                    validset=json.load(file_in)
                    file_in.close()
                    checkres(detectdict,validset,groundtruth,targetperm, fold)






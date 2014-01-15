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


def checkres(detectdict, validset,groundtruth,targetperm, fold, goodratio):
    
    finalpath='/home/zyqu/semant2/evaluation/performance/'+targetperm
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

    #print fold
    #print "%s\t"%TP+'%s\t'%FP+'%s\t'%FN+'%s\n'%TN
    #if TP+FP==0 or TP+FN==0:
        #return -1

    #Precision=TP*1.0/(TP+FP)
    #Recall=TP*1.0/(TP+FN*goodratio)

    #if Precision+Recall==0:
        #return -1

    #Fscore=2*Precision*Recall/(Precision+Recall)
    #Accuracy=(TP+TN)*1.0/(TP+TN+FP+FN*goodratio)

    #fout=open(destpath,'w')
    #fout.write('%s\t'%Precision+'%s\t'%Recall+'%s\t'%Fscore+'%s\n'%Accuracy)
    #print targetperm+'%s'%fold
    #print '%s\t'%Precision+'%s\t'%Recall+'%s\t'%Fscore+'%s'%Accuracy
    #fout.close()



f=open('/home/zyqu/semant2/data/22458_apps_permdict.json','r')
groundtruth=json.load(f)
f.close()

respath='/home/zyqu/semant2/evaluation/newres/'
validpath='/home/zyqu/semant2/evaluation/valiation/'

rootDir=respath
list_dirs=os.walk(rootDir)

for root, dirs, files in list_dirs:
        for d in dirs:
            targetperm=d

            #goodratio=(0.253+0.4699+0.3795)/3
            goodratio=0.253

            #if targetperm=='android.permission.READ_CONTACTS':
                #goodratio=0.4699

            #if targetperm=='android.permission.RECORD_AUDIO':
                #goodratio=0.3795

            if targetperm=='android.permission.ACCESS_COARSE_LOCATION':
                goodratio=0.32

            if targetperm=='android.permission.ACCESS_FINE_LOCATION':
                goodratio=0.36

            if targetperm=='android.permission.GET_ACCOUNTS':
                goodratio=0.16

            if targetperm=='android.permission.WRITE_EXTERNAL_STORAGE':
                goodratio=0.22


            if targetperm=='android.permission.GET_TASKS':
                goodratio=0.02

            if targetperm=='android.permission.CALL_PHONE':
                goodratio=0.1

            if targetperm=='android.permission.READ_CALL_LOG':
                goodratio=0.06

            if targetperm=='android.permission.RECEIVE_BOOT_COMPLETED':
                goodratio=0.18

            if targetperm=='android.permission.WRITE_SETTINGS':
                goodratio=0.16

            if targetperm=='android.permission.CAMERA':
                goodratio=0.20

            if targetperm=='android.permission.WRITE_CONTACTS':
                goodratio=0.20
            goodratio=1.0

            if targetperm!='android.permission.READ_CALENDAR':
                continue

            print goodratio
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
                    checkres(detectdict,validset,groundtruth,targetperm, fold, goodratio)






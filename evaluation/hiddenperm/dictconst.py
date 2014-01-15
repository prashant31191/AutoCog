#!/bin/python

import json, os


def dictcont(rootDir, validdict):
    list_dirs=os.walk(rootDir)

    for root, dirs, files in list_dirs:
        for f in files:
            fullpath=rootDir+f
            perm=f.replace('.txt','')
            perm=perm.replace('adjust_read_','')
            #print perm
            if perm not in validdict:
                validdict[perm]=[]

            fobj=open(fullpath,'r')
            for l in fobj.readlines():
                l=l.strip()
                if l.endswith('.apk') and l not in validdict[perm]:
                    validdict[perm].append(l)
            fobj.close()
            #print perm
            #print len(validdict[perm])



validdict={}


destpath='/home/zyqu/semant2/evaluation/valiation/'


first50='/home/zyqu/semant2/evaluation/hiddenperm/adj/'
last100='/home/zyqu/semant2/evaluation/hiddenperm/new100adj/'
hidden50='/home/zyqu/semant2/evaluation/hiddenperm/new50adj/'
dictcont(first50,validdict)
dictcont(last100,validdict)
dictcont(hidden50,validdict)

validdict['READ_CALENDAR']=json.load(open('/home/zyqu/semant2/evaluation/manualeval/appstoread/dataset_READ_CALENDAR1678.json','r'))
validdict['READ_CONTACTS']=json.load(open('/home/zyqu/semant2/evaluation/manualeval/appstoread/dataset_READ_CONTACTS3.json','r'))
validdict['RECORD_AUDIO']=json.load(open('/home/zyqu/semant2/evaluation/manualeval/appstoread/dataset_RECORD_AUDIO4.json','r'))

for item in validdict.keys():
    if len(validdict[item]) not in [150,166]:
        continue

    permpath=destpath+'android.permission.'+item
    command='mkdir '+permpath
    os.system(command)
    writepath=permpath+'/validset0.json'
    fw=open(permpath+'/validset0.json','w')
    print len(validdict[item])
    fw.write(json.dumps(validdict[item]))
    fw.close()

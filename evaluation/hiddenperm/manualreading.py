#!/bin/python
import json,os


proj_path=os.path.abspath('../..')

f=open('22458_apps_desctext.json','r')
desctext=json.load(f)
f.close()

f=open(proj_path+'/data/22458_apps_permdict.json','r')
permdict=json.load(f)
f.close()

counter=50
#permlst=['WRITE_EXTERNAL_STORAGE','ACCESS_FINE_LOCATION','ACCESS_COARSE_LOCATION','GET_ACCOUNTS','RECEIVE_BOOT_COMPLETED','CAMERA','WRITE_SETTINGS','WRITE_CONTACTS']
permlst=['GET_TASKS','CALL_PHONE','READ_CALL_LOG']
#permlst=['READ_SMS','SEND_SMS']
lowercounter=101



for eachperm in permlst:
    Perm='android.permission.'+eachperm
    applst=[]
    index=0
    for eachapk in permdict:
        if eachapk in desctext and Perm in permdict[eachapk] and eachapk not in applst and len(applst)<counter:
            index=index+1
            if index <= lowercounter:
                continue
            
            applst.append(eachapk)
    #print index
    f=open(proj_path+'/evaluation/hiddenperm/new50adj/adjust_read_'+eachperm+'.txt','w')
    for eachapk in applst:
            f.write(eachapk+'\n')
            f.write('%s'%desctext[eachapk]+'\n')
            f.write('\n')
    f.close()
    print len(applst)

'''



taskperm='android.permission.GET_TASKS'
setperm='android.permission.WRITE_SETTINGS'
callperm='android.permission.CALL_PHONE'
logperm='android.permission.READ_CALL_LOG'

readsmsperm='android.permission.READ_SMS'
sendsmsperm='android.permission.SEND_SMS'





tasklst=[]

temp=0

for eachapk in permdict:
    if eachapk in desctext and taskperm in permdict[eachapk] and len(tasklst)<=counter:
        tasklst.append(eachapk)

setlst=[]
for eachapk in permdict:
    if eachapk in desctext and setperm in permdict[eachapk] and eachapk not in tasklst and len(setlst)<=counter:
        setlst.append(eachapk)

calllst=[]
for eachapk in permdict:
    if eachapk in desctext and callperm in permdict[eachapk] and len(calllst)<=counter:
        calllst.append(eachapk)

loglst=[]
for eachapk in permdict:
    if eachapk in desctext and logperm in permdict[eachapk] and len(loglst)<=counter:
        loglst.append(eachapk)

readsmslst=[]
for eachapk in permdict:
    if eachapk in desctext and readsmsperm in permdict[eachapk] and len(readsmslst)<=counter:
        readsmslst.append(eachapk)


sendsmslst=[]
for eachapk in permdict:
    if eachapk in desctext and sendsmsperm in permdict[eachapk] and len(sendsmslst)<=counter:
        sendsmslst.append(eachapk)

        
print len(setlst)
print len(tasklst)


f=open('hidden_WRITESETTINGS.txt','w')
for eachapk in setlst:
    f.write(eachapk+'\n')
    f.write('%s'%desctext[eachapk]+'\n')
    f.write('\n')

f.close()


f=open('hidden_GETTASKS.txt','w')
for eachapk in tasklst:
        f.write(eachapk+'\n')
        f.write('%s'%desctext[eachapk]+'\n')
        f.write('\n')
                    
f.close()

f=open('hidden_CALL_PHONE.txt','w')
for eachapk in calllst:
        f.write(eachapk+'\n')
        f.write('%s'%desctext[eachapk]+'\n')
        f.write('\n')

f.close()


f=open('hidden_READ_CALL_LOG.txt','w')
for eachapk in loglst:
        f.write(eachapk+'\n')
        f.write('%s'%desctext[eachapk]+'\n')
        f.write('\n')
f.close()

f=open('hidden_READ_SMS.txt','w')
for eachapk in readsmslst:
        f.write(eachapk+'\n')
        f.write('%s'%desctext[eachapk]+'\n')
        f.write('\n')
f.close()



f=open('hidden_SEND_SMS.txt','w')
for eachapk in sendsmslst:
        f.write(eachapk+'\n')
        f.write('%s'%desctext[eachapk]+'\n')
        f.write('\n')
f.close()

'''

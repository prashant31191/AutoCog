#!/bin/python

import json
import os


def newgetdataset(validpath,targetperm,groundtruth):
    foldlst=[]
    if targetperm=='android.permission.READ_CONTACTS':
	foldlst.append('3')
    if targetperm=='android.permission.RECORD_AUDIO':
	foldlst.append('4')
    if targetperm=='android.permission.READ_CALENDAR':
	foldlst.extend(['1','6','7','8'])
    rootvalidpath=validpath+targetperm
    appset=[]
    for eachfold in foldlst:
	validfilename=rootvalidpath+'/validset'+eachfold+'.json'
	inputfile=open(validfilename,'r')
	validset=json.load(inputfile)
	inputfile.close()
	print validfilename
	for eachapp in validset:
		if targetperm in groundtruth[eachapp] and eachapp not in appset:
			appset.append(eachapp)
    newappset=appset[0:166]
    tempperm=targetperm.replace('android.permission.','')
    for eachfold in foldlst:
	tempperm=tempperm+eachfold
    output=file('dataset_'+tempperm+'.json','w')
    output.write(json.dumps(newappset))
    output.close()
	
	

def getdataset(ourres,willres,validset):
    #return [TPapps,FPapps,FNapps,TNapps]
    ourTP=ourres[0]
    ourFP=ourres[1]
    ourFN=ourres[2]
    ourTN=ourres[3]
    willTP=willres[0]
    willFP=willres[1]
    willFN=willres[2]
    willTN=willres[3]

    TPTP=[]
    TPFN=[]
    FNFN=[]
    FNTP=[]

    FPFP=[]
    FPTN=[]
    TNFP=[]
    TNTN=[]

    for eachapk in validset:

	if eachapk in ourTP and eachapk in willTP:
		TPTP.append(eachapk)

	if eachapk in ourTP and eachapk in willFN:
		TPFN.append(eachapk)	


	if eachapk in ourFN and eachapk in willFN:
		FNFN.append(eachapk)	

	if eachapk in ourFN and eachapk in willTP:
		FNTP.append(eachapk)

	

	if eachapk in ourFP and eachapk in willFP:
		FPFP.append(eachapk)

	if eachapk in ourFP and eachapk in willTN:
		FPTN.append(eachapk)	


	if eachapk in ourTN and eachapk in willFP:
		TNFP.append(eachapk)	

	if eachapk in ourTN and eachapk in willTN:
		TNTN.append(eachapk)



    print '\n'
    print "TPTP: %s"%len(TPTP)
    print "TPFN: %s"%len(TPFN)
    print "FNFN: %s"%len(FNFN)
    print "FNTP: %s"%len(FNTP)
    print "FPFP: %s"%len(FPFP)
    print "FPTN: %s"%len(FPTN)
    print "TNFP: %s"%len(TNFP)
    print "TNTN: %s"%len(TNTN)
    finallst=TPTP[0:10]
    print TPTP
    finallst.extend(TPFN[0:40])
    finallst.extend(FNFN[0:30])
    finallst.extend(FNTP[0:5])
    #print len(finallst)
    finallst.extend(FPFP[0:5])
    finallst.extend(FPTN[0:20])
    finallst.extend(TNFP[0:40])
    finallst.extend(TNTN[0:16])
    print len(finallst)
    final2=[]
    for eachelem in finallst:
	if eachelem not in final2:
		final2.append(eachelem)
    print len(final2)
    datafile=open('dataset_READ_CONTACT.json','w')
    datafile.write(json.dumps(final2))
    datafile.close()


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
    
    TPapps=[]
    FPapps=[]
    TNapps=[]
    FNapps=[]

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
	    TPapps.append(eachapk)
            
        
        if detectlabel==True and haslabel==False:
            FP=FP+1
            FPapps.append(eachapk)

        if detectlabel==False and haslabel==True:
            FN=FN+1
	    FNapps.append(eachapk)
            

	
        if detectlabel==False and haslabel==False:
            TN=TN+1
	    TNapps.append(eachapk)
    print "Our"
    print "%s\t"%TP+"%s\t"%FP+"%s\t"%FN+"%s"%TN
    return [TPapps,FPapps,FNapps,TNapps]






def out(perm,validpath,groundtruth,willres,targetfold):
    rootDir=validpath+perm+'/'
    list_dirs=os.walk(rootDir)
    #respath='/home/zyqu/semant2/evaluation/wiilres/'+perm
    #fout=open(respath,'w')
    for root, dirs, files in list_dirs:
        for f in files:
            filepath=rootDir+f
            input_f=open(filepath,'r')
            validset=json.load(input_f)
            input_f.close()
            fold=f.replace('validset','')
            fold=fold.replace('.json','')
	    if targetfold!=fold:
		continue
            TP=0
            FP=0
            TN=0
            FN=0
	    TPapps=[]
	    FPapps=[]
	    TNapps=[]
	    FNapps=[]
            for apk in validset:
                hasperm=perm in groundtruth[apk]
                detectperm= willres[apk]
                if hasperm==True and detectperm==True:
                    TP=TP+1
		    TPapps.append(apk)
                elif hasperm==False and detectperm==True:
                    FP=FP+1
		    FPapps.append(apk)
                elif hasperm==True and detectperm==False:
                    FN=FN+1
		    FNapps.append(apk)
                elif hasperm==False and detectperm==False:
                    TN=TN+1
		    TNapps.append(apk)
            if TP+FP==0 or TP+FN==0:
                continue
            Precision=TP*1.0/(TP+FP)
            Recall=TP*1.0/(TP+FN)
            Fscore=2*Precision*Recall/(Precision+Recall)
            Accu=(TP+TN)*1.0/(TP+TN+FP+FN)
            #fout.write('fold%s\n'%fold)
            #fout.write('%s\t'%Precision+'%s\t'%Recall+'%s\t'%Fscore+'%s\t\n'%Accu)
            #fout.write('\n')
            print "William"
	    print "%s\t"%TP+"%s\t"%FP+"%s\t"%FN+"%s"%TN
	    return [TPapps,FPapps,FNapps,TNapps]
    #fout.close()
                

            



f=open('/home/zyqu/semant2/evaluation/output_Oct05_01_48_22458_apps_desctext.txt','r')
lines=f.readlines()
f.close()

apkName=''
contactlabel=''
calendarlabel=''
audiolabel=''

contactdict={}
calendardict={}
audiodict={}

for l in lines:
    l=l.strip()
    if l.endswith('.apk'):
        apkName=l
        continue
    if len(l)==0 and len(apkName)>0 and len(contactlabel)>0 and len(calendarlabel)>0 and len(audiolabel)>0:
        if apkName not in contactdict:
            if contactlabel=='false':
                contactdict[apkName]=False
            elif contactlabel=='true':
                contactdict[apkName]=True
        
        if apkName not in calendardict:
            if calendarlabel=='false':
                calendardict[apkName]=False
            elif calendarlabel=='true':
                calendardict[apkName]=True

        if apkName not in audiodict:
            if audiolabel=='false':
                audiodict[apkName]=False
            elif audiolabel=='true':
                audiodict[apkName]=True
        apkName=''
        contactlabel=''
        calendarlabel=''
        audiolabel=''
        continue
    
    if len(l)>0 and l.find('.apk')<0:
        tokens=l.split('\t')
        contactlabel=tokens[0]
        calendarlabel=tokens[1]
        audiolabel=tokens[2]
        continue

f=open('/home/zyqu/semant2/data/22458_apps_permdict.json','r')
groundtruth=json.load(f)
f.close()

contactperm='android.permission.READ_CONTACTS'
calendarperm='android.permission.READ_CALENDAR'
audioperm='android.permission.RECORD_AUDIO'

validpath='/home/zyqu/semant2/evaluation/valiation/'





newgetdataset(validpath,audioperm,groundtruth)
'''

#targetfold='4'

#willres=out(contactperm,validpath,groundtruth,contactdict,targetfold)



respath='/home/zyqu/semant2/evaluation/newres/'
validpath='/home/zyqu/semant2/evaluation/valiation/'

rootDir=respath
list_dirs=os.walk(rootDir)



for root, dirs, files in list_dirs:
        for d in dirs:
            targetperm=d
            if targetperm!=contactperm:
                continue
            level2rootDir=os.path.join(root, d)
            newroot=rootDir+d+'/'
            new_list_dirs=os.walk(newroot)
            for Nroot, Ndirs, Nfiles in new_list_dirs:
                for Nfile in Nfiles:
                    respath=newroot+Nfile
                    detectdict=parsetxt(respath)

                    fold=Nfile.replace('newout','')
                    fold=fold.replace('.txt','')
                    if fold!=targetfold:
                        continue
                    print respath
                    validfilename=validpath+targetperm+'/validset'+fold+'.json'
                    file_in=open(validfilename,'r')
                    validset=json.load(file_in)
                    file_in.close()
                    #ourres=checkres(detectdict,validset,groundtruth,targetperm, fold)
		    #getdataset(ourres,willres,validset)

'''



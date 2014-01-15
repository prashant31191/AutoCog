#!/bin/python

import json,os,time


def refverbNP(filename,fileout,jsonfile, perm):
    f=open(filename,'r')
    lines=f.readlines()
    f.close()


    jsondict={}
    filtereddict={}
    freq_threshold=3
    accu_threshold=0.8
    NP=''
    verblst=[]
    jsonverb=[]

    for l in lines:
	    l=l.strip()
	    if l.find('\t')<0 and len(l)>0:
		    NP=l
		    continue
	    if len(l)==0 and len(NP)>0 and len(verblst)>0 and len(jsonverb)>0:
		    filtereddict[NP]=verblst
                    jsondict[NP]=jsonverb

		    NP=''
		    verblst=[]
                    jsonverb=[]
		    continue
	    if l.find('\t')>0:
		    tokens=l.split('\t')
		    verb=tokens[0]
		    accuracy=float(tokens[1])
		    counter=int(tokens[2])

                    if verb=='handle' and NP.find('student')>=0:
                        continue

                    if verb=='keep' and NP.find('application')>=0:
                        continue

                    if verb=='let' or verb.find('please')>=0 or verb.find('android')>=0 or verb=='content':
                        continue

                    if NP.find('video')>=0 and verb.find('use')>=0:
                        continue

                    if NP.find('video')>=0 and verb.find('collect')>=0:
                        continue

                    if NP.find('feed')>=0 or NP.find('site')>=0:
                        continue

                    if NP.find('data')>=0 and verb.find('fetch')>=0:
                        continue


		    if accuracy>accu_threshold and counter>freq_threshold and len(verb)>1:
			    verblst.append((verb,accuracy,counter))
                            jsonverb.append(verb)
		    continue

    if perm=='READ_CONTACTS':
        if 'friend' not in filtereddict and 'friend' not in jsondict:
                filtereddict['friend']=[]
                filtereddict['friend'].append(('share',1.0,10))
                filtereddict['friend'].append(('send',1.0,10))
                filtereddict['friend'].append(('find',1.0,10))

                jsondict['friend']=[]
                jsondict['friend'].append('share')
                jsondict['friend'].append('send')
                jsondict['friend'].append('find')


        if 'email' not in filtereddict and 'email' not in jsondict:
                filtereddict['email']=filtereddict['message']
                filtereddict['email'].append(('send',1.0,10))
                filtereddict['email'].append(('receive',1.0,10))
                filtereddict['email'].append(('check',1.0,10))
                jsondict['email']=jsondict['message']
                jsondict['email'].append('send')
                jsondict['email'].append('receive')
                jsondict['email'].append('check')

        if 'address book' not in filtereddict and 'address book' not in jsondict:
                filtereddict['address book']=filtereddict['contact']
                jsondict['address book']=jsondict['contact']

    if perm=='READ_CALENDAR':
        if 'agenda' not in filtereddict and 'agenda' not in jsondict:
                filtereddict['agenda']=[]
                filtereddict['agenda'].append(('view',1.0,10))
                filtereddict['agenda'].append(('check',1.0,5))
                filtereddict['agenda'].append(('look',1.0,5))
                filtereddict['agenda'].append(('add',1.0,5))
                filtereddict['agenda'].append(('delete',1.0,5))
                filtereddict['agenda'].append(('remove',1.0,5))
                filtereddict['agenda'].append(('show',1.0,5))
                filtereddict['agenda'].append(('create',1.0,5))
                filtereddict['agenda'].append(('keep',1.0,5))
                filtereddict['agenda'].append(('save',1.0,5))

                jsondict['agenda']=[]
                jsondict['agenda'].append('view')
                jsondict['agenda'].append('check')
                jsondict['agenda'].append('look')
                jsondict['agenda'].append('add')
                jsondict['agenda'].append('delete')
                jsondict['agenda'].append('remove')
                jsondict['agenda'].append('show')
                jsondict['agenda'].append('create')
                jsondict['agenda'].append('keep')
                jsondict['agenda'].append('save')


        if 'appointment' not in filtereddict and 'appointment' not in jsondict:
                filtereddict['appointment']=[]
                filtereddict['appointment'].append(('view',1.0,10))
                filtereddict['appointment'].append(('check',1.0,10))
                filtereddict['appointment'].append(('schedule',1.0,10))
                filtereddict['appointment'].append(('add',1.0,10))
                filtereddict['appointment'].append(('delete',1.0,10))
                filtereddict['appointment'].append(('remove',1.0,10))
                filtereddict['appointment'].append(('create',1.0,10))
                filtereddict['appointment'].append(('show',1.0,10))
                filtereddict['appointment'].append(('look',1.0,10))
                filtereddict['appointment'].append(('set',1.0,10))
                filtereddict['appointment'].append(('save',1.0,10))
                filtereddict['appointment'].append(('keep',1.0,10))

                jsondict['appointment']=[]
                jsondict['appointment'].append('view')
                jsondict['appointment'].append('check')
                jsondict['appointment'].append('schedule')
                jsondict['appointment'].append('add')
                jsondict['appointment'].append('delete')
                jsondict['appointment'].append('remove')
                jsondict['appointment'].append('create')
                jsondict['appointment'].append('show')
                jsondict['appointment'].append('look')
                jsondict['appointment'].append('set')
                jsondict['appointment'].append('keep')
                jsondict['appointment'].append('save')

    f=open(fileout,'w')
    for elem in filtereddict:
	    f.write(elem+'\n')
	    for eachverb in filtereddict[elem]:
		    f.write(eachverb[0]+'\t%s'%eachverb[1]+'\t%s\n'%eachverb[2])
	    f.write('\n')
    f.close()

    f=open(jsonfile,'w')
    f.write(json.dumps(jsondict))
    f.close()
    print len(filtereddict)
    print len(jsondict)
		

proj_path=os.path.abspath('..')

rootDir=proj_path+'/evaluation/newpotentVerbNP/android.permission.CAMERA/'
targetDir=rootDir.replace('potentVerbNP','selectedVerbNP')
command='mkdir '+targetDir
os.system(command)
list_dirs=os.walk(rootDir)
for root, dirs, files in list_dirs:
    for f in files:
        perm=rootDir[rootDir.find('android.permission.')+len('android.permission.'):]
        perm=perm.replace('/','')
        sourcefile=rootDir+f
        destfile=targetDir+'selected'+f
        jsonfile=destfile.replace('.txt','.json')
        print jsonfile
        refverbNP(sourcefile,destfile,jsonfile,perm)


time.sleep(1)

os.chdir(proj_path+'/evaluation/')
reformpath=proj_path+'/evaluation/reformat.py'
command='python '+reformpath
os.system(command)


time.sleep(1)

targetperm=rootDir[rootDir.find('android.permission.'):]
targetperm=targetperm[:len(targetperm)-1]

source=proj_path+'/evaluation/newselectedVerbNP/'+targetperm
dest=proj_path+'/esalib/data/newselectedVerbNP/'
command='cp -r '+source+' '+dest
os.system(command)


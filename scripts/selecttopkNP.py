#!/bin/python


import json,os





def gettopk(lst,k):
    newlst=[]
    for elemindex in range(len(lst)):
        if elemindex >= k:
            break
        newlst.append(lst[elemindex][0])
    return newlst



proj_path=os.path.abspath('..')
potentNPpath=proj_path+'/evaluation/potentNP/'
selectedNPpath=proj_path+'/evaluation/topkNP/'


rootDir=potentNPpath
list_dirs=os.walk(rootDir)

for root, dirs, files in list_dirs:
    for d in dirs:
        level2rootDir=os.path.join(root, d)
        newroot=rootDir+d+'/'
        new_list_dirs=os.walk(newroot)
        #print d
        #if d!='android.permission.WRITE_SETTINGS':
            #continue
        for Nroot, Ndirs, Nfiles in new_list_dirs:
            for Nfile in Nfiles:
                filefullpath=os.path.join(Nroot,Nfile)
                filename=os.path.basename(filefullpath)
                if filename.find('.json')<0:
                    continue
                #print filefullpath
                fold=filename.replace('NPfold','')
                fold=fold.replace('.json','')
                #print fold
                f=open(filefullpath,'r')
                x=json.load(f)
                f.close()
                newNPdict={}
                targetPerm=x.keys()[0]
                #print targetPerm
                #print len(x[targetPerm])
                newNPdict[targetPerm]=gettopk(x[targetPerm], 250)
                #print len(x[targetPerm])
                command='mkdir '+selectedNPpath+targetPerm
                os.system(command)
                despath=selectedNPpath+targetPerm+'/selectedNPfold'+fold+'.json'
                f=open(despath,'w')
                f.write(json.dumps(newNPdict))
                f.close()
                print targetPerm
                #print despath
                print len(newNPdict[targetPerm])







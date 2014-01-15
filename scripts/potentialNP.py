#!/usr/bin/python

import os, json, subprocess,time
import shlex
from operator import mul
import nltk
import string
import xml.dom.minidom

#from nltk.stem.wordnet import WordNetLemmatizer
#list of stop words	
filteredlist=['yes','no','true','false','thank','thanks','null','error','none','success','default','array','version','use','dot','unknown','valid','invalid','byte','result','other','code','debug','token','integer','medium','are','has','have','nan','male','female','gender','bse','want','sorry','phd', 'a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you','de','plus']

replacedict={'advertisement' : ['ad','ads','advertising','advertisements','advertiser'], 
		     'wifi' : ['wi-fi'],
		     'message' : ['sm','sms','messager'],
		     'email': ['e-mail'],		
		     'information' : ['info',],
		     'notification' : ['notify','notifys'],
		     'photo' : ['photograph','photography','picture','pic','pics'],
		     'application' : ['app','applications'],
		     '' : ['e.g','e.g.', 'yes', 'no',  'true', 'false', 'thank',
'thanks','null','error','none','success','default','array','version','use','dot','unknown','valid','invalid','byte','result','other','code','debug','token','integer','medium','are','has','have','nan','male','female','gender','bse','want','sorry','phd', 'a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you','isnt','.com','wouldn','red','blue','pink','purple','black','green','orange','don']
}

class Map:
  def __init__(self):
    pass


#keyworddict: appName -> listofkeywords 
#permissiondict: appName -> listofpermissions
#the frequecy of each pair of keywords given a permission
  def getcombokwfreq(self,keyworddict,permissiondict):
    permlist=[]
    maindict={}
    pmdict={}

#the times a permission found
    threshold=5

    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in pmdict:
			pmdict[elem]=1
		elif elem in pmdict:
			pmdict[elem]=pmdict[elem]+1


    for pmkey in pmdict:
	if pmdict[pmkey]>threshold:
		permlist.append(pmkey)


    loopall=len(permlist)
    loopcount=1
    for elem in permlist:
	print 'Loop: %s'%loopcount+'/%s'%loopall
	loopcount=loopcount+1
	kwlist=[]
	totalcount=0
	kwmap={}
	orderedlist=[]
	for apkname in permissiondict:
		if elem in permissiondict[apkname]:
			totalcount=totalcount+1
			for eachkw in keyworddict[apkname]:
				if eachkw not in kwlist:
					kwlist.append(eachkw)

        n=len(kwlist)
        iterations=reduce(mul, range(1,n+1))/2/reduce(mul, range(1,n-2+1))
	
        print 'Number of iterations: %s'%iterations

	for i in range(len(kwlist)-1):
		for j in range(i+1,len(kwlist)):
			targetkw1=kwlist[i]
			targetkw2=kwlist[j]
			for keyapk in permissiondict:
				if elem in permissiondict[keyapk]:
					if (targetkw1 in keyworddict[keyapk]) and (targetkw2 in keyworddict[keyapk]):
						if ((targetkw1+', '+targetkw2) not in kwmap):
							kwmap[targetkw1+', '+targetkw2]=1
						elif ((targetkw1+', '+targetkw2) in kwmap):
							kwmap[targetkw1+', '+targetkw2]=kwmap[targetkw1+', '+targetkw2]+1


	for kperm in kwmap:
		kwmap[kperm]=(kwmap[kperm]*100.0)/totalcount

	orderedlist=sorted(kwmap.iteritems(), key=lambda d:d[1], reverse=True)
	maindict[elem]=orderedlist
						
    file_op1=open('combokwFREQ.txt','w')
    try:
	for k in maindict:
		file_op1.write(k)
		file_op1.write('\n')
		for v in maindict[k]:
			file_op1.write(v)
			file_op1.write('\n')
		file_op1.write('\n')

    except:
	print "Errors in writing file combokwFREQ.txt"
    finally:
	file_op1.close()


#the frequecy of each permission given a pair of keywords
  def getcombopermfreq(self,keyworddict,permissiondict):
    threshold=1
    combothreshold=2
    kwdict={}
    maindict={}

    for (k,v) in keyworddict.iteritems():
	for elem in v:
		if elem not in kwdict:
			kwdict[elem]=1
		elif elem in kwdict:
			kwdict[elem]=kwdict[elem]+1

    kwlist=[]
    for kkey in kwdict:
	if kwdict[kkey]>threshold:
		kwlist.append(kkey)

    n=len(kwlist)
    loopall=reduce(mul, range(1,n+1))/2/reduce(mul, range(1,n-2+1))
    loopcount=1
    file_op2=open('combopermissionFREQ.txt','w')
    try:
    	for i in range(len(kwlist)-1):
		for j in range(i+1,len(kwlist)):
	        	print 'Loop: %s'%loopcount+'/%s'%loopall
			loopcount=loopcount+1	
			targetkw1=kwlist[i]
			targetkw2=kwlist[j]
			permissionmap={}
			orderedlist=[]
			totalcount=0
			for targetapp in keyworddict:
				if (targetkw1 in keyworddict[targetapp]) and (targetkw2 in keyworddict[targetapp]):
					totalcount=totalcount+1
					for pm in permissiondict[targetapp]:
						if pm not in permissionmap:
							permissionmap[pm]=1
						elif pm in permissionmap:
							temp=permissionmap[pm]
							permissionmap[pm]=temp+1

			if totalcount >= combothreshold:
				for kperm in permissionmap:
					tempcoun=permissionmap[kperm]
					permissionmap[kperm]=(permissionmap[kperm]*100.0)/totalcount
					if permissionmap[kperm] > 100:
						print 'XXXXXXXXXXXXXXXX Error! XXXXXXXXXXXXXXXXXX'
						print permissionmap[kperm]
						print tempcoun
						print totalcount

				orderedlist=sorted(permissionmap.iteritems(), key=lambda d:d[1], reverse=True)
				maindict[targetkw1+', '+targetkw2]=orderedlist
				file_op2.write(targetkw1+', '+targetkw2)
				file_op2.write('\n')
				for v in orderedlist:
					file_op2.write(v[0])
					file_op2.write(', ')
					file_op2.write('%s'%v[1])
					file_op2.write('\n')
				file_op2.write('\n')
				file_op2.flush()
			
    except:
    	print "Errors in writing file combopermissionFREQ.txt"

    finally:
    	file_op2.close()
    #return maindict
						

  def combovariation(self,keyworddict,permissiondict,pmdict):
    threshold=1
    kwdict={}
    for (k,v) in keyworddict.iteritems():
	for elem in v:
		if elem not in kwdict:
			kwdict[elem]=1
		elif elem in kwdict:
			kwdict[elem]=kwdict[elem]+1

    kwlist=[]
    for kkey in kwdict:
	if kwdict[kkey]>threshold:
		kwlist.append(kkey)
    print 'How many keywords?\n%s'%len(kwlist)

    file_op2=open('combokwmatchperms.txt',"w")
    file_op3=open('combokwstep.txt',"w")
    file_op4=open('combokwindex.txt',"w")
    try:
	finalresnum=0
	combothreshold=2
	loopcount=1
	n=len(kwlist)
	totalcount=reduce(mul, range(1,n+1))/2/reduce(mul, range(1,n-2+1))
    	for i in range(len(kwlist)-1):
		for j in range(i+1,len(kwlist)):
			print 'Loop: %s'%loopcount+'/%s'%totalcount
			stepsize=0
			targetkw1=kwlist[i]
			targetkw2=kwlist[j]
			targetpermissions={}


			for targetapp in keyworddict:
				if (targetkw1 in keyworddict[targetapp]) and (targetkw2 in keyworddict[targetapp]):
					stepsize=stepsize+1
					targetpermissions[stepsize]=permissiondict[targetapp]
			
			

			if stepsize >= combothreshold:
				
				for keynum in targetpermissions:
					for valperm in targetpermissions[keynum]:
						file_op2.write('%s'%pmdict[valperm])
						file_op2.write('	')
					file_op2.write('\n')
				#file_op2.write('\n')

				file_op3.write('%s'%stepsize)
				file_op3.write('\n')

				file_op4.write(targetkw1+', '+targetkw2)
				file_op4.write('\n')
				finalresnum=finalresnum+1


			if stepsize < combothreshold:
				print 'Only %s samples'%stepsize+' less than %s'%combothreshold
			loopcount=loopcount+1
		
    except:
	print 'faile to write files combokwmatchperms.txt / combokwstep.txt / combokwindex.txt'

    finally:
	file_op2.close()
	file_op3.close()
	file_op4.close()
	print 'Number of keywords: %s'%finalresnum
		


  def getpermindex(self, permissiondict):
    permorder=1
    pmdict={}
    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in pmdict:
			pmdict[elem]=permorder
			permorder=permorder+1


    print pmdict
    print len(pmdict)
    file_op=open('varpermindex.txt',"w")
    try:
	orderedlist=sorted(pmdict.iteritems(), key=lambda d:d[1], reverse=False)
	print orderedlist
	for index in range(0,len(pmdict)):
		file_op.write(orderedlist[index][0]+'\n')
    except:
	print "Errors in writing file varpermindex"
    finally:
	file_op.close()

    return pmdict

#given each keyword, calculate the variation of permissions, need to be used with Matlab,
#pmdict: permission -> index
  def variation(self,keyworddict,permissiondict,pmdict):
    threshold=35
    kwdict={}
    for (k,v) in keyworddict.iteritems():
	for elem in v:
		if elem not in kwdict:
			kwdict[elem]=1
		elif elem in kwdict:
			kwdict[elem]=kwdict[elem]+1

    kwlist=[]
    for kkey in kwdict:
	if kwdict[kkey]>threshold:
		#print kwdict[kkey]
		#print threshold
		#print '\n'
		kwlist.append(kkey)
    #print 'How many keywords?\n%s'%len(kwlist)
    file_op2=open('kwmatchperms.txt',"w")
    file_op3=open('kwstep.txt',"w")
    file_op4=open('kwindex.txt',"w")
    try:
	loopcount=0
    	for elem in kwlist:
		loopcount=loopcount+1
		print 'Loop: %s'%loopcount+' in %s'%len(kwlist)
		stepsize=0
		for (k,v) in keyworddict.iteritems():
			for targetkw in v:
				if targetkw==elem:
					permissions=permissiondict[k]
					for targetperm in permissions:
						file_op2.write('%s'%pmdict[targetperm])
						file_op2.write('	')
					file_op2.write('\n')
					stepsize=stepsize+1
		file_op3.write('%s'%stepsize)
		file_op3.write('\n')
		file_op4.write(elem)
		file_op4.write('\n')
    except:
	print 'faile to write files kwmatchperms.txt / kwstep.txt / kwindex.txt'
    finally:
	file_op2.close()
	file_op3.close()
	file_op4.close()


  def combochisquare(self,keyworddict,permissiondict,permdict):
    permlist=[]
    maindict={}
    pmdict={}
#the times a permission found
    threshold=5

    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in pmdict:
			pmdict[elem]=1
		elif elem in pmdict:
			pmdict[elem]=pmdict[elem]+1

    for pmkey in pmdict:
	if pmdict[pmkey]>threshold:
		permlist.append(pmkey)    

    loopall=len(permlist)
    loopcount=1
    for elem in permlist:
	print 'Loop: %s'%loopcount+'/%s'%loopall
	chisqlist=[]
	loopcount=loopcount+1
	kwlist=[]
	kwmap={}
	for apkname in permissiondict:
		if elem in permissiondict[apkname]:
			for eachkw in keyworddict[apkname]:
				if eachkw not in kwlist:
					kwlist.append(eachkw)

        n=len(kwlist)
        iterations=reduce(mul, range(1,n+1))/2/reduce(mul, range(1,n-2+1))
        print 'Number of iterations: %s'%iterations

	for i in range(len(kwlist)-1):
		for j in range(i+1,len(kwlist)):
			targetkw1=kwlist[i]
			targetkw2=kwlist[j]
			a=0
			b=0
			c=0	
			d=0
			for targetapk in permissiondict:
				if (elem in permissiondict[targetapk]) and ((targetkw1 in keyworddict[targetapk]) and (targetkw2 in keyworddict[targetapk])):
					a=a+1
					continue
				if (elem in permissiondict[targetapk]) and ((targetkw1 not in keyworddict[targetapk]) or (targetkw2 not in keyworddict[targetapk])):
					b=b+1
					continue
				if (elem not in permissiondict[targetapk]) and ((targetkw1 in keyworddict[targetapk]) and (targetkw2 in keyworddict[targetapk])):
					c=c+1
					continue
				if (elem not in permissiondict[targetapk]) and ((targetkw1 not in keyworddict[targetapk]) or (targetkw2 not in keyworddict[targetapk])):
					d=d+1
					continue

			if (a+b+c+d)>40:
				chisq=(a+b+c+d)* (abs(a*d-b*c)-0.5*(a+b+c+d)) * (abs(a*d-b*c)-0.5*(a+b+c+d)) *1.0/(a+b)/(c+d)/(b+d)/(a+c)
			if (a+b+c+d)<=40:
				chisq=(a+b+c+d)*(a*d-b*c)*(a*d-b*c)*1.0/(a+b)/(c+d)/(b+d)/(a+c)
			chisqlist.append(chisq)
	maindict[elem]=chisqlist

    return maindict

#chi-square analysis of permission and keyword
  def chisquare(self,keyworddict,permissiondict):
    threshold=20
    chisqthres=6.635
    pmdict={}
    permlist=[]  
    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in pmdict:
			pmdict[elem]=1
		elif elem in pmdict:
			pmdict[elem]=pmdict[elem]+1
    for pmkey in pmdict:
	if pmdict[pmkey]>threshold:
		permlist.append(pmkey)

    permkeydict={}   

    for elem in permlist:
	
	permkeylist=[]
	keywordmap={}
	for (k,v) in permissiondict.iteritems():
		for perm in v:
			if perm==elem:
				thiskeywords=keyworddict[k]
				for kw in thiskeywords:
					if kw not in keywordmap:
						keywordmap[kw]=1
					elif kw in keywordmap:
						keywordmap[kw]=keywordmap[kw]+1
	for kw in keywordmap:
		permkeylist.append(kw)

	permkeydict[elem]=permkeylist

    maindict={}
    print 'Ready to Go!'
    loopcount=1

    chisqkw=open('chisqkeywordres.txt',"w")


    for (targetperm,v) in permkeydict.iteritems():
	print 'Loop: %s'%loopcount+'/%s'%len(permkeydict)
	loopcount=loopcount+1
        chisqlist=[]
	print 'Number of keywords: %s'%len(v)

	chisqkw.write(targetperm)
	chisqkw.write('\n')

	for targetkw in v:
		a=0
		b=0
		c=0
		d=0
		for apkname in permissiondict:
			if ((targetperm in permissiondict[apkname]) and (targetkw in keyworddict[apkname])):
				a=a+1
				continue
			if ((targetperm in permissiondict[apkname]) and (targetkw not in keyworddict[apkname])):
				b=b+1
				continue
			if ((targetperm not in permissiondict[apkname]) and (targetkw in keyworddict[apkname])):
				c=c+1
				continue
			if ((targetperm not in permissiondict[apkname]) and (targetkw not in keyworddict[apkname])):
				d=d+1
				continue
		if (a+b+c+d)>40:
			chisq=(a+b+c+d)* (abs(a*d-b*c)-0.5*(a+b+c+d)) * (abs(a*d-b*c)-0.5*(a+b+c+d)) *1.0/(a+b)/(c+d)/(b+d)/(a+c)
		if (a+b+c+d)<=40:
			chisq=(a+b+c+d)*(a*d-b*c)*(a*d-b*c)*1.0/(a+b)/(c+d)/(b+d)/(a+c)

		chisqlist.append(chisq)

		if chisq>chisqthres:
			chisqkw.write(targetkw+', a=%s'%a+', b=%s'%b+', c=%s'%c+', d=%s'%d)
			chisqkw.write('\n')

	chisqkw.write('\n')
	chisqkw.flush()
	maindict[targetperm]=chisqlist


    chisqkw.close()		
    return maindict		

#given a keyword, get the frequency of permissions		
  def getpermissionfrequency(self,keyworddict,permissiondict):
	# --> <keyword1,[(permmission1,freq1),...]>
    kwdict={}
    kwcount=0
    maindict={}
	#the times a key word is found
    threshold=35

    for (k,v) in keyworddict.iteritems():
	for elem in v:
		if elem not in kwdict:
			kwdict[elem]=1
		elif elem in kwdict:
			kwdict[elem]=kwdict[elem]+1

    kwlist=[]
    for kkey in kwdict:
	if kwdict[kkey]>threshold:
		kwlist.append(kkey)
		kwcount=kwcount+1
    #print kwcount

    loopcount=1
    for elem in kwlist:
	
	permissionmap={}
	orderedlist=[]
	#print "In function getpermissionfrequency() Loop: %s"%loopcount+'/%s'%len(kwlist)
	loopcount=loopcount+1
	for (k,v) in keyworddict.iteritems():
		for targetkw in v:
			if elem==targetkw:
				thispermisions=permissiondict[k]
				for pm in thispermisions:
					if pm not in permissionmap:
						permissionmap[pm]=1
					elif pm in permissionmap:
						permissionmap[pm]=permissionmap[pm]+1

	for kperm in permissionmap:
		permissionmap[kperm]=(permissionmap[kperm]*100.0)/kwdict[elem]

	orderedlist=sorted(permissionmap.iteritems(), key=lambda d:d[1], reverse=True)
	maindict[elem]=orderedlist

    return maindict


  def reversepermissionfreq(self,kwpermfreqdict,kwfilterlist):
	pmlist=[]
	for targetkw in kwpermfreqdict:
		for permfreq in kwpermfreqdict[targetkw]:
			if permfreq[0] not in pmlist: #permfreq[0] is permission and permfreqp[1] is freq
				pmlist.append(permfreq[0])
			elif permfreq[0] in pmlist:
				continue
	
	permkwfreqdict={}
	for targetperm in pmlist:
		tempdict={}
		for targetkw in kwpermfreqdict:
			if targetkw not in kwfilterlist:
				continue
			for permfreq in kwpermfreqdict[targetkw]:
				if permfreq[0]==targetperm:
					tempdict[targetkw]=permfreq[1]
		permkwfreqdict[targetperm]=sorted(tempdict.iteritems(), key=lambda d:d[1], reverse=True)	

	file_op1=open("reversepermfreq.txt",'w')
	try:
		for perm in permkwfreqdict:
			file_op1.write(perm+'\n')
			for elem in permkwfreqdict[perm]:
				file_op1.write(elem[0]+', %s\n'%elem[1])
			file_op1.write('\n')
	except:
		print "Errors in writing file reversepermfreq.txt"
	finally:
		file_op1.close()
		return permkwfreqdict
				
			

  def reversekwfreq(self, permkwfreqdict):

	kwlist=[]
	for targetperm in permkwfreqdict:
		for kwfreq in permkwfreqdict[targetperm]:
			if kwfreq[0] not in kwlist:
				kwlist.append(kwfreq[0])
			elif kwfreq[0] in kwlist:
				continue


	kwpermfreqdict={}
	for targetkw in kwlist:
		tempdict={}
		for targetperm in permkwfreqdict:
			for kwfreq in permkwfreqdict[targetperm]:
				if kwfreq[0]==targetkw:
					tempdict[targetperm]=kwfreq[1]
		kwpermfreqdict[targetkw]=sorted(tempdict.iteritems(), key=lambda d:d[1], reverse=True)


	file_op1=open("reversekwfreq.txt",'w')
	try:
		for kw in kwpermfreqdict:
			file_op1.write(kw+'\n')
			for elem in kwpermfreqdict[kw]:
				file_op1.write(elem[0]+', %s\n'%elem[1])
			file_op1.write('\n')
	except:
		print "Errors in writing file reversekwfreq.txt"
	finally:
		file_op1.close()
		return kwpermfreqdict
	
				

#given a permission, get the frequency of each keyword
  def getkeywordfrequency(self,keyworddict,permissiondict):

	# --> <permission1,[(keyword1,freq1),...]>
    permlist=[]
    kwlist=[]
    maindict={}
    pmdict={}
    kwdict={}

#the times a keyword found
    kwthreshold=35


    for (k,v) in keyworddict.iteritems():
	for elem in v:
		if elem not in kwdict:
			kwdict[elem]=1
		elif elem in kwdict:
			kwdict[elem]=kwdict[elem]+1

    for kwkey in kwdict:
	if kwdict[kwkey]>kwthreshold:
		kwlist.append(kwkey)

#the times a permission found
    permthreshold=20

    for (k,v) in permissiondict.iteritems():
	for elem in v:
		if elem not in pmdict:
			pmdict[elem]=1
		elif elem in pmdict:
			pmdict[elem]=pmdict[elem]+1


    for pmkey in pmdict:
	if pmdict[pmkey]>permthreshold:
		permlist.append(pmkey)


    for elem in permlist:

        #totalthisperm=0
	keywordmap={}
	orderedlist=[]	

	for (k,v) in permissiondict.iteritems():
		for perm in v:
			if perm==elem:
				thiskeywords=keyworddict[k]
				for kw in thiskeywords:
					if kw in kwlist:
						if kw not in keywordmap:
							keywordmap[kw]=1
						elif kw in keywordmap:
							keywordmap[kw]=keywordmap[kw]+1

	for kkey in keywordmap:
		keywordmap[kkey]= (keywordmap[kkey]*100.0)/pmdict[elem]

	maindict[elem]=sorted(keywordmap.iteritems(), key=lambda d:d[1], reverse=True)
	
    file_op=open('permkwfreq.txt','w')
    try:
	for perm in maindict:
		file_op.write(perm+'\n')
		for keyword in maindict[perm]:
			file_op.write(keyword[0]+', %s\n'%keyword[1])
		file_op.write('\n')
    except:
	print "Errors in writing file permkwfreq.txt"
    finally:
	file_op.close()
    return maindict
	
#extracted the resulted from Alchemy API (sourcepath)	 					
  def getkeyword(self,sourcepath, permissiondict):
    file_object=open(sourcepath)
    count=0

    try:
    	alllines = file_object.readlines()
        maindict={}
	apkname=''
	keywords=[]
	for line in alllines:
		line=line.strip()
		if line.find('.apk.apk')>0:
			line=line.replace('.apk.apk','.apk')
			apkname=line
			continue
		if len(line)==0:
			if len(apkname)>0 and (apkname not in maindict) and len(keywords)>0:
				maindict[apkname]=keywords
				count=count+1
			keywords=[]
			apkname=''
			continue
		keywords.append(line.lower())
    finally:
        file_object.close()
	kwdict={}
	for kkey in maindict:
		if kkey in permissiondict:
			kwdict[kkey]=maindict[kkey]
	keywordlist=[]
	for elem in kwdict:
		for eachkw in kwdict[elem]:
			if eachkw not in keywordlist:
				keywordlist.append(eachkw)
	print "Numebr of keywords: %s"%len(keywordlist)    	
	return kwdict
	

#old version of function getkeyword(...)
  def getkeyword2(self,sourcepath):
    file_object=open(sourcepath)
    count=0
    count2=0

    try:
    	alllines = file_object.readlines()
        maindict={}
	apkname=''
	keywords=[]
	for line in alllines:
		line=line.strip()
		if line.find('.apk.apk')>0:
			line=line.replace('.apk.apk','.apk')
			apkname=line
			continue
		if len(line)==0:
			if len(apkname)>0 and (apkname not in maindict) and len(keywords)>0:
				maindict[apkname]=keywords
				count=count+1
			elif len(keywords)==0 and len(apkname)>0:
				count2=count2+1
				
			keywords=[]
			apkname=''
			continue
		keywords.append(line.lower())
    finally:
        file_object.close()
	
	templist=[]
	for apkname in maindict:
		for targetkw in maindict[apkname]:
			if targetkw not in templist:
				templist.append(targetkw)
	#print "Length of templist: %s"%len(templist)
	#print "Number of apps in kwdict: %s"%len(maindict)
	#print "Number of empty apps: %s"%count2
    	return maindict

#refine the keywords
  def keywordrefine(self,keyworddict):
    from nltk.stem.wordnet import WordNetLemmatizer
    lmtzr = WordNetLemmatizer()
    kwdict={}
    threshold=5

    for (k,v) in keyworddict.iteritems():
	for elem in v:
		if elem not in kwdict:
			kwdict[elem]=1
		elif elem in kwdict:
			kwdict[elem]=kwdict[elem]+1

    kwlist=[]
    for kkey in kwdict:
	if kwdict[kkey]>threshold:
		kwlist.append(kkey)

	
    maindict={}
    for apkname in keyworddict:
	#print apkname
	refinedkwlist=[]
	for targetkw in keyworddict[apkname]:
		if (targetkw not in kwlist) or (not targetkw.isalnum()):
			continue
		#flag=False
		#for char in targetkw:
			#flag=flag or char.isalnum()
		#if flag==False:
			#continue

		elif targetkw in kwlist:
			targetkw=targetkw.strip()
			#print targetkw
			while not targetkw[len(targetkw)-1].isalnum():
				targetkw=targetkw[:len(targetkw)-1]

			targetkw=lmtzr.lemmatize(targetkw)
			targetkw=lmtzr.lemmatize(targetkw,'v')

			targetkw=targetkw.replace('apps','app')


			if targetkw not in refinedkwlist:
				refinedkwlist.append(targetkw)

	if len(refinedkwlist)>0 and (apkname not in maindict):
		maindict[apkname]=refinedkwlist
    file_op=open('refinedkws','w')
    try:
	for key in maindict:
		file_op.write(key)
		file_op.write('\n')
		for elem in maindict[key]:
			file_op.write(elem)
			file_op.write('\n')
		file_op.write('\n')
    except: 
	print "Errors in writing refinedkws"
    finally:
	file_op.close()

    return maindict
			

  def parseperm(self,filename):
    file_in=open(filename)
    maindict={}
    
    try:
	alllines=file_in.readlines()
	appname=''
	permlist=[]
	for line in alllines:
		line=line.strip()
		if line.find('.apk')>0:
			appname=line
			continue
		elif len(line)==0 and len(appname)>0 and len(permlist)>0:
			maindict[appname]=permlist
			appname=''
			permlist=[]
			continue
		permlist.append(line)
    finally:
	file_in.close()
	return maindict

#get the permissions of each app, which is results output from Stowaway. Resolve the problem of over-priviliage
  def getperm(self,sourcepath): 
    maindict={}
    rootDir=sourcepath
    list_dirs=os.walk(rootDir)
    count=0
    for root, dirs, files in list_dirs:
	for d in dirs:       
        	level2rootDir=os.path.join(root, d)
		appname=os.path.basename(level2rootDir)
		if appname.find('.apk')==(len(appname)-4):
			list_files=os.walk(level2rootDir)
			fileslist=[]
			origpermissions=[]
			ourpermissions=[]
			overpermissions=[]
			underpermissions=[]
			for root2, dirs2, files2 in list_files:
				for f in files2:
					filename=os.path.join(root2,f)
					filebasename=os.path.basename(filename)
					fileslist.append(filebasename)
					print filename
					
					if filebasename =='orig':
						file_object=open(filename)
						try:
							alllines = file_object.readlines()
							for line in alllines:
								line=line.strip()
								ContainOr=1
								if line.find(' or ')==-1:
									ContainOr=0
									if (line not in origpermissions) and line != 'NONE':
										origpermissions.append(line)
										continue

								first='XXXX'
								remain=line
								while ContainOr==1:
									first=remain[:remain.find(' or ')]
									remain=remain[remain.find(' or ')+4:]
									if (first not in origpermissions) and first!='NONE':
										origpermissions.append(first)
									if remain.find(' or ')<0:
										ContainOr=0
										break
								if (remain not in origpermissions) and remain!='NONE':
									origpermissions.append(remain)
						except:
							print 'fail to open '+filename

						finally:
							file_object.close()

					if filebasename =='OurPermissions':
						file_object=open(filename)
						try:
							alllines = file_object.readlines()
							for line in alllines:
								line=line.strip()
								ContainOr=1
								if line.find(' or ')==-1:
									ContainOr=0
									if (line not in ourpermissions) and line != 'NONE':
										ourpermissions.append(line)
										continue

								first='XXXX'
								remain=line
								while ContainOr==1:
									first=remain[:remain.find(' or ')]
									remain=remain[remain.find(' or ')+4:]
									if (first not in ourpermissions) and first!='NONE':
										ourpermissions.append(first)
									if remain.find(' or ')<0:
										ContainOr=0
										break
								if (remain not in ourpermissions) and remain!='NONE':
									ourpermissions.append(remain)

						except:
							print 'fail to open '+filename

						finally:
							file_object.close()
					if filebasename =='Overprivilege':
						file_object=open(filename)
						try:
							alllines = file_object.readlines()
							for line in alllines:
								line=line.strip()
								if (line not in overpermissions) and line != 'NONE':
									overpermissions.append(line)
						except:
							print 'fail to open '+filename

						finally:
							file_object.close()
					if filebasename =='Underprivilege':
						file_object=open(filename)
						try:
							alllines = file_object.readlines()
							for line in alllines:
								line=line.strip()
								ContainOr=1
								if line.find(' or ')==-1:
									ContainOr=0
									if (line not in underpermissions) and line != 'NONE':
										underpermissions.append(line)
										continue

								first='XXXX'
								remain=line
								while ContainOr==1:
									first=remain[:remain.find(' or ')]
									remain=remain[remain.find(' or ')+4:]
									if (first not in underpermissions) and first!='NONE':
										underpermissions.append(first)
									if remain.find(' or ')<0:
										ContainOr=0
										break
								if (remain not in underpermissions) and remain!='NONE':
									underpermissions.append(remain)
						except:
							print 'fail to open '+filename


						finally:
							file_object.close()

			if 'AndroidManifest.xml' in fileslist and (len(origpermissions)>0 or len(ourpermissions)>0):
				finalpermissions=[]
				for elem in ourpermissions:
					if (elem in underpermissions) or (elem in origpermissions):
						finalpermissions.append(elem)
				if appname not in maindict:
					maindict[appname]=finalpermissions
					count=count+1

    #print len(maindict)

    return maindict


#get the category of each app
  def getcate(self, path): 
    catedict={
		"BOOKS_AND_REFERENCE": 1, 
		"BUSINESS" : 2, 
		"COMICS": 3,
		"COMMUNICATION" : 4,
		"EDUCATION" : 5, 
		"ENTERTAINMENT" : 6, 
		"FINANCE" : 7,
        	"HEALTH_AND_FITNESS" : 8, 
		"LIBRARIES_AND_DEMO" : 9, 
		"LIFESTYLE" : 10, 
		"APP_WALLPAPER" : 11, 
		"MEDIA_AND_VIDEO" : 12, 
		"MEDICAL" : 13,
	        "MUSIC_AND_AUDIO" : 14, 
		"NEWS_AND_MAGAZINES" : 15, 
		"PERSONALIZATION" : 16, 
		"PHOTOGRAPHY" : 17, 
		"PRODUCTIVITY" : 18, 
		"SHOPPING" : 19, 
		"SOCIAL" : 20,
	        "SPORTS" : 21, 
		"TOOLS" : 22, 
		"TRANSPORTATION" : 23, 
		"TRAVEL_AND_LOCAL" : 24, 
		"WEATHER" : 25, 
		"APP_WIDGETS" : 26, 
		"ARCADE" : 27, 
		"BRAIN" : 28, 
		"CARDS" : 29,
	        "CASUAL": 30, 
		"GAME_WALLPAPER" : 31, 
		"RACING" : 32, 
		"SPORTS_GAMES" : 33, 
		"GAME_WIDGETS": 34}	
	
    maindict = {}
    list_dirs = os.walk(path) 
    package=''
    category=''


    for root, dirs, files in list_dirs: 
    	for f in files:
    		filepath=os.path.join(root, f)
    		if filepath.find("meta")>=0 and filepath.find("WIDGETS")<0:
    			file_object=open(filepath)
    			try:
   				alllines = file_object.readlines()
    				for line in alllines:
					line=line.strip()
					if line.find("packageName:")>=0: 
						line = line[len("packageName:\"")+1: ]
						package = line[: len(line)-1]
						package=package+'.apk'
						if (package not in maindict) and len(package)>0:
							category=filepath[filepath.find('meta_')+len('meta_'):filepath.find('.txt')]
							maindict[package]=catedict[category]
							continue

			finally:
				file_object.close()
   
    return maindict

#get the description of each app, put in 4 files separately. To be handled with Alchemy API or Tf-idf
  def getdesc(self,path):
	maindict = {}
	list_dirs = os.walk(path) 
	i=0
	j=0
	k=0
	speclist=[]
	desc=''
	package=''
	while i<10:
		while j<10:
			while k<10:
				speclist.append('\\'+'%s'%i+'%s'%j+'%s'%k)
				k=k+1
			k=0
			j=j+1				
		j=0
		i=i+1

	for root, dirs, files in list_dirs: 
		for f in files:
			filepath=os.path.join(root, f)
			if filepath.find("meta")>=0 and filepath.find("WIDGETS") <0 and filepath.find("GAME") < 0:
				file_object=open(filepath)
				try:
					alllines = file_object.readlines()
					for line in alllines:
						if line.find("description:")>=0:
							if (package not in maindict) and len(package)>0:# and len(desc)>0:
								maindict[package]=desc
							package=''
							desc=''
								
							line=line.strip()
							line = line[len("description:\"")+1: ]
							desc = line[: len(line)-1]
							for eachspecwd in speclist:
								desc=desc.replace(eachspecwd,'')

							desc=desc.replace('\\n','DELIMITXXX')
							desc=desc.replace('\\t','DELIMITXXX')
							desc=desc.replace('- ','DELIMITXXX')
							desc=desc.replace(' -','DELIMITXXX')
							desc=desc.replace(':','DELIMITXXX')
							desc=desc.replace('...','DELIMITXXX')
							desc=desc.replace('\\"','\"')
							desc=desc.replace('*',' ')
							desc=desc.replace('#',' ')
							desc=desc.replace("\\'","\'")
							desc=desc.replace("\\",'')
							desc=desc.replace(" && "," & ")
							desc=desc.replace(" & ",' and ')
							desc=desc.strip()
							continue


                                                        #desc=desc.replace('\\n',' ')
                                                        #desc=desc.replace('\\t',' ')
                                                        #desc=desc.replace("\\'"," ")
                                                        #desc=desc.replace('\\"',' ')
                                                        #desc=desc.replace('*',' ')
                                                        #desc=desc.replace('#',' ')
                                                        #desc=desc.replace('\\',' ')
                                                        #desc=desc.strip()
                                                        #continue

						if line.find("promoText:")>=0:

							continue

							line=line.strip()
							line = line[len("promoText:\"")+1: ]
							line = line[: len(line)-1]
							for eachspecwd in speclist:
								line=line.replace(eachspecwd,'')
							line=line.replace('\\n',' ')
							line=line.replace('\\t',' ')
							line=line.replace("\\'"," ")
							line=line.replace('\\"',' ')
							line=line.replace('*',' ')
							line=line.replace('#',' ')
							line=line.replace('\\',' ')
							line=line.strip()
							if line not in desc:
								desc = desc + ' '+line
							continue

						if line.find("recentChanges:")>=0:
	
							continue

							line=line.strip()
							line = line[len("recentChanges:\"")+1: ]
							recentchange =  line[: len(line)-1]
							for eachspecwd in speclist:
								recentchange=recentchange.replace(eachspecwd,'')
							recentchange=recentchange.replace('\\n',' ')
							recentchange=recentchange.replace('\\t',' ')
							recentchange=recentchange.replace("\\'"," ")
							recentchange=recentchange.replace('\\"',' ')
							recentchange=recentchange.replace('*',' ')
							recentchange=recentchange.replace('#',' ')
							recentchange=recentchange.replace('\\',' ')
							recentchange=recentchange.replace('fixed',' ')
							recentchange=recentchange.replace('Fixed',' ')
							recentchange=recentchange.replace('fix',' ')
							recentchange=recentchange.replace('Fix',' ')
							recentchange=recentchange.replace('bugs',' ')
							recentchange=recentchange.replace('Bugs',' ')
							recentchange=recentchange.replace('bug',' ')
							recentchange=recentchange.replace('Bug',' ')
							#if recentchange not in desc:
								#desc=desc+recentchange.strip()
							#continue


						if line.find("packageName:")>=0: 
							line=line.strip()
							line = line[len("packageName:\"")+1: ]
							package = line[: len(line)-1]
							package=package+'.apk'

				finally:
					file_object.close()
					if (package not in maindict) and len(package)>0 and len(desc)>0:
						maindict[package]=desc
						#print package 
						#print desc
					#elif package in maindict:
						#print package
					package=''
					desc=''

	#print json.dumps(maindict)		
	keylist=maindict.keys()


	tempdict={}


	for index in range(0,2500):
		tempdict[keylist[index]]=maindict[keylist[index]]

	file_op1=open("TEMP1.txt",'w')
	try: 
		file_op1.write(json.dumps(tempdict))
		file_op1.write('\n')
		#print tempdict
	finally:
		tempdict={}
		file_op1.close()


	for index in range(2500,5000):
		tempdict[keylist[index]]=maindict[keylist[index]]

	file_op2=open("TEMP2.txt",'w')
	try: 
		file_op2.write(json.dumps(tempdict))
		file_op2.write('\n')
		#print tempdict
	finally:
		tempdict={}
		file_op2.close()

	for index in range(5000,7500):
		tempdict[keylist[index]]=maindict[keylist[index]]

	file_op3=open("TEMP3.txt",'w')
	try: 
		file_op3.write(json.dumps(tempdict))
		file_op3.write('\n')
		#print tempdict
	finally:
		tempdict={}
		file_op3.close()



	for index in range(7500,len(maindict)):
		tempdict[keylist[index]]=maindict[keylist[index]]

	file_op4=open("TEMP4.txt",'w')
	try: 
		file_op4.write(json.dumps(tempdict))
		file_op4.write('\n')
		#print tempdict
	finally:
		tempdict={}
		file_op4.close()


	#file_op=open('descwithapk.txt',"w")
	#try:
		#for k in maindict:
			#file_op.write(k+'\n')
			#file_op.write(maindict[k]+'\n')
			#file_op.write('\n')
			#file_op.flush()
	#except:
		#print "Errors in writing the file keyworddictory.txt"
	#finally:
		#file_op.close()
	#print 'End of function getdesc()'
	#print 'Length of maindict is: %s'%len(maindict)

	#print len(maindict)
	return maindict


#get the rating of each app
  def getrate(self,path):
	maindict = {}
	list_dirs = os.walk(path) 
	rate=''
	package=''
	for root, dirs, files in list_dirs: 
		for f in files:
			filepath=os.path.join(root, f)
			if filepath.find("meta")>=0 and filepath.find("WIDGETS")<0:
				file_object=open(filepath)
				try:
					alllines = file_object.readlines()
					for line in alllines:
						if line.find("rating:")>=0:
							line=line.strip()
							line = line[len("rating:\"")+1: ]
							rate = line[: len(line)-1]
							continue
						if line.find("packageName:")>=0: 
							line=line.strip()
							line = line[len("packageName:\"")+1: ]
							package = line[: len(line)-1]
							package=package+'.apk'
							if (package not in maindict) and len(package)>0 and len(rate)>0:
								maindict[package]=rate		
							package=''
							rate=''

				finally:
					file_object.close()

	return maindict

#get the number of ratings of each app
  def getnumofrate(self,path):
	maindict = {}
	list_dirs = os.walk(path) 
	ratecount=''
	package=''
	for root, dirs, files in list_dirs: 
		for f in files:
			filepath=os.path.join(root, f)
			if filepath.find("meta")>=0 and filepath.find("WIDGETS")<0:
				file_object=open(filepath)
				try:
					alllines = file_object.readlines()
					for line in alllines:
						if line.find("ratingsCount:")>=0:
							line=line.strip()
							ratecount = line[len("ratingsCount:")+1: ]
							continue
						if line.find("packageName:")>=0: 
							line=line.strip()
							line = line[len("packageName:\"")+1: ]
							package = line[: len(line)-1]
							package=package+'.apk'
							if (package not in maindict) and len(package)>0 and len(ratecount)>0:
								maindict[package]=ratecount
							package=''
							ratecount=''

				finally:
					file_object.close()

	return maindict


#get the size of each app
  def getsize(self,path):
	maindict = {}
	list_dirs = os.walk(path) 
	size=''
	package=''
	for root, dirs, files in list_dirs: 
		for f in files:
			filepath=os.path.join(root, f)
			if filepath.find("meta")>=0 and filepath.find("WIDGETS")<0:
				file_object=open(filepath)
				try:
					alllines = file_object.readlines()
					for line in alllines:
						if line.find("installSize:")>=0:
							line=line.strip()
							size = line[len("installSize:")+1: ]
							continue
						if line.find("packageName:")>=0: 
							line=line.strip()
							line = line[len("packageName:\"")+1: ]
							package = line[: len(line)-1]
							package=package+'.apk'
							if (package not in maindict) and len(package)>0 and len(size)>0:
								maindict[package]=size
							package=''
							size=''

				finally:
					file_object.close()

	return maindict

#output the permissions as index 
#output: appName -> List(permissionIndex)
  def extractperms(self,permdict,permindexdict):
	maindict={}
	for apkname in permdict:
		templist=[]
		for targetperm in permdict[apkname]:
				   templist.append(permindexdict[targetperm])
		maindict[apkname]=templist
	return maindict





  def break2sentence(self,desc):
	import re
        from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
	maindict={}
	delimit=['!','?','>','-','.',' ','=','<']
	numberindex=['1)','2)','3)','4)','5)','6)','7)','8)','9)','10)',
		     '(1)','(2)','(3)','(4)','(5)','(6)','(7)','(8)','(9)','(10)',
                     '1.','2.','3.','4.','5.','6.','7.','8.','9.','10.','>'
		     'a)','b)','c)','d)','e)','f)','g)','h)','i)','g)','k)','l)','m)','n)',
		     'o)','p)','q)','r)','s)','t)','u)','v)','w)','x)','y)','z)',
		     '(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)','(i)','(g)','(k)','(l)','(m)','(n)',
		     '(o)','(p)','(q)','(r)','(s)','(t)','(u)','(v)','(w)','(x)','(y)','(z)',
		     'A)','B)','C)','D)','E)','F)','G)','H)','I)','G)','K)','L)','M)','N)',
		     'O)','P)','Q)','R)','S)','T)','U)','V)','W)','X)','Y)','Z)',
		     '(A)','(B)','(C)','(D)','(E)','(F)','(G)','(H)','(I)','(G)','(K)','(L)','(M)','(N)',
		     '(O)','(P)','(Q)','(R)','(S)','(T)','(U)','(V)','(W)','(X)','(Y)','(Z)']
	for apkname in desc:
		string=desc[apkname]
		print string
		sentences=sent_tokenize(string)
		newsentences=[]
		for sentenceindex in range(len(sentences)):
			sentences[sentenceindex]=" ".join(sentences[sentenceindex].split())
			#sentences[sentenceindex]="-".join(sentences[sentenceindex].split('--'))
			sentences[sentenceindex]=sentences[sentenceindex].strip()
			tempsentences=sentences[sentenceindex].split('DELIMITXXX')
			#if sentences[sentenceindex].find('\n')>0:
				#print sentences[sentenceindex]
			#tempsentences=re.split(r" - |\n|\t|\'|:",sentences[sentenceindex])
			#if sentences[sentenceindex].find('\n')>0:
				#print tempsentences
			#del sentences[sentenceindex]
			for eachelemindex in range(len(tempsentences)):
				tempsentences[eachelemindex]=tempsentences[eachelemindex].replace('\\\\','')
				tempsentences[eachelemindex]=tempsentences[eachelemindex].strip()
				for eachnumber in numberindex:
					if tempsentences[eachelemindex].startswith(eachnumber):
						tempsentences[eachelemindex]=tempsentences[eachelemindex][len(eachnumber):]
						tempsentences[eachelemindex]=tempsentences[eachelemindex].strip()
				#print tempsentences[eachelemindex]
				for delimitelem in delimit:
					while tempsentences[eachelemindex].endswith(delimitelem):
						tempsentences[eachelemindex]=tempsentences[eachelemindex][:len(tempsentences[eachelemindex])-1]
					while tempsentences[eachelemindex].startswith(delimitelem):
						tempsentences[eachelemindex]=tempsentences[eachelemindex][1:]
					
			newsentences.extend(tempsentences)

		removeredund=[]
		for senten in newsentences:
			templowersenten=senten.lower()
			if templowersenten.endswith('http') or templowersenten.endswith('https') or templowersenten.startswith('//') or templowersenten.startswith('www.'):# or templowersenten.find(' us ')>0 or templowersenten.endswith(' us'):
				continue
			if senten not in removeredund and len(senten)>0:
				removeredund.append(senten)
		print removeredund
		#print '\n'
		maindict[apkname]=removeredund
	return maindict
		

# preprocess the description of application so as to be handled in TF-idf
# output appName -> List(words in description)
  def preprocessbfTF(self,desc):
        from nltk.stem.wordnet import WordNetLemmatizer
        lmtzr = WordNetLemmatizer()
	
	from nltk.corpus import wordnet

	from nltk.tag.simplify import simplify_wsj_tag


	keeplist=['sms','facebook','photo','mms']
	
	maindict={}
	for apkname in desc:
		string=desc[apkname]
		#print string
		delimlist=['!','.',',','-']
		finallist=[]
		for delim in delimlist:
			string=string.replace(delim,' ')
		templist=string.split(' ')
		for elem in templist:
			elem=elem.strip()
			if len(elem)>2 and elem.isalpha() and len(wordnet.synsets(elem)) > 0: #the last one is for test

				elem=elem.lower()
				

				if elem in keeplist:
					finallist.append(elem) 
					continue


				tokens=[]
				tokens.append(elem)
				tagged_sent = nltk.pos_tag(tokens)
				tag=simplify_wsj_tag(tagged_sent[0][1])
				if tag=='VD' or tag=='VG' or tag=='VN':

					continue
					elem=lmtzr.lemmatize(elem,'v')
					if elem not in filteredlist:
						finallist.append(elem)
				elif tag=='V' or tag=='ADJ':
					continue
					if elem not in filteredlist:
						finallist.append(elem)
				elif tag=='N':# or tag=='NP' or tag=='NUM':
					elem=lmtzr.lemmatize(elem)
					if elem not in filteredlist:
						finallist.append(elem)


		if (apkname not in maindict) and len(finallist)>0:
			maindict[apkname]=finallist
			#print finallist
			print "In preprocessbfTF, current Loop: %s in about 10000 loops"%len(maindict)
	return maindict

#used to append the Stings defined in the process of App development, not very useful 
  def appendString(self,descdict):
        from nltk.stem.wordnet import WordNetLemmatizer
        lmtzr = WordNetLemmatizer()

	from nltk.corpus import wordnet

	from nltk.tag.simplify import simplify_wsj_tag
	
	appendstrdict={}


	file_obj=open("/home/zyqu/Research/Android_sec/parsexml/semant/2145appsStringtoAppend.txt")
	try:
		alllines = file_obj.readlines()
		keywords=[]
		apkname=''
		for line in alllines:
			line=line.strip()
			if line.find('.apk')>0:
				apkname=line
				continue
			if len(line)==0:
				if len(apkname)>0 and (apkname not in appendstrdict) and len(keywords)>0:
					appendstrdict[apkname]=keywords
				keywords=[]
				apkname=''
				continue
			keywords.append(lmtzr.lemmatize(line.lower()))
	except:
		print "Errors in openning 2145appsStringtoAppend.txt"
	finally:
		file_obj.close()


	file_obj=open("/home/zyqu/Research/Android_sec/parsexml/semant/3089appsStringtoAppend.txt")
	try:
		alllines = file_obj.readlines()
		keywords=[]
		apkname=''
		for line in alllines:
			line=line.strip()
			if line.find('.apk')>0:
				apkname=line
				continue
			if len(line)==0:
				if len(apkname)>0 and (apkname not in appendstrdict) and len(keywords)>0:
					appendstrdict[apkname]=keywords
				keywords=[]
				apkname=''
				continue
			keywords.append(lmtzr.lemmatize(line.lower()))
	except:
		print "Errors in openning 3089appsStringtoAppend.txt"
	finally:
		file_obj.close()

	file_obj=open("/home/zyqu/Research/Android_sec/parsexml/semant/4308appsStringtoAppend.txt")
	try:
		alllines = file_obj.readlines()
		keywords=[]
		apkname=''
		for line in alllines:
			line=line.strip()
			if line.find('.apk')>0:
				apkname=line
				continue
			if len(line)==0:
				if len(apkname)>0 and (apkname not in appendstrdict) and len(keywords)>0:
					appendstrdict[apkname]=keywords
				keywords=[]
				apkname=''
				continue
			keywords.append(lmtzr.lemmatize(line.lower()))
	except:
		print "Errors in openning 4308appsStringtoAppend.txt"
	finally:
		file_obj.close()


	maindict={}
	filteredlist=['yes','no','true','false','thank','thanks','null','error','none','success','default','array','version','use','dot','unknown','valid','invalid','byte','result','other','code','debug','token','integer','medium','are','has','have','nan','male','female','gender','bse','want','sorry','phd', 'a', 'able', 'about', 'across', 'after', 'all', 'almost', 'also', 'am', 'among', 'an', 'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'but', 'by', 'can', 'cannot', 'could', 'dear', 'did', 'do', 'does', 'either', 'else', 'ever', 'every', 'for', 'from', 'get', 'got', 'had', 'has', 'have', 'he', 'her', 'hers', 'him', 'his', 'how', 'however', 'i', 'if', 'in', 'into', 'is', 'it', 'its', 'just', 'least', 'let', 'like', 'likely', 'may', 'me', 'might', 'most', 'must', 'my', 'neither', 'no', 'nor', 'not', 'of', 'off', 'often', 'on', 'only', 'or', 'other', 'our', 'own', 'rather', 'said', 'say', 'says', 'she', 'should', 'since', 'so', 'some', 'than', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'this', 'tis', 'to', 'too', 'twas', 'us', 'wants', 'was', 'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'would', 'yet', 'you']

	for apkname in appendstrdict:
		keywlist=[]
		for eachstring in appendstrdict[apkname]:
			if len(eachstring)>2 and len(wordnet.synsets(eachstring))>0: #the last one for test
				#keywlist.append(eachstring)

				eachstring=eachstring.lower()
				if eachstring in filteredlist:
					continue

				tokens=[]
				tokens.append(eachstring)
				tagged_sent = nltk.pos_tag(tokens)
				tag=simplify_wsj_tag(tagged_sent[0][1])
				if tag=='VD' or tag=='VG' or tag=='VN':
					eachstring=lmtzr.lemmatize(eachstring,'v')
					if eachstring not in filteredlist:
						keywlist.append(eachstring)
				elif tag=='V' or tag=='ADJ':
					if eachstring not in filteredlist:
						keywlist.append(eachstring)
				elif tag=='N':# or tag=='NP' or tag=='NUM':
					eachstring=lmtzr.lemmatize(eachstring)
					if eachstring not in filteredlist:
						keywlist.append(eachstring)




		if apkname in descdict:
			for eachkw in descdict[apkname]:
				keywlist.append(eachkw)
		if (apkname not in maindict) and len(keywlist)>0:	
			maindict[apkname]=keywlist
			print "In appendString, current Loop: %s in randomly 10000 loops"%len(maindict)

	for apkname in descdict:
		keywlist=[]
		if apkname not in appendstrdict:			
			for eachkw in descdict[apkname]:
				keywlist.append(eachkw)
			if (apkname not in maindict) and len(keywlist)>0:
				maindict[apkname]=keywlist
				#if len(keywlist)!=len(descdict[apkname]):
					#print "XXXXXXXXXXXXX"	

	#print maindict
	#print "Length of appendstrdict: %s"%len(appendstrdict)
	#print len(descdict)
	#print "Length of Union Set: %s"%len(maindict)
	#for elem in descdict:
		#if elem not in maindict:
			#print "In descdict not in maindict: "+elem
			#print descdict[elem]
	return maindict


#calculate the TF value of each keyword, output the sorted list
  def TFfreq(self,kwdict):
	maindict={}
	totalcount=0
	for apkname in kwdict:
		for eachkw in kwdict[apkname]:
			totalcount=totalcount+1
			if eachkw not in maindict:
				maindict[eachkw]=1
				continue
			elif eachkw in maindict:
				maindict[eachkw]=maindict[eachkw]+1
	for elem in maindict:
		maindict[elem]=maindict[elem]*100.0/totalcount

	orderedlist=sorted(maindict.iteritems(), key=lambda d:d[1], reverse=True)
	print "Function TFfreq finished"
	return orderedlist
	
  def TFfilter(self, TFlist, kwdict, upper, lower):

	newlist=[]
	for elem in TFlist:
		if lower<elem[1]<upper:
			newlist.append(elem[0])
	#print "length of newlist is: %s"%len(newlist)

	maindict={}
	for appname in kwdict:
		templist=[]
		for eachkw in kwdict[appname]:
			if (eachkw in newlist) and (eachkw not in templist):
				templist.append(eachkw)
		if (appname not in maindict) and len(templist)>0:
			maindict[appname]=templist
	
	#print "Function TFfilter finished, the length of newkwdict{} is %s"%len(maindict)	

	file_opt=open("filterkwdict.txt","w")
	try:
		for apk in maindict:
			file_opt.write(apk+'\n')
			for v in maindict[apk]:
				file_opt.write(v+'\n')
			file_opt.write('\n')
	except:
		print "Errors in writing file: filterkwdict.txt"
	finally:
		file_opt.close()
	return maindict

#output the Tf-idf value of each word in the description of each app
  def TfIdf(self, kwdict):
	print "Begin TfIdf."
	import math
	maindict={}
	totalapps=len(kwdict)
	loopcount=1

	for appname in kwdict:
		print "Loopcount: %s"%loopcount+" in %s"%totalapps
		loopcount=loopcount+1
		totalkwinapp=len(kwdict[appname])

		kwlist=[]
		for keyword in kwdict[appname]:
			if keyword not in kwlist:
				kwlist.append(keyword)


		tempdict={}
		for targetkw in kwlist:

			kwfreqcount=0
			for tempkw in kwdict[appname]:
				if tempkw==targetkw:
					kwfreqcount=kwfreqcount+1
			TF=kwfreqcount*1.0/totalkwinapp

			idfreqcount=0
			for tempapk in kwdict:
				if targetkw in kwdict[tempapk]:
					idfreqcount=idfreqcount+1
			IDF=math.log(totalapps*1.0/idfreqcount)
			tempdict[targetkw]=TF*IDF
		orderedlist=sorted(tempdict.iteritems(), key=lambda d:d[1], reverse=True)
		maindict[appname]=orderedlist


	print "Begin writing file TDIDFres.txt"
	file_op=open("TFIDFres.txt","w")
	try:
		for elem in maindict:
			file_op.write(elem+'\n')
			for kw in maindict[elem]:
				file_op.write(kw[0]+', %s\n'%kw[1])
			file_op.write('\n')
	except:
		print "Errors in writing file TFIDFres.txt"
	finally:
		file_op.close()

	return maindict
			
  def preCluster(self):
	file_in=open("TFIDFres.txt")
	keywordindex={}
	orderedlist=[]
	indexcount=0
	maindict={}

	try:
		alllines = file_in.readlines()		
		for line in alllines:
			line=line.strip()
			if line.find('.apk')<0 and len(line)>0:
				keyword=line[:line.find(',')]
				if keyword not in keywordindex:
					keywordindex[keyword]=indexcount
					indexcount=indexcount+1	
		orderedlist=sorted(keywordindex.iteritems(), key=lambda d:d[1], reverse=False)		

		for line2 in alllines:
			line2=line2.strip()
			if line2.find('.apk')>0:
				appname=line2
				keywordlist=range(0,len(keywordindex))
				for index in range(0,len(keywordindex)):
					keywordlist[index]=0
				if len(keywordlist) != len(keywordindex):
					print "Mismatch in the size of keywordlist"
				continue

			if len(line2)==0:
				if (appname not in maindict) and len(appname)>0:
					maindict[appname]=keywordlist
				appname=''
				keywordlist=[]
				continue

			if line2.find('.apk')<0 and len(line2)>0:
				kw=line2[:line2.find(',')]
				tfidfval=line2[line2.find(',')+2:]
				keywordlist[keywordindex[kw]]=tfidfval	
				continue							
	except:
		print "Errors in reading file TFIDFres.txt"
	finally:
		file_in.close()

	#print maindict

	file_out=open("samplesCluster","w")
	try:
		tempstring="appname"
		for elem in orderedlist:
			tempstring=tempstring+','+elem[0]
			#print elem[1]
		file_out.write(tempstring+'\n')
		
		tempstring=''

		for k in maindict:
			tempstring=k
			for tempindex in range(0,len(keywordindex)):
				tempstring=tempstring+',%s'%maindict[k][tempindex]
			file_out.write(tempstring+'\n')
			
	
	except:
		print "Errors in writing file samplesCLuster"
	finally:
		file_out.close()
	
# refine the keywords output from Alchemy API
  def keywordrefine2(self,keyworddict):
	maindict={}
	filterphrase=['high quality','android','application','app','applications']
	for apkname in keyworddict:
		templist=[]
		for phrase in keyworddict[apkname]:
			tempphrase=phrase.strip()
			tempphrase=tempphrase.lower()
			tempapkname=apkname.lower()
			#if tempapkname.find(tempphrase)>=0:
				#continue
			for elem in filterphrase:
				tempphrase=tempphrase.replace(elem,'')		
			if (tempphrase not in templist):
				tempphrase=tempphrase.strip()
				if 'wallpaper' in tempphrase:
					tempphrase='wallpaper'
				templist.append(tempphrase)
		templist=self.phraseprocess(templist,tempapkname)
		if (apkname not in maindict) and len(templist)>0 and len(apkname)>0:
			maindict[apkname]=templist
	return maindict




#helper function of keywordrefine2
  def phraseprocess(self,phraselist,apkname):
        from nltk.stem.wordnet import WordNetLemmatizer
        lmtzr = WordNetLemmatizer()

	from nltk.corpus import wordnet

	from nltk.tag.simplify import simplify_wsj_tag

	newphraselist=[]


	for phrase in phraselist:
		wordlist=phrase.split(' ')
		newwordlist=[]
		for word in wordlist:
			if len(word)<=1:
				continue
			if word.find('http://')>=0 or word.find('https://')>=0:
				continue

			if word[0].isalpha()==False:
				word=word[1:]

			if len(word)<=1:
				continue

			if word[len(word)-1].isalpha()==False:
				word=word[:len(word)-1]
			#if apkname.find(word)>=0:
				#continue

			token=[]
			token.append(word)
			tagged_sent = nltk.pos_tag(token)
			tag=simplify_wsj_tag(tagged_sent[0][1])
			
			if tag=='VD' or tag=='VG' or tag=='VN':
				continue
				word=lmtzr.lemmatize(word,'v')

			elif tag=='N' or tag=='NP' or tag=='NUM':
				word=lmtzr.lemmatize(word)

			elif tag=='ADV' or tagged_sent[0][1]=='NNP' or tagged_sent[0][1]=='JJR' or tagged_sent[0][1]=='JJS':
				continue

			for originalword in replacedict:
				if word in replacedict[originalword]:
					word=originalword

			word=word.strip()
			if (word not in newwordlist) and len(word)>1:
				if word.find('-')<0 and len(wordnet.synsets(word))>0:
					newwordlist.append(word)
					continue
				elif word.find('-')>0:
					newwordlist.append(word)
					continue

		newphrase=' '.join(newwordlist)
		newphrase=newphrase.strip()
		if (newphrase not in newphraselist) and len(newphrase)>0:
			newphraselist.append(newphrase)
	return newphraselist


  def keywordfilter(self, reversekwfreqdict):
	reslist=[]
	gapthreshold=4.05
	for kw in reversekwfreqdict:
		upper=reversekwfreqdict[kw][0][1]
		lower=reversekwfreqdict[kw][len(reversekwfreqdict[kw])-1][1]
		#print kw 
		#print upper-lower
		if (upper-lower)>gapthreshold:
			reslist.append(kw)
			
	print "Length of the filtered list: %s"%len(reslist)
	return reslist

#output the permission dict appName -> ListofKeypermissions			
  def getkeyperm(self, permdict):
	permlist=['android.permission.ACCESS_FINE_LOCATION',
                'android.permission.ACCESS_COARSE_LOCATION',
                'android.permission.CALL_PHONE',
                'android.permission.CAMERA',
                'android.permission.READ_CALENDAR',
                'android.permission.READ_CALL_LOG',
                'android.permission.READ_CONTACTS',
                'android.permission.READ_SMS',
                'android.permission.RECEIVE_BOOT_COMPLETED',
                'android.permission.RECORD_AUDIO',
                'android.permission.SEND_SMS',
                'android.permission.WRITE_CONTACTS',
                'android.permission.WRITE_EXTERNAL_STORAGE',
                'android.permission.GET_ACCOUNTS',
                'android.permission.GET_TASKS',
                'android.permission.WRITE_SETTINGS'
                ]

	maindict={}
	for apkname in permdict:
		templist=[]
		for perm in permdict[apkname]:
			if (perm in permlist) and (perm not in templist):
				templist.append(perm)
		if len(templist)>0:
			maindict[apkname]=templist
	return maindict		

#first K of a list
def firstklist(lst,k):
	templist=[]
	if len(lst)<=k:
		return lst
	elif len(lst)>k:
		templist=lst[:k]
		return templist

#output List(parents of the input role roleindex)
def getparent(roleindex, parentchildrelat):
  parents=[]
  parent=-1

  for eachindex in parentchildrelat:
	if roleindex==parentchildrelat[eachindex][0] or roleindex==parentchildrelat[eachindex][1]:
		parent=eachindex
		parents.append(parent)
		break

  while parent>=0:
	myself=parent
  	for eachindex in parentchildrelat:
		if myself==parentchildrelat[eachindex][0] or myself==parentchildrelat[eachindex][1]:
			parent=eachindex
			parents.append(parent)
			break
	if parent==myself:
		break
  return parents

#output List(children of the input role roleindex)	
def getchild(roleindex, parentchildrelat):
  children=[]
  if roleindex in parentchildrelat:
	childAindex=parentchildrelat[roleindex][0]
	childBindex=parentchildrelat[roleindex][1]
	children.append(childAindex)
	children.append(childBindex)
	children.extend(getchild(childAindex,parentchildrelat))
	children.extend(getchild(childBindex,parentchildrelat))
  return children

def newnewfscore(permdict,keyworddict,replaceworddict,targetperm,trainapplst,fold):
  TPdict={}
  FPdict={}
  FNdict={}
  Precisiondict={}
  Recalldict={}
  permpercdict={}
  kwpercdict={}

  maindict={}

  groupedwords=[]
  for eachwd in replaceworddict:
	if eachwd not in groupedwords:
		groupedwords.append(eachwd)

  ungroupedwords=[]
  for apkName in keyworddict:
	for eachwd in keyworddict[apkName]:
		if eachwd in groupedwords:
			continue
		if eachwd not in ungroupedwords:
			ungroupedwords.append(eachwd)


  permlist=[]
  for appName in permdict:
	for eachPerm in permdict[appName]:
		if eachPerm not in permlist:
			permlist.append(eachPerm)


  print "Total number of ungrouped words: %s"%len(ungroupedwords)
  print "Total number of grouped words: %s"%len(groupedwords)

  numofapps=len(trainapplst)

  for eachPerm in permlist:
        if eachPerm != targetperm:
                continue
      
	appswithperm=0

        for apk in trainapplst:
                if apk not in permdict:
                        continue
                elif (apk in permdict) and (eachPerm in permdict[apk]):
                    appswithperm=appswithperm+1

	tempdict={}
	percentperm=appswithperm*1.0/numofapps
	print percentperm

  #frequency measurement for grouped words
	for eachgroupkey in replaceworddict:
		TPcounter=0
		FPcounter=0
		TNcounter=0
		FNcounter=0


		appswithgroupkey=0
		
		for eachApp in trainapplst:
                        if eachApp not in keyworddict:
                            continue

                        if eachApp not in permdict:
                            continue


			thiswordlst=keyworddict[eachApp]

			if eachgroupkey in thiswordlst:
				appswithgroupkey=appswithgroupkey+1
				if eachPerm in permdict[eachApp]:
					TPcounter=TPcounter+1
				elif eachPerm not in permdict[eachApp]:
					FPcounter=FPcounter+1
				continue

			elif eachgroupkey not in thiswordlst:
				hasword=False
				maxrelval=0.0

				for eachrelatedwd in replaceworddict[eachgroupkey]:
					if eachrelatedwd[0] in thiswordlst:
						hasword=True
						if eachrelatedwd[1]>maxrelval:
							maxrelval=eachrelatedwd[1]

			if hasword==True:
				appswithgroupkey=appswithgroupkey+maxrelval
				if eachPerm in permdict[eachApp]:
					TPcounter=TPcounter+maxrelval
				elif eachPerm not in permdict[eachApp]:
					FPcounter=FPcounter+maxrelval

			if hasword==False:
				if eachPerm in permdict[eachApp]:
					FNcounter=FNcounter+1
				elif eachPerm not in permdict[eachApp]:
					TNcounter=TNcounter+1

		if TPcounter+FPcounter==0 or TPcounter+FNcounter==0: 
			continue

		Precision=TPcounter*1.0/(TPcounter+FPcounter)
		Recall=TPcounter*1.0/(TPcounter+FNcounter)


		if Precision+Recall==0:
			continue

		percentkwgroup=appswithgroupkey*1.0/numofapps
		if Recall/percentkwgroup <1.0 or Precision/percentperm<1.0:
			continue
                prec_increment=(Precision-percentperm)/percentperm
                recall_increment=(Recall-percentkwgroup)/percentkwgroup
                permpercdict[eachPerm]=percentperm
                kwpercdict[(eachPerm,eachgroupkey)]=percentkwgroup
                beta=1
                if beta*beta*prec_increment+recall_increment==0:
                    continue
                tempdict[eachgroupkey]=(1+beta*beta)*prec_increment*recall_increment/(beta*beta*prec_increment+recall_increment)
		TPdict[(eachPerm,eachgroupkey)]=TPcounter
		FPdict[(eachPerm,eachgroupkey)]=FPcounter
		FNdict[(eachPerm,eachgroupkey)]=FNcounter
		Precisiondict[(eachPerm,eachgroupkey)]=Precision
		Recalldict[(eachPerm,eachgroupkey)]=Recall

	maindict[eachPerm]=sorted(tempdict.iteritems(), key=lambda d:d[1], reverse=True)

  resroot=proj_path+'/evaluation/potentNP/'
  for eachelem in maindict:
        resperm=resroot+eachelem
        command='mkdir '+resperm
        os.system(command)
        jsonpath=resperm+'/'+'NPfold%s.json'%fold
        f_op=open(jsonpath,'w')
        f_op.write(json.dumps(maindict))
        f_op.close()

        txtpath=resperm+'/'+'NPfold%s.txt'%fold
        
        file_op=open(txtpath,'w')
        try:
                file_op.write('Word\tincrement\tTP\tFP\tFN\tPrecision\tRecall\tPermperc\tgroupkeyperc\n')
	        for eachPerm in maindict:
		        file_op.write(eachPerm+'\n')
		        templist=firstklist(maindict[eachPerm],300)
		        for eachelem in templist:
			        file_op.write(eachelem[0]+'\t%s'%eachelem[1]+'\t%s'%TPdict.get((eachPerm,eachelem[0]))+'\t%s'%FPdict.get((eachPerm,eachelem[0]))+'\t%s'%FNdict.get((eachPerm,eachelem[0]))+'\t%s'%Precisiondict.get((eachPerm,eachelem[0]))+'\t%s'%Recalldict.get((eachPerm,eachelem[0]))+'\t%s'%permpercdict.get(eachPerm)+'\t%s\n'%kwpercdict.get((eachPerm,eachelem[0]))
                                )
		        file_op.write('\n')		
        finally:
	        file_op.close()



def newfscore(permdict,keyworddict,groupworddict):
  TPdict={}
  FPdict={}
  FNdict={}
  Precisiondict={}
  Recalldict={}

  beta=0.3
  groupedwords=[]
  maindict={}
  for eachCluster in groupworddict:
	for eachgroupwd in groupworddict[eachCluster]:
		if eachgroupwd[0] not in groupedwords:
			groupedwords.append(eachgroupwd[0])


  ungroupedwords=[]
  for apkName in keyworddict:
	for eachwd in keyworddict[apkName]:
		if eachwd in groupedwords:
			continue
		if eachwd not in ungroupedwords:
			ungroupedwords.append(eachwd)


  permlist=[]
  for appName in permdict:
	for eachPerm in permdict[appName]:
		if eachPerm not in permlist:
			permlist.append(eachPerm)


  print "Total number of ungrouped words: %s"%len(ungroupedwords)
  print "Total number of grouped words: %s"%len(groupedwords)

  counter=0
  for permindex in range(0,3):
  #for eachPerm in permlist:
	eachPerm = permlist[permindex]
	counter=counter+1
	print "Loop %s"%counter + ' in %s'%len(permlist)
	tempdict={}

	#frequency measurement fo grouped words
	for eachCluster in groupworddict:
		TPcounter=0
		FPcounter=0
		TNcounter=0
		FNcounter=0
		
		for eachApp in keyworddict:
			thiswordlst=keyworddict[eachApp]
			hasword=False
			maxrelval=0.0

			for eachgroupword in groupworddict[eachCluster]:
				if eachgroupword[0] in thiswordlst:
					hasword=True
					if eachgroupword[1] > maxrelval:
						maxrelval=eachgroupword[1]
			
			if hasword==True:
				if eachPerm in permdict[eachApp]:
					TPcounter=TPcounter+maxrelval
				elif eachPerm not in permdict[eachApp]:
					FPcounter=FPcounter+maxrelval

			if hasword==False:
				if eachPerm in permdict[eachApp]:
					FNcounter=FNcounter+1
				elif eachPerm not in permdict[eachApp]:
					TNcounter=TNcounter+1


		if TPcounter+FPcounter==0 or TPcounter+FNcounter==0: 
			continue

		Precision=TPcounter*1.0/(TPcounter+FPcounter)
		Recall=TPcounter*1.0/(TPcounter+FNcounter)


		if Precision+Recall==0:
			continue

		#fscore=2*Precision*Recall*1.0/(Precision+Recall)
		fscore=(1+beta*beta)*Precision*Recall/(beta*beta*Precision+Recall)
		tempdict['Cluster'+eachCluster]=fscore
		TPdict[(eachPerm,'Cluster'+eachCluster)]=TPcounter
		FPdict[(eachPerm,'Cluster'+eachCluster)]=FPcounter
		FNdict[(eachPerm,'Cluster'+eachCluster)]=FNcounter
		Precisiondict[(eachPerm,'Cluster'+eachCluster)]=Precision
		Recalldict[(eachPerm,'Cluster'+eachCluster)]=Recall
			
			


	#frequency measurement for ungrouped words
	for eachWord in ungroupedwords:
		TPcounter=0
		FPcounter=0
		TNcounter=0
		FNcounter=0
		for eachApp in keyworddict:
			if (eachWord in keyworddict[eachApp]) and (eachPerm in permdict[eachApp]):
				TPcounter=TPcounter+1

			elif (eachWord in keyworddict[eachApp]) and (eachPerm not in permdict[eachApp]):
				FPcounter=FPcounter+1

			elif (eachWord not in keyworddict[eachApp]) and (eachPerm in permdict[eachApp]):
				FNcounter=FNcounter+1

			elif (eachWord not in keyworddict[eachApp]) and (eachPerm not in permdict[eachApp]):
				TNcounter=TNcounter+1

		if TPcounter+FPcounter==0 or TPcounter+FNcounter==0: 
			continue

		Precision=TPcounter*1.0/(TPcounter+FPcounter)
		Recall=TPcounter*1.0/(TPcounter+FNcounter)


		if Precision+Recall==0:
			continue

		#fscore=2*Precision*Recall*1.0/(Precision+Recall)
		fscore=(1+beta*beta)*Precision*Recall/(beta*beta*Precision+Recall)
		tempdict[eachWord]=fscore
		TPdict[(eachPerm,eachWord)]=TPcounter
		FPdict[(eachPerm,eachWord)]=FPcounter
		FNdict[(eachPerm,eachWord)]=FNcounter
		Precisiondict[(eachPerm,eachWord)]=Precision
		Recalldict[(eachPerm,eachWord)]=Recall


	maindict[eachPerm]=sorted(tempdict.iteritems(), key=lambda d:d[1], reverse=True)
	

  file_op=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/Clusterbasedres/beta03Perm0to2fscgroupFeature.txt','w')
  try:
	file_op.write('Word	fscore	TP	FP	FN	Precision	Recall\n')
	for eachPerm in maindict:
		file_op.write(eachPerm+'\n')
		templist=firstklist(maindict[eachPerm],100)#eachelem[0] is the cluster number or a phrase
		for eachelem in templist:
			file_op.write(eachelem[0]+'	%s'%eachelem[1]+'	%s'%TPdict.get((eachPerm,eachelem[0]))+'	%s'%FPdict.get((eachPerm,eachelem[0]))+'	%s'%FNdict.get((eachPerm,eachelem[0]))+'	%s'%Precisiondict.get((eachPerm,eachelem[0]))+'	%s\n'%Recalldict.get((eachPerm,eachelem[0])))
		file_op.write('\n')		
  finally:
	file_op.close()

  return maindict


def fscore(permdict,keyworddict):
  permlist=[]
  maindict={}
  TPdict={}
  FPdict={}
  FNdict={}
  Precisiondict={}
  Recalldict={}
  beta=0.3
  for appName in permdict:
	for eachPerm in permdict[appName]:
		if eachPerm not in permlist:
			permlist.append(eachPerm)

  wordlist=[]	
  for appName in keyworddict:
	for eachKeyword in keyworddict[appName]:
		if eachKeyword not in wordlist:
			wordlist.append(eachKeyword)
  print "total number of words: %s"%len(wordlist)

  counter=0
  for permindex in range(0,3):
	eachPerm=permlist[permindex]
	counter=counter+1
	print "Loop %s"%counter + 'in %s'%len(permlist)


	tempdict={}

	for eachWord in wordlist:
		TPcounter=0
		FPcounter=0
		TNcounter=0
		FNcounter=0
		for eachApp in keyworddict:
			if (eachWord in keyworddict[eachApp]) and (eachPerm in permdict[eachApp]):
				TPcounter=TPcounter+1

			elif (eachWord in keyworddict[eachApp]) and (eachPerm not in permdict[eachApp]):
				FPcounter=FPcounter+1

			elif (eachWord not in keyworddict[eachApp]) and (eachPerm in permdict[eachApp]):
				FNcounter=FNcounter+1

			elif (eachWord not in keyworddict[eachApp]) and (eachPerm not in permdict[eachApp]):
				TNcounter=TNcounter+1

		if TPcounter+FPcounter==0 or TPcounter+FNcounter==0: 
			continue

		Precision=TPcounter*1.0/(TPcounter+FPcounter)
		Recall=TPcounter*1.0/(TPcounter+FNcounter)
		#print TPcounter
		#print FNcounter
		#print Recall

		if Precision+Recall==0:
			continue

		#fscore=2*Precision*Recall*1.0/(Precision+Recall)
		fscore=(1+beta*beta)*Precision*Recall/(beta*beta*Precision+Recall)
		tempdict[eachWord]=fscore
		TPdict[(eachPerm,eachWord)]=TPcounter
		FPdict[(eachPerm,eachWord)]=FPcounter
		FNdict[(eachPerm,eachWord)]=FNcounter
		Precisiondict[(eachPerm,eachWord)]=Precision
		Recalldict[(eachPerm,eachWord)]=Recall
	

	maindict[eachPerm]=sorted(tempdict.iteritems(), key=lambda d:d[1], reverse=True)
	

  file_op=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/appendres/beta03Perm0to2fscoregroupFeature.txt','w')
  try:
	file_op.write('Word	fscore	TP	FP	FN	Precision	Recall\n')
	for eachPerm in maindict:
		file_op.write(eachPerm+'\n')
		templist=firstklist(maindict[eachPerm],100)
		for eachelem in templist:#eachelem[0] keyword, eachelem[1] fscore
			#print '	%s'%TPdict[(eachPerm,eachelem[0])]
			file_op.write(eachelem[0]+'	%s'%eachelem[1]+'	%s'%TPdict.get((eachPerm,eachelem[0]))+'	%s'%FPdict.get((eachPerm,eachelem[0]))+'	%s'%FNdict.get((eachPerm,eachelem[0]))+'	%s'%Precisiondict.get((eachPerm,eachelem[0]))+'	%s\n'%Recalldict.get((eachPerm,eachelem[0])))
		file_op.write('\n')		
  finally:
	file_op.close()

  return maindict

def portiondiff(permdict,keyworddict):
  permlist=[]
  maindict={}
  for appName in permdict:
	for eachPerm in permdict[appName]:
		if eachPerm not in permlist:
			permlist.append(eachPerm)


  counter=0
  for eachPerm in permlist:
	counter=counter+1
	print "Loop %s"%counter + 'in %s'%len(permlist)
	appwithPermlist=[]
	appwithoutPermlist=[]
	for appName in permdict:
		if eachPerm in permdict[appName]:
			appwithPermlist.append(appName)
		elif eachPerm not in permdict[appName]:
			appwithoutPermlist.append(appName)

	wordlist=[]	
	for eachApp in appwithPermlist:
		for eachWord in keyworddict[eachApp]:
			if eachWord not in wordlist:
				wordlist.append(eachWord)

	tempdict={}	
	for eachWordelem in wordlist:
		numappswithperm=0
		numappswithoutperm=0
		for eachApp in appwithPermlist:
			if eachWordelem in keyworddict[eachApp]:
				numappswithperm=numappswithperm+1
		for eachApp in appwithoutPermlist:
			if eachWordelem in keyworddict[eachApp]:
				numappswithoutperm=numappswithoutperm+1
		percentappswithPerm=numappswithperm*1.0/len(appwithPermlist)
		percentappswithoutPerm=numappswithoutperm*1.0/len(appwithoutPermlist)
		res=percentappswithPerm*(percentappswithPerm-percentappswithoutPerm)
		tempdict[eachWordelem]=res
		
	maindict[eachPerm]=sorted(tempdict.iteritems(), key=lambda d:d[1], reverse=True)	

  file_op=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/AllStanfordportiondiffJN.txt','w')
  try:
	for eachPerm in maindict:
		file_op.write(eachPerm+'\n')
		templist=firstklist(maindict[eachPerm],100)
		for eachelem in templist:
			file_op.write(eachelem[0]+', %s\n'%eachelem[1])
		file_op.write('\n')		
  finally:
	file_op.close()

  return maindict
  	


#rolemining of ORCA
def roleminingORCA(permdict,keyworddict):
  currentroles={}#temp
  finalroles={}#apps and role
  parentchildrelat={}
  indextorole={}#permissions and role
  counter=1
  numofappsdict={}#number of members and role
  rolekeyword={}#keyword and role
  tfidfrolekeyword={}

#initialization
  permlist=[]
  for apkname in permdict:
	for eachperm in permdict[apkname]:
		if eachperm not in permlist:
			permlist.append(eachperm)
  
  for eachperm in permlist:
	apkbuffer=[]
	for apkname in permdict:
		for elem in permdict[apkname]:
			if elem==eachperm:
				apkbuffer.append(apkname)
        currentroles[counter]=apkbuffer
	templist=[]
	templist.append(eachperm)
	indextorole[counter]=templist
	numofappsdict[counter]=len(currentroles[counter])
	#print eachperm
	counter=counter+1


#keep generating the super cluster
  while len(currentroles)>1:
	print "Current number of roles %s, the operation will terminate as it is 1"%len(currentroles)
	intersectnumdict={}
	for counter1 in currentroles:
		for counter2 in currentroles:
			if counter1==counter2:
				continue
			elif counter1 != counter2:
				appsetrole1=set(currentroles[counter1])
				appsetrole2=set(currentroles[counter2])
				numinterset=len(appsetrole1.intersection(appsetrole2))
				intersectnumdict[(counter1,counter2)]=numinterset

	orderedlist=sorted(intersectnumdict.iteritems(), key=lambda d:d[1], reverse=True)
	firstroleindex=orderedlist[0][0][0]
	secondroleindex=orderedlist[0][0][1]
	roleAtomine=indextorole[firstroleindex]
	#print roleAtomine
	roleBtomine=indextorole[secondroleindex]
	superrole=list(set(roleAtomine).union(set(roleBtomine)))
	#print superrole
	supermember=list(set(currentroles[firstroleindex]).intersection(set(currentroles[secondroleindex])))
	currentroles[counter]=supermember
	indextorole[counter]=superrole
	parentchildrelat[counter]=(firstroleindex,secondroleindex)
	numofappsdict[counter]=len(currentroles[counter])



	if counter not in finalroles:
		finalroles[counter]=supermember
	if firstroleindex not in finalroles:
		finalroles[firstroleindex]=currentroles[firstroleindex]
	if secondroleindex not in finalroles:  
		finalroles[secondroleindex]=currentroles[secondroleindex]

	counter=counter+1
	#remove the old role
	del currentroles[firstroleindex]
	del currentroles[secondroleindex]
	

  for roleindex in finalroles:
	print roleindex
	tempkeywordfreq={}
	tempkeywordidf={}
	tfidf={}
	parentchildlist=getparent(roleindex,parentchildrelat)
	#print parentchildlist
	parentchildlist.extend(getchild(roleindex,parentchildrelat))
	#print parentchildlist
	parentchildlist.append(roleindex)
	selfparentchildlist=parentchildlist
	for eachapk in finalroles[roleindex]:
		for eachkw in keyworddict[eachapk]:
			if eachkw not in tempkeywordfreq:
				tempkeywordfreq[eachkw]=1
			elif eachkw in tempkeywordfreq:
				tempkeywordfreq[eachkw]=tempkeywordfreq[eachkw]+1
	#getidf
	for eachkw in tempkeywordfreq:
		idfval=1
		for otherroleindex in finalroles:
			#print selfparentchildlist
			if otherroleindex in selfparentchildlist:
				continue

			for eachapk in finalroles[otherroleindex]:
				if eachkw in keyworddict[eachapk]:
					idfval=idfval+1
					break
		tempkeywordidf[eachkw]=idfval
	
				

	for eachelem in tempkeywordfreq:
		tempkeywordfreq[eachelem]=tempkeywordfreq[eachelem]*1.0/len(finalroles[roleindex])
		tfidf[eachelem]=tempkeywordfreq[eachelem]/tempkeywordidf[eachelem]
	rolekeyword[roleindex]=sorted(tempkeywordfreq.iteritems(), key=lambda d:d[1], reverse=True)
	tfidfrolekeyword[roleindex]=sorted(tfidf.iteritems(), key=lambda d:d[1], reverse=True)
	

  print "Number of roles: %s"%len(finalroles)


  file_op7=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/ORCAtfidf3.txt','w')
  try:
	for roleindex in tfidfrolekeyword:
		if len(finalroles[roleindex])<100 or len(finalroles[roleindex])>6000:
			continue

		for eachperm in indextorole[roleindex]:
			file_op7.write(eachperm +'	')
		file_op7.write('\n')
		for eachkeyword in firstklist(tfidfrolekeyword[roleindex],60):
			file_op7.write(eachkeyword[0]+', %s'%eachkeyword[1])
			file_op7.write('\n')
		file_op7.write('\n')
  finally:
	file_op7.close()

  file_op6=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/boot_completed3.txt','w')
  try:

	for roleindex in rolekeyword:
		if 'android.permission.RECEIVE_BOOT_COMPLETED' not in indextorole[roleindex]:
			continue

		for eachperm in indextorole[roleindex]:
			file_op6.write(eachperm +'	')
		file_op6.write('\n')
		print len(finalroles[roleindex])
		for eachkeyword in rolekeyword[roleindex]:
			file_op6.write(eachkeyword[0]+', %s'%eachkeyword[1])
			file_op6.write('\n')
		file_op6.write('\n')
  finally:
	file_op6.close()

  file_op5=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/500to200ORCArole_kw3.txt','w')
  try:

	for roleindex in rolekeyword:
		if len(finalroles[roleindex])<100 or len(finalroles[roleindex])>6000:
			continue

		for eachperm in indextorole[roleindex]:
			file_op5.write(eachperm +'	')
		file_op5.write('\n')
		#print len(rolekeyword[roleindex])
		for eachkeyword in rolekeyword[roleindex]:
			file_op5.write(eachkeyword[0]+', %s'%eachkeyword[1])
			file_op5.write('\n')
		file_op5.write('\n')
  finally:
	file_op5.close()


  file_op4=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/ORCArole_kw_topk3.txt','w')
  try:

	for roleindex in rolekeyword:
		if len(finalroles[roleindex])<100 or len(finalroles[roleindex])>6000:
			continue

		for eachperm in indextorole[roleindex]:
			file_op4.write(eachperm +'	')
		file_op4.write('\n')
		for eachkeyword in firstklist(rolekeyword[roleindex],60):
			file_op4.write(eachkeyword[0]+', %s'%eachkeyword[1])
			file_op4.write('\n')
		file_op4.write('\n')
  finally:
	file_op4.close()		

  file_op1=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/ORCARoles3.txt','w')
  try:
	for roleindex in finalroles:
		for eachperm in indextorole[roleindex]:
			file_op1.write(eachperm +'	')
		file_op1.write('\n')
		for eachapk in finalroles[roleindex]:
			file_op1.write(eachapk)
			file_op1.write('\n')
		file_op1.write('\n')
  finally:
	file_op1.close()

	
  file_op2=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/ORCAparentchild3.txt','w')
  try:
	for parentindex in parentchildrelat:
		#print indextorole[parentindex]
		for eachperm in indextorole[parentindex]:
			file_op2.write(eachperm +'	')
			#print eachperm
		file_op2.write('\n')

		for eachperm in indextorole[parentchildrelat[parentindex][0]]:
			file_op2.write(eachperm+'	')
		file_op2.write('\n')

		for eachperm in indextorole[parentchildrelat[parentindex][1]]:
			file_op2.write(eachperm +'	')
		file_op2.write('\n\n')
  finally:
	file_op2.close()	
  
  file_op3=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/ORCAdist3.txt','w')
  try:
	for roleindex in numofappsdict:
		file_op3.write(str(numofappsdict[roleindex])+'\n')
  finally:
	file_op3.close()		



def stadfordParser(sentencedict):

  for apkName in sentencedict:
    	rootDir='/home/zyqu/stanfordxml/'
    	list_dirs=os.walk(rootDir)
    	finishedapps=[]
    	for root, dirs, files in list_dirs:
		for d in dirs:       
			level2rootDir=os.path.join(root, d)
			app=os.path.basename(level2rootDir)
			finishedapps.append(app)

    	rootDir='/home/zyqu/stanfordtemp/'
    	list_dirs=os.walk(rootDir)
    	finishedtxts=[]
    	for root, dirs, files in list_dirs:
		for d in dirs:       
			level2rootDir=os.path.join(root, d)
			app=os.path.basename(level2rootDir)
			finishedtxts.append(app)


#	if (apkName in finishedapps) and (apkName in finishedtxts):
#		print 'Skip app: '+apkName
#		continue

	sentencecounter=0

	command="mkdir /home/zyqu/stanfordtemp/"+apkName
	tokenarrays=shlex.split(command)
	subprocess_execute(tokenarrays, 10, '/dev/null')

	command="mkdir /home/zyqu/stanfordxml/"+apkName
	tokenarrays=shlex.split(command)
	subprocess_execute(tokenarrays, 10, '/dev/null')

	#command="rm /home/zyqu/stanfordtemp/*"
	#tokenarrays=shlex.split(command)
	#subprocess_execute(tokenarrays, 10, '/dev/null')

	#command="rm /home/zyqu/stanfordxml/*"
	#tokenarrays=shlex.split(command)
	#subprocess_execute(tokenarrays, 10, '/dev/null')

	for eachSentence in sentencedict[apkName]:
		sentencecounter=sentencecounter+1
		#print eachSentence
		eachSentence=eachSentence.replace('"',"'")
		eachSentence=eachSentence.replace('\\',"")
		eachSentence=eachSentence.replace('>'," ")
		eachSentence=eachSentence.replace('<'," ")

		if len(eachSentence)<300 and eachSentence.find('&&')<0:
			continue

		while eachSentence.find('&&')>=0:
			eachSentence=eachSentence.replace('&&','&')
		eachSentence=eachSentence.replace('&',' and ')



		command="echo \""+eachSentence+"\""
		print command
		tokenarrays=shlex.split(command)
		txtpath="/home/zyqu/stanfordtemp/"+apkName+"/%s"%sentencecounter+".txt"
		subprocess_execute(tokenarrays, 10, txtpath)

		command="/home/zyqu/stanford-parser-full-2013-06-20/lexparser.sh "+txtpath#/home/zyqu/stanfordtemp.txt"# >"
		print command
		tokenarrays=shlex.split(command)
		xmlpath="/home/zyqu/stanfordxml/"+apkName+"/%s"%sentencecounter+".xml"
		newxmlpath="/home/zyqu/stanfordxml/"+apkName+"/new%s"%sentencecounter+".xml"
		subprocess_execute(tokenarrays, 500, xmlpath)
		#preprocessxmlTree(xmlpath,newxmlpath)


def Batchparse_xml(xmlrootpath):
    rootDir=xmlrootpath
    list_dirs=os.walk(rootDir)
    maindict={}
    phrasetypelist=[]
    redphrasetypelist=[]
    fwword=[]
    for root, dirs, files in list_dirs:
	for d in dirs:       
		level2rootDir=os.path.join(root, d)
		app=os.path.basename(level2rootDir)
		newroot=rootDir+app+'/'
		new_list_dirs=os.walk(newroot)
		keywordlist=[]
		for Nroot, Ndirs, Nfiles in new_list_dirs:
			for Nfile in Nfiles:
				filefullpath=os.path.join(Nroot, Nfile)
				filename=os.path.basename(filefullpath)
				if filename.find('new')>=0:
					#print filefullpath
					#parse_xml(filefullpath)
					keywordlist.extend(parse_xml(filefullpath))
		maindict[app]=keywordlist
		for eachphrase in keywordlist:
			temptypelist=[]
			for eachword in eachphrase:
				#print eachword
				wordtype=eachword[1]
				temptypelist.append(wordtype)
			if temptypelist not in phrasetypelist:
				phrasetypelist.append(temptypelist)
			redphrasetypelist.append(temptypelist)

		#print keywordlist
    file_op1=open('/home/zyqu/Research/Android_sec/parsexml/semant/data/TypePatterns.txt','w')
    try:
	for eachpattern in phrasetypelist:
		counter=0
		for redpattern in redphrasetypelist:
			if redpattern==eachpattern:
				counter=counter+1
		file_op1.write('%s'%eachpattern+'\n')
		file_op1.write('%s'%counter+'/%s\n'%len(redphrasetypelist))
		file_op1.write('\n')
    finally:
	file_op1.close()
    return maindict

def onlysinglenoun(phrasedict):
    	from nltk.corpus import stopwords
   	stopwords = stopwords.words('english')
    	lemmatizer = nltk.WordNetLemmatizer()
	maindict={}
	for apkName in phrasedict:
		wordlist=[]
		for eachphrase in phrasedict[apkName]:
			if len(eachphrase)>1:
				continue	
			word=eachphrase[0][0]
			if len(word)==0:
				continue
			if word.find('/')<0:
				wordlist.append(word)
			elif word.find('/')>=0:
				#print word
				tempwords=word.split('/')
				for eachtempword in tempwords:
					eachtempword=eachtempword.strip()
					if (eachtempword not in filteredlist) and (eachtempword not in stopwords):
						eachtempword=lemmatizer.lemmatize(eachtempword)
						for originalword in replacedict:
							if eachtempword in replacedict[originalword]:
								eachtempword=originalword

						#print eachtempword
						wordlist.append(eachtempword)

		if len(wordlist)>0:
			maindict[apkName]=wordlist
		print wordlist
	return maindict	

def twonouns(phrasedict):
    	from nltk.corpus import stopwords
   	stopwords = stopwords.words('english')
    	lemmatizer = nltk.WordNetLemmatizer()
	maindict={}
	for apkName in phrasedict:
		wordlist=[]
		for eachphrase in phrasedict[apkName]:
			if len(eachphrase)!=2:
				continue	
			word1=eachphrase[0][0]
			word2=eachphrase[1][0]
			wordtype1=eachphrase[0][1]
			wordtype2=eachphrase[1][1]
			if wordtype1=='N' and wordtype2=='N':
				if word1.find('/')<0 and word2.find('/')<0:
					word=word1+' '+word2
					word=" ".join(word.split())
					word=word.strip()
					wordlist.append(word)


				elif word1.find('/')>=0 or word2.find('/')>=0:
					#print word1+' '+word2
					word1list=word1.split('/')
					word2list=word2.split('/')
					for tempword1 in word1list:
						tempword1=tempword1.strip()
						if (tempword1 not in filteredlist) and (tempword1 not in stopwords):
							tempword1=lemmatizer.lemmatize(tempword1)
							for originalword in replacedict:
								if tempword1 in replacedict[originalword]:
									tempword1=originalword
						elif (tempword1 in filteredlist) or (tempword1 in stopwords):
							tempword1=''

						for tempword2 in word2list:
							tempword2=tempword2.strip()

							if (tempword2 not in filteredlist) and (tempword2 not in stopwords):
								tempword2=lemmatizer.lemmatize(tempword2)
								for originalword in replacedict:
									if tempword2 in replacedict[originalword]:
										tempword2=originalword
							elif (tempword2 in filteredlist) or (tempword2 in stopwords):
								tempword2=''

							word=tempword1+' '+tempword2
							word=" ".join(word.split())
							word=word.strip()
							#print word
							wordlist.append(word)


		if len(wordlist)>0:
			maindict[apkName]=wordlist
		print wordlist
	return maindict	

def adjnoun(phrasedict):
    	from nltk.corpus import stopwords
   	stopwords = stopwords.words('english')
    	lemmatizer = nltk.WordNetLemmatizer()
	maindict={}
	for apkName in phrasedict:
		wordlist=[]
		for eachphrase in phrasedict[apkName]:
			if len(eachphrase)!=2:
				continue	
			word1=eachphrase[0][0]
			word2=eachphrase[1][0]
			wordtype1=eachphrase[0][1]
			wordtype2=eachphrase[1][1]
			if wordtype1=='J' and wordtype2=='N':
				if word1.find('/')<0 and word2.find('/')<0:
					word=word1+' '+word2
					word=" ".join(word.split())
					word=word.strip()
					wordlist.append(word)
				elif word1.find('/')>=0 or word2.find('/')>=0:
					word1list=word1.split('/')
					word2list=word2.split('/')
					for tempword1 in word1list:
						tempword1=tempword1.strip()
						if (tempword1 not in filteredlist) and (tempword1 not in stopwords):
							tempword1=lemmatizer.lemmatize(tempword1)
							for originalword in replacedict:
								if tempword1 in replacedict[originalword]:
									tempword1=originalword
						elif (tempword1 in filteredlist) or (tempword1 in stopwords):
							tempword1=''

						for tempword2 in word2list:
							tempword2=tempword2.strip()

							if (tempword2 not in filteredlist) and (tempword2 not in stopwords):
								tempword2=lemmatizer.lemmatize(tempword2)
								for originalword in replacedict:
									if tempword2 in replacedict[originalword]:
										tempword2=originalword
							elif (tempword2 in filteredlist) or (tempword2 in stopwords):
								tempword2=''

							word=tempword1+' '+tempword2
							word=" ".join(word.split())
							word=word.strip()
							#print word
							wordlist.append(word)

							
							
		if len(wordlist)>0:
			maindict[apkName]=wordlist
		print wordlist
	return maindict			

def BatchpreprocessxmlT(xmlrootpath):
    rootDir=xmlrootpath
    list_dirs=os.walk(rootDir)
    for root, dirs, files in list_dirs:
	for d in dirs:       
		level2rootDir=os.path.join(root, d)
		app=os.path.basename(level2rootDir)
		newroot=rootDir+app+'/'
		new_list_dirs=os.walk(newroot)
		for Nroot, Ndirs, Nfiles in new_list_dirs:
			for Nfile in Nfiles:
				filefullpath=os.path.join(Nroot, Nfile)
				filename=os.path.basename(filefullpath)
				if filename.find('new')<0:
					xmlpath=filefullpath
					newxmlpath=newroot+'new'+filename
					preprocessxmlTree2(xmlpath,newxmlpath)

    


def preprocessxmlTree2(xmlpath,newxmlpath):
    keeplist=['<','>','/',' ','\t','\n','\r','-']
    nums=['0','1','2','3','4','5','6','7','8','9']
    filein=open(xmlpath,'r')
    fileout=open(newxmlpath,'w')
    alllines = filein.readlines()
    reducecounter=0
    rootfinished=False
    for line in alllines:
	originalline=line
	if line.find('</ROOT>')>=0:
		rootfinished=True

	line=line.replace('$','')
	if line.find(',')>0:
		if line.find(', ')<0:
			reducecounter=reducecounter+1
		continue
	Skipflag=False
	if line.find('-LRB-')>=0 or line.find('-RRB-')>=0:
		Skipflag=True

	if line.find('<-')>=0 or line.find('-/>')>=0 or line.find('</-')>=0 or line.find('->')>=0:
		Skipflag=True

	for eachnum in nums:
		line=line.replace(eachnum,'')
	while line.find('<-')>=0:
		line=line.replace('<-','<')
	while line.find('->')>=0:
		line=line.replace('->','>')
	while line.find('</-')>=0:
		line=line.replace('</-','</')
	while line.find('-/>')>=0:
		line=line.replace('-/>','/>')

	#line=line.replace('-',' ')
	line=line.replace('\\/','XXXXX') #special delimit for word type as word1/word2

	if line.find('</>')>=0 or line.find('<>')>=0:
		Skipflag=True

	for c in line:
		if c.isalpha()==False and (c not in keeplist):
			Skipflag=True

	if Skipflag==True:
		reducecounter=reducecounter+1
		continue	
			
        fileout.write(line)
	if rootfinished==True:
		break
    fileout.close()
    filein.close()
    #print newxmlpath
    #print reducecounter
    #print newxmlpath
    if rootfinished==True:
    	parse_xml(newxmlpath)
    elif rootfinished==False:
	command='rm '+newxmlpath
	os.system(command)
	command='rm '+xmlpath
	os.system(command)


	 
def preprocessxmlTree(xmlpath,newxmlpath):
    keeplist=['<','>','/',' ','\t','\n','\r']#'-','/'
    filein=open(xmlpath,'r')
    fileout=open(newxmlpath,'w')
    alllines = filein.readlines()
    reducecounter=0
    for line in alllines:
	line=line.replace('$','')
	if line.find(',')>0:
		if line.find(', ')<0:
			reducecounter=reducecounter+1
		continue
	Skipflag=False
	for c in line:
		if c.isalpha()==False and (c not in keeplist):
			#print c,
			#print "Problem: "+line

			Skipflag=True
	if Skipflag==True:
		reducecounter=reducecounter+1
		continue	
			
        fileout.write(line)
    fileout.close()
    filein.close()
    print newxmlpath
    print reducecounter
    parse_xml(newxmlpath)



def parsekeyword(sourcepath):
    file_object=open(sourcepath)
    try:
    	alllines = file_object.readlines()
        maindict={}
	apkname=''
	keywords=[]
	for line in alllines:
		line=line.strip()
		if line.endswith('.apk'):
			apkname=line
			continue
		if len(line)==0:
			if len(apkname)>0 and (apkname not in maindict) and len(keywords)>0:
				maindict[apkname]=keywords				
			keywords=[]
			apkname=''
			continue
		keywords.append(line.lower())
    finally:
        file_object.close()
    	return maindict



def parse_xml(file_path):

    keeplist=['sms','facebook','photo','mms']
    from nltk.corpus import stopwords
    lemmatizer = nltk.WordNetLemmatizer()
    stopwords = stopwords.words('english')   
    dom = xml.dom.minidom.parse(file_path)
    root = dom.documentElement
    NPlist = root.getElementsByTagName('NP')
    nplist=[]
    for eachNP in NPlist:
	targetflag=True
	NP=[]
	for NPchild in eachNP.childNodes:
		for NPchildchild in NPchild.childNodes:
			if len(NPchildchild.childNodes)>0:
				targetflag=False
			elif len(NPchildchild.childNodes)==0:
				word='%s'%NPchildchild.nodeName
				wordtype='%s'%NPchild.nodeName
				if word.find('XXXXX')>=0:
					word=word.replace('XXXXX','/')# TODO
  				accepted = bool(2 <= len(word) <= 40 and word.lower() not in stopwords)
				if word=='#text' or (word.lower() in filteredlist) or wordtype=='DT' or wordtype=='WDT' or wordtype=='CD' or wordtype=='PRP' or wordtype.startswith('V') or wordtype.startswith('R') or accepted==False:
					continue

#refine the word

				word=" ".join(word.split())
				word=word.strip()
				word=word.lower()
				if wordtype.startswith('N'):
					if word not in keeplist:
						word=lemmatizer.lemmatize(word)
					wordtype='N'

				if wordtype.startswith('J'):
					word=lemmatizer.lemmatize(word,'a')
					wordtype='J'

				

				for originalword in replacedict:
					if word in replacedict[originalword]:
						word=originalword

######




				NP.append((word, wordtype))
				#if len(NP)==0:
					#NP='%s'%NPchildchild.nodeName
				#elif len(NP)>0:
					#NP=NP+' %s'%NPchildchild.nodeName
	if targetflag==False:
		continue

	containNoun=False
	for eachword in NP:
		if eachword[1].startswith('N'):
			containNoun=True
	if containNoun==False:
		continue

	containFW=False
	for eachword in NP:
		if eachword[1]=='FW':
			containFW=True
	if containFW==True:
		continue


	containWP=False
	for eachword in NP:
		if eachword[1]=='WP':
			containWP=True
	if containWP==True:
		continue

	containCC=False
	for eachword in NP:
		if eachword[1]=='CC':
			containCC=True
	if containCC==True:
		continue

	containPDT=False
	for eachword in NP:
		if eachword[1]=='PDT':
			containPDT=True
	if containPDT==True:
		continue

	containPOS=False
	for eachword in NP:
		if eachword[1]=='POS':
			containPOS=True
	if containPOS==True:
		continue


	if len(NP)>0:
		if len(NP)==2 and NP[0][0]==NP[1][0] and NP[0][1]==NP[1][1]:
			tempNP=[(NP[0][0],NP[0][1])]
			NP=tempNP
		nplist.append(NP)
	#NP=NP.replace('#text','')
	#NP=" ".join(NP.split())
	#print NP
    #if file_path=='/home/zyqu/stanfordxml/com.needom.recorder.apk/new7.xml':
    	#for eachelem in nplist:
		#print eachelem
    	#print '\n'
    #print nplist  
    #for eachelem in nplist:
	#print eachelem
    #print '\n'
    return nplist

def subprocess_execute(command, time_out, filepath):
    # launching the command 
    f = open(filepath,"w")   
    c = subprocess.Popen(command,stdout=f)
    # now waiting for the command to complete
    t = 0
    while t < time_out and c.poll() is None:
        time.sleep(1)  # (comment 1)
        t += 1
    # there are two possibilities for the while to have stopped:
    if c.poll() is None:
        # in the case the process did not complete, we kill it
        c.terminate()
        # and fill the return code with some error value
        returncode = -1  # (comment 2)
    else:                 
        # in the case the process completed normally
        returncode = c.poll()
    f.close()
    return returncode


grammar = r"""
NBAR:
{<NN.*>?<NN.*>} # Nouns and Adjectives, terminated with Nouns
"""


def wordtag(sentencedict):
  import nltk
  maindict={}

  for apkName in sentencedict:
	for eachSentence in sentencedict[apkName]:
		print eachSentence
		tokens=nltk.word_tokenize(eachSentence)
		postoks = nltk.tag.pos_tag(tokens)
		chunker = nltk.RegexpParser(grammar)
		tree = chunker.parse(postoks)
		terms = get_terms(tree)
		newterms=[]
		for term in terms:
			newterm=[]
			print term
			#for word in term:
				#for originalword in replacedict:
					#if word in replacedict[originalword]:
						#word=originalword
				

def leaves(tree):
#"""Finds NP (nounphrase) leaf nodes of a chunk tree."""
  for subtree in tree.subtrees(filter = lambda t: t.node=='NBAR'):
	yield subtree.leaves()

def normalise(word):
#"""Normalises words to lowercase and stems and lemmatizes it."""
  import nltk
  lemmatizer = nltk.WordNetLemmatizer()
  stemmer = nltk.stem.porter.PorterStemmer()

  #word = stemmer.stem_word(word)
  word = lemmatizer.lemmatize(word)
  word = word.lower()
  return word

def acceptable_word(word):
#"""Checks conditions for acceptable word: length, stopword."""
  from nltk.corpus import stopwords
  stopwords = stopwords.words('english')
  accepted = bool(2 <= len(word) <= 40 and word.lower() not in stopwords)
  return accepted

def get_terms(tree):
  for leaf in leaves(tree):
	term = [ normalise(w) for w,t in leaf if acceptable_word(w) ]
	yield term
		
def removeredunt(lst):
	mainlst=[]
	for elem in lst:
		if elem not in mainlst:
			mainlst.append(elem)
	return mainlst

def dictmerge(keyworddict1,keyworddict2):
	maindict={}
	for eachkey in keyworddict1:
		wordlist1=keyworddict1[eachkey]
		if eachkey not in keyworddict2:
			maindict[eachkey]=wordlist1


		if eachkey in keyworddict2:
			wordlist2=keyworddict2[eachkey]
			wordlist1.extend(wordlist2)
			maindict[eachkey]=wordlist1
	for eachkey in keyworddict2:
		if eachkey in keyworddict1:
			continue
		maindict[eachkey]=keyworddict2[eachkey]

	for elem in maindict:
		maindict[elem]=removeredunt(maindict[elem])
	return maindict


def groupappend(keyworddict,replaceworddict):
        maindict={}
	for apkName in keyworddict:
		originalwords=keyworddict[apkName]
		newwords=[]
		for eachword in originalwords:
			newwords.append(eachword)
			if eachword in replaceworddict:
				newwords.extend(replaceworddict[eachword])
		maindict[apkName]=newwords
	
	for elem in maindict:
		maindict[elem]=removeredunt(maindict[elem])
	return maindict	


#get a list of permission where the # of apps have this permission over
#threshold
def permpercent(permdict):
    maindict={}
    threshold=0
    numofapps=len(permdict)
    freqdict={}
    for apkName in permdict:
        for eachPerm in permdict[apkName]:
            if eachPerm not in freqdict:
                freqdict[eachPerm]=1
            elif eachPerm in freqdict:
                freqdict[eachPerm]=freqdict[eachPerm]+1

    for eachPerm in freqdict:
        if freqdict[eachPerm]>threshold:
            print eachPerm +'\t%s'%freqdict[eachPerm]+' in %s'%numofapps
            maindict[eachPerm]=freqdict[eachPerm]
    return maindict
            

def update_repdict(permdict,keyworddict,replaceworddict,targetperm,numappsperm):
   
    tempdict={}
    maindict={} #the output of updated replaceworddict

    finishpercent=0.5
    orig_thres=0.6
    new_thres=0.5
    increase_rate=(1/orig_thres)**(1.0/finishpercent/numappsperm)
    decrease_rate=(new_thres/1.0)**(1.0/finishpercent/numappsperm)

    print targetperm

    for eachgroupkey in replaceworddict:
        #if len(replaceworddict[eachgroupkey])<5:
            #continue

	templst=[] # the lst of (word,rel_val) being updated
	for eachrepwd in replaceworddict[eachgroupkey]:
		templst.append(eachrepwd)

	

		
	for eachApp in keyworddict:

		thiswordlst=keyworddict[eachApp]
                wdtoremove=[]
		if targetperm in permdict[eachApp]:
			for relwdindex in range(len(templst)):
				if templst[relwdindex][0] in thiswordlst:
					if templst[relwdindex][1]*increase_rate<=1.0:
                                                #print templst[relwdindex]
						templst[relwdindex][1]=templst[relwdindex][1]*increase_rate
                                                #print templst[relwdindex]


		elif targetperm not in permdict[eachApp]:
			for relwdindex in range(len(templst)):
				if templst[relwdindex][0] in thiswordlst:
					if templst[relwdindex][1]*decrease_rate>=new_thres:
                                                #print templst[relwdindex]
						templst[relwdindex][1]=templst[relwdindex][1]*decrease_rate
                                                #print templst[relwdindex]
					elif templst[relwdindex][1]*decrease_rate<new_thres:
                                                wdtoremove.append(relwdindex)
                                                #print templst[relwdindex]
                                                #print (templst[relwdindex][0],templst[relwdindex][1])
						#print len(templst)
                                                #templst.remove(templst[relwdindex])
                                                #print len(templst)
                for eachremoveindex in wdtoremove:
                        #print "In list",
                        #print templst[eachremoveindex]
                        templst.remove(templst[eachremoveindex])

        maindict[eachgroupkey]=templst
	reducedratio=len(templst)*1.0/len(replaceworddict[eachgroupkey])
	tempdict[eachgroupkey]=reducedratio
	
	
    return sorted(tempdict.iteritems(), key=lambda d:d[1], reverse=True)
    

if __name__=="__main__":
  result=Map()
  proj_path=os.path.abspath('..')

  filein=open(proj_path+'/data/49183_apps_descdict.json','r')
  keyworddict2=json.load(filein)
  filein.close()
  print len(keyworddict2)

  filein=open(proj_path+'/data/49183_apps_permdict.json','r')
  permissiondict=json.load(filein)
  filein.close()

  onlykeypermdict=result.getkeyperm(permissiondict)

  intersectpermissiondict={}
  for elem in onlykeypermdict:
  	if elem in keyworddict2:
		intersectpermissiondict[elem]=onlykeypermdict[elem]
  keyworddict={}
  for elem in keyworddict2:
  	if elem in intersectpermissiondict:
		keyworddict[elem]=keyworddict2[elem]

  print len(keyworddict)
  print len(intersectpermissiondict)
  relatedictfile=open(proj_path+'/data/49183_100_0_67_5_relateddict.json','r')
  replaceworddict = json.load(relatedictfile)	
  relatedictfile.close()


  rootDir=proj_path+'/evaluation/training/'
  list_dirs=os.walk(rootDir)
  count=0
  for root, dirs, files in list_dirs:
        for d in dirs:
            targetperm=d
            if targetperm!='android.permission.WRITE_SETTINGS':
                continue

            print targetperm
            level2rootDir=os.path.join(root, d)
            newroot=rootDir+targetperm+'/'
            new_list_dirs=os.walk(newroot)
            for Nroot, Ndirs, Nfiles in new_list_dirs:
                for Nfile in Nfiles:
                    filefullpath=os.path.join(Nroot,Nfile)
                    filename=os.path.basename(filefullpath)
                    fold=filename.replace('trainset','')
                    fold=fold.replace('.json','')
                    #if fold not in ['9','1','4','8']:
                        #continue
                    f=open(filefullpath,'r')
                    trainapplst=json.load(f)
                    f.close()
                    newnewfscore(intersectpermissiondict,keyworddict,replaceworddict,targetperm,trainapplst,fold)

  
  
  #permfreqdic=permpercent(intersectpermissiondict)
  #resdict={}
  #looplimit=3
  #maincounter=0
  #for eachPerm in permfreqdic:
    #if maincounter>looplimit:
        #break
    #maincounter=maincounter+1
    #resdict[eachPerm]=update_repdict(intersectpermissiondict,keyworddict,replaceworddict,eachPerm, permfreqdic[eachPerm])
    #file_o=open(proj_path+'/data/softappendres/reducegroup'+eachPerm+'.txt','w')
    #try:
        #file_o.write(eachPerm+'\n')
        #for eachgroup in resdict[eachPerm]:
            #file_o.write(eachgroup[0]+'\t%s\n'%eachgroup[1])
    #finally:
        #file_o.close()



  





import numpy as np



#MAX_SAMPLE = 25
#EPS= 15
MAX_SAMPLE = 100
EPS= 1.0/0.67-1


def getrelatedwords(eps,wordindex,matrix):
	relatedwords=[]	
	for wordindex2 in range(len(matrix[wordindex])):
		if wordindex==wordindex2:
			continue
		if matrix[wordindex][wordindex2]<eps and wordl[wordindex2].find('please')<0:
			#relatedwords.append(wordl[wordindex2])
			relval=1/(matrix[wordindex][wordindex2]+1)
			relatedwords.append((wordl[wordindex2],relval))
	if len(relatedwords)<MAX_SAMPLE:
		return relatedwords
	elif len(relatedwords)>=MAX_SAMPLE:
		return getrelatedwords(eps*0.9,wordindex,matrix)
	

def formatconv(X):
	numofwords=len(X[0])
	file_op=open('dictform.txt','w')
	try:
		file_op.write('%s '%numofwords+'%s\n'%numofwords)
		for rowindex in range(len(X)):
			for colindex in range(len(X[rowindex])):
				if colindex < len(X[rowindex]) - 1:
					file_op.write('%s '%X[rowindex][colindex])
				elif colindex == len(X[rowindex]) - 1:
					file_op.write('%s\n' %X[rowindex][colindex]) 
	finally:
		file_op.close()

def preconvert_dist_M(X):
    matrix=[]

    for rolindex in range(len(X)):
        temprol=[]
        for colindex in range(len(X[rolindex])):
            if X[rolindex][colindex] != X[rolindex][colindex]:
                #print X[rolindex][colindex]
                temprol.append(99999.99)
                continue
            if X[rolindex][colindex] == 0.0:
                #print X[rolindex][colindex]
                temprol.append(99999.99)
                continue
            temprol.append(1/X[rolindex][colindex]-1)
        matrix.append(temprol)

    #file_o=open('pre_dist_disM5.json','w')
    #file_o.write(json.dumps(matrix))
    #file_o.close()
    return matrix



import json
f = open('49183_disM10.txt','r') #is a relatedness matrix, not the distance!
X = json.load(f)
f.close()

#print len(X)
#print X[0]

dist_matrix = preconvert_dist_M(X) #convert to distance matrix!
#print len(dist_matrix)
#print dist_matrix[0][1]

wordl = []
for line in open('49183_wordsmore15.txt','r'):
    wordl.append(line[:line.index('\t')])
print len(wordl)

highfreqwordl=[]
for line in open('49183_wordsmore15.txt','r'):
    highfreqwordl.append(line[:line.index('\t')])
print len(highfreqwordl)


maindict={}
for wordindex in range(len(wordl)):
    if wordl[wordindex] not in highfreqwordl or wordl[wordindex].find('please')>=0:
        continue
    relatedwords=getrelatedwords(EPS,wordindex,dist_matrix)
    if len(relatedwords)>=5:# threshold on the size of group
        maindict[wordl[wordindex]]=relatedwords
        #print wordl[wordindex], relatedwords

print len(maindict)

file_op=open('49183_100_0_67_5_relateddict.json','w')
try:
	file_op.write(json.dumps(maindict))
finally:
	file_op.close()



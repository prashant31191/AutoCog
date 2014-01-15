import json
import glob
from pprint import pprint

dataW = {}

json_data = open('22458_apps_desctext.json')
dataD = json.load(json_data)

ident = None
flag = None
for line in open( 'output_Oct28_20_56_Read_Contact.txt' ):
	line = line.strip()
	if line:
		if ident is None:
			ident = line
		elif flag is None:
			flag = (line == 'true')
			dataW[ident] = [];
		elif flag:
			dataW[ident].append(line)
	else:
		ident = None
		flag = None

dataO = {}
ident = None
flag = None
for line in open( 'new_noskip_0_READ_CONTACTS.txt' ):
	line = line.strip()
	if line:
		if ident is None:
			ident = line
		elif flag is None:
			flag = (line == 'true')
			dataO[ident] = [];
		elif flag:
			np = line.split('\t')[2]
			verb = line.split('\t')[3]
			if len(filter(lambda pair: (pair['verb'] == verb) & (pair['np'] == np), dataO[ident])) == 0:
				dataO[ident].append({'np': np, 'verb': verb})
	else:
		ident = None
		flag = None

data = []

#print len(dataO), len(dataW), len(dataD)

#print len((set(dataO.keys()) & set(dataW.keys()) & set(dataD.keys())))

sentcount=0
whypercount=0
for app in dataO: #(set(dataO.keys()) & set(dataW.keys()) & set(dataD.keys())):
        item = {}
        item['appname'] = app
        item['desc'] = dataD[app]
        item['totalnum'] = len(dataD[app])
        sentcount=sentcount+ len(dataD[app])
        item['whypernum'] = len(dataW[app])
        whypercount=whypercount+len(dataW[app])
        item['whypersents'] = dataW[app]
        item['ournum'] = len(dataO[app])
        item['ourpairs'] = dataO[app]
        data.append(item)

print len(data)
fileout=open('new_49183_manul_res_Read_Contact.json','w')
fileout.write(json.dumps(data))
fileout.close()


fileout=open('new_49183_manul_res_Read_Contact.txt','w')
for eachelem in data:
    fileout.write('ApkName: '+eachelem['appname']+'\n')
    fileout.write('ournum: %s\n'%eachelem['ournum'])
    fileout.write('ourpairs: %s'%eachelem['ourpairs']+'\n')
    fileout.write('whypernum: %s\n'%eachelem['whypernum'])
    if eachelem['whypernum']>0:
        print eachelem['whypersents']
    fileout.write('whypersents: %s'%eachelem['whypersents']+'\n')
    fileout.write('totoalsents: %s\n'%eachelem['totalnum'])
    fileout.write('desc: %s'%eachelem['desc'])
    fileout.write('\n\n')
fileout.close()


print "Total number of sentences: %s"%sentcount
print "Totoal number of whyper: %s"%whypercount

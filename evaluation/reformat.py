import json
import glob
from pprint import pprint

print "reformatiing the Description-to-Permission Relatedness Model..."

for filename in glob.iglob('newselectedVerbNP/*/*.json'):
	json_data = open(filename)

	out = open(filename+'.txt','w+')

	data = json.load(json_data)

	for noun in data:
		out.write(noun)
		out.write('\n')	
		for verb in data[noun]:
			out.write(verb)
			out.write('\n')
		out.write('\n')	
'''
json_data = open('new49183_apps_NPverb.json')
out = open('new49183_apps_NPverb.txt','w+')
data = json.load(json_data)

for app in data:
 	out.write(app)
 	out.write('\n')
 	for pair in data[app]:
 		out.write(pair[0])
 		out.write('\t')
 		out.write(pair[1])
 		out.write('\n')
 	out.write('\n')
'''

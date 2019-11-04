import json
import os
h = []
for filename in os.listdir('./'):
    if filename.endswith(".json"): 
		with open(filename) as json_file:
			data = json.load(json_file)
			for d in data:
				d['name']= filename.split('.json')[0]
				h.append(d)

with open('../compiled.json', 'w') as outfile:
    json.dump(h, outfile)
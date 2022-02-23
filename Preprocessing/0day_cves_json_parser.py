import json
import pandas as pd

f = open('cve_0day_refs_data.json')
data = json.load(f)

cve_ids = []
path_dates = []

for entry in data:
    print(entry['cve-id'])
    print(len(entry['refs']))
    cve_ids.append(entry['cve-id'])
    for ref in entry['refs']:
        print(ref[1].split()[0])
    # if len(len(entry['refs'])) == 1:
    #
import json

dir_path = "../Files/NVD-JSON"

file_path = '../Files/NVD-JSON/nvdcve-1.1-2015.json'

f = open(file_path)

data = json.load(f)

cve_list = data["CVE_Items"]

for cve in cve_list:
    # print(cve["references"])
    ref = cve["cve"]["references"]["reference_data"]
    print(ref)
    break

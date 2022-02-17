import json
import os
import pandas as pd

# Dir path that contains all the json files
# dir_path = "C:/Users/SYL/Desktop/CALSysLab/Code/Files/NVD-JSON/"
dir_path = "../Files/NVD-JSON/"

# Get all the files
files = os.listdir(dir_path)

# Initialize a list to store all the cve-ids
patched_cves = []

# Go thru each file
for f in files:
    print(f)
    print(dir_path + f)
    # Open the json file
    json_file = open(dir_path + f, encoding="utf8")
    data = json.load(json_file)

    # Get all the cves
    cve_list = data["CVE_Items"]

    cur_patched_cves = []
    
    # Go thru each cve
    for cve in cve_list:
        # Get the CVE-ID
        cve_id = cve["cve"]["CVE_data_meta"]["ID"]

        # Get the refs
        refs = cve["cve"]["references"]["reference_data"]
        cve_patched = False

        # Go thru each ref
        for ref in refs:
            tags = ref['tags']
            # Go thru each tag
            for tag in tags:
                # Check if a ref is Patch
                if "Patch" in tag:
                    cve_patched = True
                    break

        # Add the cve-id that has patch refs
        if cve_patched:
            cur_patched_cves.append(cve_id)

    patched_cves.append(cur_patched_cves)

# data = {"CVE ID": patched_cves}
# df = pd.DataFrame(data)
# df.to_csv("patched_cves.csv", index=False)

for i in range(len(files)):
    data = {"CVE ID": patched_cves[i]}
    df = pd.DataFrame(data)
    file_name = "patched_cves_" + str(i) + ".csv" 
    df.to_csv(file_name, index=False)



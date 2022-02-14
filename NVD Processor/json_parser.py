import json
import os
import pandas as pd

# Dir path that contains all the json files
dir_path = "../Files/NVD-JSON/"

# Get all the files
files = os.listdir(dir_path)

# Initialize a list to store all the cve-ids
patched_cves = []

# Go thru each file
for f in files:
    # Open the json file
    json_file = open(dir_path + f)
    data = json.load(json_file)

    # Get all the cves
    cve_list = data["CVE_Items"]
    
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
            patched_cves.append(cve_id)

data = {"CVE ID": patched_cves}
df = pd.DataFrame(data)
df.to_csv("patched_cves.csv", index=False)



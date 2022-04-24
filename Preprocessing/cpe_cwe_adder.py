import json
import os
import pandas as pd

# Zero Day Exploit Files
zero_day_file1 = pd.read_csv("../Files/selected_zero_day_negative_cases_with_zdi.csv")
zero_day_file2 = pd.read_csv("../Files/selected_zero_day_positive_cases_with_zdi.csv")
zero_day_file3 = pd.read_csv("../Files/remaining_zero_day_negative_cases_with_zdi.csv")

zero_day_files = [zero_day_file1, zero_day_file2, zero_day_file3]

for zero_day_file in zero_day_files:
    zero_day_file['CWE ID'] = 'None'
    zero_day_file['Num of CPE'] = 0
    zero_day_file['Num of Refs'] = 0
    zero_day_file['Refs'] = 'None'

# Dir path to nvd json files
dir_path = "../Files/NVD-JSON/"

# Get all the json files
files = os.listdir(dir_path)

# Go thru each json file
for file in files:
    pdf = pd.read_json(dir_path + file)
    xdf = pdf['CVE_Items'].to_dict()

    # Go thru each cve-id
    for i in xdf.keys():
        cve_id = (xdf[i]['cve']['CVE_data_meta']['ID']).lower()
        cwe_id = ''
        num_of_cpe = 0
        try:
            cwe_id = xdf[i]['cve']['problemtype']['problemtype_data'][0]['description'][0]['value']
        except IndexError:
            pass

        affected_cpe = []
        def get_cpe(nd):
            if len(nd['children']) > 0:
                # not empty
                for child in nd['children']:
                    get_cpe(child)
            else:
                # empty and base case
                for match in nd['cpe_match']:
                    # print(match['cpe23Uri'])
                    affected_cpe.append(match['cpe23Uri'])

        nodes_list = xdf[i]['configurations']['nodes']
        for node in nodes_list:
            get_cpe(node)

        num_of_cpe = len(affected_cpe)

        refs = xdf[i]["cve"]["references"]["reference_data"]

        num_of_refs = len(refs)
        ref_srs = ''

        for ref in refs:
            if ('Third Party Advisory' in ref['tags'] or 'VDB Entry' in ref['tags'] or 'Vendor Advisory' in ref['tags']) and not 'Exploit' in ref['tags'] and not 'Patch' in ref['tags']:
                ref_srs += str(ref['refsource']) + ' '

        for zero_day_file in zero_day_files:
            zero_day_file.loc[zero_day_file['CVE-ID'] == cve_id, ['CWE ID', 'Num of CPE', 'Num of Refs', 'Refs']] = [cwe_id, num_of_cpe, num_of_refs, ref_srs]
        print(cve_id)

zero_day_file1.to_csv('selected_zero_day_negative_cases_with_zdi.csv', index=False)
zero_day_file2.to_csv('selected_zero_day_positive_cases_with_zdi.csv', index=False)
zero_day_file3.to_csv('remaining_zero_day_negative_cases_with_zdi.csv', index=False)



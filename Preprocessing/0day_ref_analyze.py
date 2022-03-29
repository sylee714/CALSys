# import os
import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict

# ['Broken Link', 'Exploit', 'Issue Tracking', 'Mailing List', 'Mitigation', 'Not Applicable', 'Patch',
# 'Permissions Required', 'Press/Media Coverage', 'Product', 'Release Notes', 'Technical Description',
# 'Third Party Advisory', 'Tool Signature', 'URL Repurposed', 'US Government Resource', 'VDB Entry', 'Vendor Advisory']
def type_to_index(type_str):
    if type_str == 'Broken Link':
        return 0
    elif type_str == 'Exploit':
        return 1
    elif type_str == 'Issue Tracking':
        return 2
    elif type_str == 'Mailing List':
        return 3
    elif type_str == 'Mitigation':
        return 4
    elif type_str == 'Not Applicable':
        return 5
    elif type_str == 'Patch':
        return 6
    elif type_str == 'Permissions Required':
        return 7
    elif type_str == 'Press/Media Coverage':
        return 8
    elif type_str == 'Product':
        return 9
    elif type_str == 'Release Notes':
        return 10
    elif type_str == 'Technical Description':
        return 11
    elif type_str == 'Third Party Advisory':
        return 12
    elif type_str == 'Tool Signature':
        return 13
    elif type_str == 'URL Repurposed':
        return 14
    elif type_str == 'US Government Resource':
        return 15
    elif type_str == 'VDB Entry':
        return 16
    elif type_str == 'Vendor Advisory':
        return 17



def toDate(date_str):
    year, month, day = date_str.split('-')
    date_obj = datetime.datetime(int(year), int(month), int(day))
    return date_obj

def cve_0day_refs_data_processor():
    f = open('cve_0day_refs_analyze_data.json')
    data = json.load(f)

    # {ref_domain_name: [{type1: # of occurrences}, {type2: # of occurrences}, ...]}
    ref_data = {}

    # Go thru each cve-id
    for entry in data:
        # Go thru each ref
        for ref in entry["refs"]:
            # Check if the ref's url is already in the dict.
            # If it's new, then add it
            if ref[0] not in ref_data.keys():
                ref_data[ref[0]] = [0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0]

            # Go thru each type of the current reference
            for ref_type in ref[1]:
                ref_data[ref[0]][type_to_index(ref_type)] += 1

    # Sort it by the url
    sorted_ref_data = OrderedDict(sorted(ref_data.items()))

    urls = []
    type1 = []
    type2 = []
    type3 = []
    type4 = []
    type5 = []
    type6 = []
    type7 = []
    type8 = []
    type9 = []
    type10 = []
    type11 = []
    type12 = []
    type13 = []
    type14 = []
    type15 = []
    type16 = []
    type17 = []
    type18 = []
    types = [type1, type2, type3, type4, type5, type6,
             type7, type8, type9, type10, type11, type12,
             type13, type14, type15, type16, type17, type18]

    for key, val in sorted_ref_data.items():
        urls.append(key)
        for i in range(len(val)):
            types[i].append(val[i])

    # ['Broken Link', 'Exploit', 'Issue Tracking', 'Mailing List', 'Mitigation', 'Not Applicable', 'Patch',
    # 'Permissions Required', 'Press/Media Coverage', 'Product', 'Release Notes', 'Technical Description',
    # 'Third Party Advisory', 'Tool Signature', 'URL Repurposed', 'US Government Resource', 'VDB Entry', 'Vendor Advisory']
    # Turn the extracted data into pandas
    zero_day_refs_analyze = pd.DataFrame({
        "URL": urls,
        "Broken Link": type1,
        "Exploit": type2,
        "Issue Tracking": type3,
        "Mailing List": type4,
        "Mitigation": type5,
        "Not Applicable": type6,
        "Patch": type7,
        "Permissions Required": type8,
        "Press/Media Coverage": type9,
        "Product": type10,
        "Release Notes": type11,
        "Technical Description": type12,
        "Third Party Advisory": type13,
        "Tool Signature": type14,
        "URL Repurposed": type15,
        "US Government Resource": type16,
        "VDB Entry": type17,
        "Vendor Advisory": type18
    })

    # Write to a file
    zero_day_refs_analyze.to_csv("zero_day_refs_analyze.csv", index=False)

# cve_0day_refs_data_processor()


data = pd.read_csv("zero_day_refs_analyze.csv")
data["Total"] = data.sum(axis=1)
total_top_ten = data.nlargest(10, 'Total')
broken_link_top_ten = data.nlargest(10, 'Broken Link')
exploit_top_ten = data.nlargest(10, 'Exploit')
issue_tracking_top_ten = data.nlargest(10, 'Issue Tracking')
mailing_list_top_ten = data.nlargest(10, 'Mailing List')
mitigation_top_ten = data.nlargest(10, 'Mitigation')
not_applicable_top_ten = data.nlargest(10, 'Not Applicable')
patch_top_ten = data.nlargest(10, 'Patch')
permissions_required_top_ten = data.nlargest(10, 'Permissions Required')
press_media_coverage_top_ten = data.nlargest(10, 'Press/Media Coverage')
product_top_ten = data.nlargest(10, 'Product')
release_notes_top_ten = data.nlargest(10, 'Release Notes')
technical_description_top_ten = data.nlargest(10, 'Technical Description')
third_party_advisory_top_ten = data.nlargest(10, 'Third Party Advisory')
tool_signature_top_ten = data.nlargest(10, 'Tool Signature')
url_repurposed_top_ten = data.nlargest(10, 'URL Repurposed')
us_gov_resource_top_ten = data.nlargest(10, 'US Government Resource')
vdb_entry_top_ten = data.nlargest(10, 'VDB Entry')
vendor_advisory_top_ten = data.nlargest(10, 'Vendor Advisory')

vendor_advisory_top_ten.plot.bar(x="URL", y="Vendor Advisory", rot=70, title="Vendor Advisory Top 10")
plt.show()





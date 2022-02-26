import json
import csv
import pandas as pd
import datetime

def toDate(date_str):
    year, month, day = date_str.split('-')
    date_obj = datetime.datetime(int(year), int(month), int(day))
    return date_obj

def toDate2(date_str):
    month, day, year = date_str.split('/')
    date_obj = datetime.datetime(int(year), int(month), int(day))
    return date_obj

def edb_zdi_processor():
    file_path = "../Database Files/edb_zdi.csv"
    data = pd.read_csv(file_path)
    cve_ids = []
    exploit_dates = []
    # Need a source column?
    # source = []
    print("edb_zdi_processor")
    for index, row in data.iterrows():
        if not pd.isna(row['edb_date']):
            cve_ids.append(row['cve'].lower())
            # print(row['edb_date'])
            exploit_dates.append(toDate(row['edb_date']))

    return cve_ids, exploit_dates

def edb_zdi_samples_processor():
    file_path = "../Database Files/edb_zdi_samples.csv"
    data = pd.read_csv(file_path)
    cve_ids = []
    exploit_dates = []
    # Need a source column?
    # source = []
    print("edb_zdi_samples_processor")
    for index, row in data.iterrows():
        if not pd.isna(row['edb_date']):
            cve_ids.append(row['cve'].lower())
            # print(row['edb_date'])
            exploit_dates.append(toDate(row['edb_date']))

    return cve_ids, exploit_dates

def symantec_rapid7_processor():
    file_path = "../Database Files/symantec_rapid7.csv"
    data = pd.read_csv(file_path)
    cve_ids = []
    exploit_dates = []
    # Need a source column?
    # source = []
    print("symantec_rapid7_processor")
    for index, row in data.iterrows():
        if not pd.isna(row['Disclosed Date']):
            cve_ids.append(row['CVE'].lower())
            # print(row['Disclosed Date'])
            exploit_dates.append(toDate(row['Disclosed Date']))

    return cve_ids, exploit_dates

def symantec_rapid7_2015to2017_processor():
    file_path = "../Database Files/symantec_rapid7_2015to2017.csv"
    data = pd.read_csv(file_path)
    cve_ids = []
    exploit_dates = []
    # Need a source column?
    # source = []
    print("symantec_rapid7_2015to2017_processor")
    for index, row in data.iterrows():
        if not pd.isna(row['Disclosed Date']):
            cve_ids.append(row['CVE'].lower())
            # print(row['Disclosed Date'])
            exploit_dates.append(toDate(row['Disclosed Date']))

    return cve_ids, exploit_dates

def symantecvulns_processor():
    file_path = "../Database Files/symantecvulns.csv"
    data = pd.read_csv(file_path)
    cve_ids = []
    exploit_dates = []
    # Need a source column?
    # source = []
    print("symantecvulns_processor")
    for index, row in data.iterrows():
        if not pd.isna(row['date']):
            cve_ids.append(row['cve'].lower())
            # print(row['date'])
            exploit_dates.append(toDate2(row['date']))

    return cve_ids, exploit_dates

def cve_0day_refs_data_processor():
    f = open('cve_0day_refs_data.json')
    data = json.load(f)

    cve_ids = []
    patch_dates = []

    for entry in data:
        # print(entry['cve-id'])
        cve_ids.append(entry['cve-id'].lower())
        # print(entry['refs'])
        # Patch date = earliest patch date
        if len(entry['refs']) == 1:
            patch_dates.append(toDate(entry['refs'][0][1].split()[0]))
            # print(toDate(entry['refs'][0][1].split()[0]))
        else:
            early_date = datetime.datetime(9999, 12, 30)
            for ref in entry['refs']:
                if toDate(ref[1].split()[0]) < early_date:
                    early_date = toDate(ref[1].split()[0])
            patch_dates.append(early_date)
            # print(early_date)
    return cve_ids, patch_dates


# Get all the data from different files
cve_list1, exploit_date_list1 = edb_zdi_processor()
cve_list2, exploit_date_list2 = edb_zdi_samples_processor()
cve_list3, exploit_date_list3 = symantec_rapid7_processor()
cve_list4, exploit_date_list4 = symantec_rapid7_2015to2017_processor()
cve_list5, exploit_date_list5 = symantec_rapid7_2015to2017_processor()
cve_list6, exploit_date_list6 = symantecvulns_processor()

# Put them in a list
cve_lists = [cve_list1, cve_list2, cve_list3, cve_list4, cve_list5, cve_list6]
exploit_lists = [exploit_date_list1, exploit_date_list2, exploit_date_list3, exploit_date_list4, exploit_date_list5, exploit_date_list6]

# Combine them as one list
gt_cve_list = []
gt_exploit_list = []
for cve, exploit in zip(cve_lists, exploit_lists):
    gt_cve_list.extend(cve)
    gt_exploit_list.extend(exploit)

# Initialize lists
full_cve_list, full_patch_list = cve_0day_refs_data_processor()
full_exploit_list = [""]*len(full_cve_list)
full_0_day_list = [False]*len(full_cve_list)

# Update the exploit dates with matching cve-ids
for gt_cve, gt_exploit in zip(gt_cve_list, gt_exploit_list):
    for index, cve in enumerate(full_cve_list):
        if gt_cve == cve:
            if full_exploit_list[index] == "":
                full_exploit_list[index] = gt_exploit
            elif full_exploit_list[index] > gt_exploit:
                full_exploit_list[index] = gt_exploit

# Mark ones that have earlier exploit dates than patch dates as 0-day exploits
for index, cve in enumerate(full_cve_list):
    if not full_exploit_list[index] == "":
        if full_exploit_list[index] <= full_patch_list[index]:
            full_0_day_list[index] = True
        else:
            full_0_day_list[index] = False
    else:
        full_0_day_list[index] = False

# Turn the extrated data into pandas
zero_day_exploits_data = pd.DataFrame({
    "CVE-ID": full_cve_list,
    "Patch Date": full_patch_list,
    "Exploit Date": full_exploit_list,
    "Zero Day Exploit": full_0_day_list
})

# Write to a file
zero_day_exploits_data.to_csv("zero_day_exploits.csv", index=False)

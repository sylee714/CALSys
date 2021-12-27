import csv
import datetime

filename1 = "EDB_and_ZDI_dates.csv"

# ex. {"cve id: [edb date, symantec date]"}
cve_symantec_list = {}
cve_rapid7_list = {}

with open(filename1, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    next(csvreader) # skip field row

    for row in csvreader:
        if row[2] != '':
            cve_symantec_list[row[0]] = [row[2], ""]
            cve_rapid7_list[row[0]] = [row[2], ""]

filename2 = "symantec_rapid7_details_posted.csv"

with open(filename2, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    next(csvreader) # skip field row

    for row in csvreader:
        cve_id = row[0].lower()
        if row[1] == "Symantec": # Symantec
            if cve_id in cve_symantec_list and row[2] != "Not found":
                dates = cve_symantec_list[cve_id]  # get the edb and symantec dates;
                dates[1] = row[2].split()[0]  # update the symantec date; only get the date
                cve_symantec_list[cve_id] = dates
        else: # Rapid7
            if cve_id in cve_rapid7_list and row[2] != "Not found":
                dates = cve_rapid7_list[cve_id]  # get the edb and symantec dates;
                dates[1] = row[2].split()[0]  # update the symantec date; only get the date
                cve_rapid7_list[cve_id] = dates
        # if((cve_id in cve_symantec_list) and (row[1] == "Symantec") and (row[2] != "Not found")):
        #     dates = cve_symantec_list[cve_id] # get the edb and symantec dates;
        #     dates[1] = row[2].split()[0] # update the symantec date; only get the date
        #     cve_symantec_list[cve_id] = dates

print("Initial: # of cve: %d" % (len(cve_symantec_list)))

cve_symantec_delete_list = []
cve_rapid7_delete_list = []

for cve in cve_symantec_list:
    if cve_symantec_list[cve][1] == "": # add cve id that has no symantec date
        cve_symantec_delete_list.append(cve)

for cve in cve_rapid7_list:
    if cve_rapid7_list[cve][1] == "": # add cve id that has no rapid7 date
        cve_rapid7_delete_list.append(cve)

for cve in cve_symantec_delete_list: # delete ones that have no symantec dates
    del cve_symantec_list[cve]

for cve in cve_rapid7_delete_list: # delete ones that have no rapid7 dates
    del cve_rapid7_list[cve]

# print("After filtering: # of cve: %d" % (len(cve_symantec_list)))


for cve in cve_symantec_list:
    dates = cve_symantec_list[cve]
    edb_date_split = dates[0].split('/')
    symantec_date_split = dates[1].split('/')
    # Convert to datetime obj for calculation
    edb_date = datetime.datetime(int(edb_date_split[2]), int(edb_date_split[0]), int(edb_date_split[1]))
    symantec_date = datetime.datetime(int(symantec_date_split[2]), int(symantec_date_split[0]), int(symantec_date_split[1]))
    dates.append(symantec_date - edb_date) # calculate the date difference
    cve_symantec_list[cve] = dates


for cve in cve_rapid7_list:
    dates = cve_rapid7_list[cve]
    edb_date_split = dates[0].split('/')
    rapid7_date_split = dates[1].split('/')
    # Convert to datetime obj for calculation
    edb_date = datetime.datetime(int(edb_date_split[2]), int(edb_date_split[0]), int(edb_date_split[1]))
    rapid7_date = datetime.datetime(int(rapid7_date_split[2]), int(rapid7_date_split[0]), int(rapid7_date_split[1]))
    dates.append(rapid7_date - edb_date) # calculate the date difference
    cve_rapid7_list[cve] = dates

print("EDB and Symantec")
for cve in cve_symantec_list:
    print(cve + " | " + cve_symantec_list[cve][0] + " | " + cve_symantec_list[cve][1] + " | ", cve_symantec_list[cve][2])

print("--------------------------------------------------------")
print("EDB and Rapid7")
for cve in cve_rapid7_list:
    print(cve + " | " + cve_rapid7_list[cve][0] + " | " + cve_rapid7_list[cve][1] + " | ", cve_rapid7_list[cve][2])


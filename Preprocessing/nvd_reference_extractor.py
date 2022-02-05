import os
from bs4 import BeautifulSoup
import json
import datetime

def extractLink():
    pass

# class CVE:
#     cve_id = ""
#     ref = []

dir_name = "C:/Users/SYL/Desktop/CALSysLab/Code/Files/NVD-html-files/"

# https://www.geeksforgeeks.org/python-convert-list-of-dictionaries-to-json/
# https://www.programiz.com/python-programming/json
# https://www.geeksforgeeks.org/how-to-parse-local-html-file-in-python/
# 1. Go thru each html file
# 2. Use bs4 to extract data we want
# 3. Save the data as a list of dict
#       ex. ["cve-id": "1010-1010", "ref":[[url1, type1, date1], ...]]

data = []
file_names = os.listdir(dir_name)

for filename in os.listdir(dir_name):
    cve_data = {}
    cve_data["cve-id"] = filename
    refs = []
    with open(os.path.join(dir_name, filename), 'r') as f:
        # file = open("C:/Users/SYL/Desktop/CALSysLab/Code/Files/NVD-html-files/2015-0012.html", "r")
        # soup = BeautifulSoup(file, 'html.parser')
        soup = BeautifulSoup(f, 'lxml')

        # Reference Section
        ref_div = soup.find("div", {"id": "vulnHyperlinksPanel"})
        ref_table = ref_div.find("table")
        ref_table_body = ref_table.find("tbody")
        ref_table_body_rows = ref_table_body.find_all("tr")

        # This gets each ref's hyperlink and its types
        for i, row in enumerate(ref_table_body_rows):
            tds = row.find_all("td")
            ref = []
            for j, td in enumerate(tds):
                # 1st Col has the hyperlink 
                if j == 0:
                    tag_a = td.find("a")
                    # print(str(tag_a['href']))
                    ref.append(str(tag_a['href']))
                else:
                    types = []
                    spans = td.find_all("span")
                    for k, span in enumerate(spans):
                        # Even though spans are nested, it gets all.
                        # Just get if the index is not even
                        if k%2 != 0:
                            # print(span.string)
                            types.append(span.string)
                    ref.append(types)
            ref.append("")
            refs.append(ref)

        # Change History Section
        history_div = soup.find("div", {"id": "vulnChangeHistoryDiv"})
        divs = history_div.find_all("div", {"class": "vuln-change-history-container"})

        # Need to get the header to get the date and time
        for index, div in enumerate(divs):
            date_id = "vuln-change-history-date-" + str(index)
            action_id = "vuln-change-history-" + str(index) + "-action"
            type_id = "vuln-change-history-" + str(index) + "-type"
            old_val_id = "vuln-change-history-" + str(index) + "-old"
            new_val_id = "vuln-change-history-" + str(index) + "-new"

            date = div.find("span", {"data-testid": date_id})
            actions = div.find_all("td", {"data-testid": action_id})
            types = div.find_all("td", {"data-testid": type_id})
            old_vals = div.find_all("td", {"data-testid": old_val_id})
            new_vals = div.find_all("td", {"data-testid": new_val_id})

            for i in range(len(actions)):
                action_val = actions[i].string    
                type_val = types[i].string
                old_val = old_vals[i].find("pre")
                new_val = new_vals[i].find("pre")

                # We want only when a reference is added
                # https://www.educative.io/edpresso/how-to-convert-a-string-to-a-date-in-python
                if ("Added" in action_val or "Changed" in action_val) and "Reference" in type_val:
                    # 1st element is the hyperlink
                    ref_link = new_val.string.split()[0]
                    for ref in refs:
                        if ref_link in ref[0]:
                            month, day, year = date.string.split()[0].split('/')
                            # Check the date and update
                            # date_obj = datetime.strptime(date.string.split()[0], "%d/%m/%Y %H:%M:%S")
                            date_obj = datetime.datetime(int(year), int(month), int(day))
                            if ref[2] == "":
                                ref[2] = date_obj
                            else:
                                if ref[2] > date_obj:
                                    ref[2] = date_obj
    cve_data["refs"] = refs
    data.append(cve_data)
    print(cve_data)

final_data = json.dumps(data, indent=4, default=str)
with open('cve_refs_data.json', 'w') as outfile:
    outfile.write(final_data)



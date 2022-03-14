import pandas as pd

# new data cols: CVE-ID, MITRE Assign Date, Patch Date, Exploit Date,
#                   CVE Description, ZDI Description, Severity Score,
#                   Zero Day Exploit
# data1 = zero-day data
# data1 cols: CVE-ID, Patch Date, Exploit Date, Zero Day Exploit,
#               MITRE Assign Date, CVE Description, Label
# data2 = zdi sample data
# data2 cols: CVE-ID, ZDI Published Date, Severity Score, Description
def find_matchings(data1, data2, file_name):
    cve_ids = []
    mitre_dates = []
    patch_dates = []
    exploit_dates = []
    zdi_dates = []
    cve_descriptions = []
    zdi_descriptions = []
    sev_scores = []
    in_zdi = []
    zero_day_exploit = []

    no_match = False
    for index1, row1 in data1.iterrows():
        for index2, row2 in data2.iterrows():
            if row2['CVE-ID'].lower() == row1['CVE-ID']:
                no_match = False
                cve_ids.append(row1['CVE-ID'])
                mitre_dates.append(row1['MITRE Assign Date'])
                patch_dates.append(row1["Patch Date"])
                exploit_dates.append(row1["Exploit Date"])
                zdi_dates.append(row2["ZDI Published Date"])
                cve_descriptions.append(row1["CVE Description"])
                zdi_descriptions.append(row2["Description"])
                sev_scores.append(row2["Severity Score"])
                in_zdi.append("TRUE")
                zero_day_exploit.append(row1["Zero Day Exploit"])
                break # break as soon as a match is found
            else:
                no_match = True

        # When no zero day sample is found in the ZDI samples
        if no_match:
            cve_ids.append(row1['CVE-ID'])
            mitre_dates.append(row1['MITRE Assign Date'])
            patch_dates.append(row1["Patch Date"])
            exploit_dates.append(row1["Exploit Date"])
            zdi_dates.append("")
            cve_descriptions.append(row1["CVE Description"])
            zdi_descriptions.append("")
            sev_scores.append("0")
            in_zdi.append("FALSE")
            zero_day_exploit.append(row1["Zero Day Exploit"])

    # Turn the extracted data into pandas
    mitre_zdi_data = pd.DataFrame({
        "CVE-ID": cve_ids,
        "MITRE Assign Date": mitre_dates,
        "Patch Date": patch_dates,
        "Exploit Date": exploit_dates,
        "ZDI Published Date": zdi_dates,
        "CVE Description": cve_descriptions,
        "ZDI Description": zdi_descriptions,
        "Severity Score": sev_scores,
        "In ZDI": in_zdi,
        "Zero Day Exploit": zero_day_exploit
    })

    # Write to a file
    mitre_zdi_data.to_csv(file_name, index=False)
    print("Done with ", file_name)


cleaned_zdi_samples = pd.read_csv("../Files/cleaned_zdi_sample.csv")
positive_cases = pd.read_csv('../Files/selected_zero_day_positive_cases_with_zdi.csv')
selected_negative_cases = pd.read_csv('../Files/selected_zero_day_negative_cases_with_zdi.csv')
remaining_negative_cases = pd.read_csv('../Files/remaining_zero_day_negative_cases_with_zdi.csv')

find_matchings(positive_cases, cleaned_zdi_samples, "selected_zero_day_positive_cases_with_zdi.csv")
find_matchings(selected_negative_cases, cleaned_zdi_samples, "selected_zero_day_negative_cases_with_zdi.csv")
find_matchings(remaining_negative_cases, cleaned_zdi_samples, "remaining_zero_day_negative_cases_with_zdi.csv")

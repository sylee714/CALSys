import pandas as pd

# # Read negative and positive cases
# data = pd.read_csv("../Files/negative_cases.csv")
# positive_cases = pd.read_csv("../Files/positive_cases.csv")

# # Combine them
# data.append(positive_cases)
data = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/new_filtered_data.csv")

zdi_samples = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/zdi_samples.csv")

positive_zdi_samples = []
negative_zdi_samples = []

cve_ids = []
mitre_dates = []
cve_descriptions = []
og_labels = []
new_labels = []
zdi_dates = []
zdi_descriptions = []
severity_scores = []

no_match = False

for index1, row1 in data.iterrows():
    print(str(index1) + ": " + row1['CVE-ID'] + " | " + row1['OG Label'])
    for index2, row2 in zdi_samples.iterrows():
        if row2['CVE-ID'].lower() == row1['CVE-ID']:
            no_match = False
            cve_ids.append(row1['CVE-ID'])
            mitre_dates.append(row1['MITRE Assign Date'])
            cve_descriptions.append(row1['CVE Description'])
            og_labels.append(row1['OG Label'])
            new_labels.append(row1['New Label'])
            zdi_dates.append(row2['ZDI Published Date'])
            zdi_descriptions.append(row2['Description'])
            severity_scores.append(row2['Severity Score'])
            break
        else:
            no_match = True
    if no_match:
        cve_ids.append(row1['CVE-ID'])
        mitre_dates.append(row1['MITRE Assign Date'])
        cve_descriptions.append(row1['CVE Description'])
        og_labels.append(row1['OG Label'])
        new_labels.append(row1['New Label'])
        zdi_dates.append("N/A")
        zdi_descriptions.append("")
        severity_scores.append("0")



# print(len(positive_zdi_samples))
# print(len(negative_zdi_samples))

# Turn the extrated data into pandas
mitre_zdi_data = pd.DataFrame({
    "CVE-ID": cve_ids,
    "MITRE Assign Date": mitre_dates,
    "ZDI Published Date": zdi_dates,
    "Severity Score": severity_scores,
    "CVE Description": cve_descriptions,
    "ZDI Description": zdi_descriptions,
    "OG Label": og_labels,
    "New Label": new_labels
})

# Write to a file
mitre_zdi_data.to_csv("filtered_mitre_zdi_data.csv", index=False)

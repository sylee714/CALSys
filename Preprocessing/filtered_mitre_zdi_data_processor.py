import pandas as pd

# data = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/filtered_mitre_zdi_data.csv")
#
# in_zdi = []
# number_of_matched_samples = 0
#
# for index, row in data.iterrows():
#     if pd.isna(row['ZDI Published Date']):
#         in_zdi.append('f')
#     else:
#         print(str(row['CVE-ID']) + " | " + str(row['ZDI Published Date']) + " | " + str(row['Severity Score']))
#         in_zdi.append('t')
#         number_of_matched_samples += 1
#
# data['In ZDI'] = in_zdi
#
# print(number_of_matched_samples)
#
# data.fillna('', inplace=True)
#
# data.to_csv("filtered_mitre_zdi_data_with_binary.csv", index=False)

data = pd.read_csv('filtered_mitre_zdi_data_with_binary.csv')
print(data.head)



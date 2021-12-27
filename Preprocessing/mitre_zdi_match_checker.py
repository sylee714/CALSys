import pandas as pd

negative_cases = pd.read_csv('../Files/remaining_negative_cases_with_zdi.csv')
selected_negative_cases = pd.read_csv('../Files/selected_negative_cases_with_zdi.csv')
negative_cases.append(selected_negative_cases)
positive_cases = pd.read_csv('../Files/selected_positive_cases_with_zdi.csv')

negative_cases_with_zdi = negative_cases.loc[negative_cases["In ZDI"] == 't']
positive_cases_with_zdi = positive_cases.loc[positive_cases["In ZDI"] == 't']

avg_severity_score = 0
for index, row in negative_cases_with_zdi.iterrows():
    if row['In ZDI'] == 't':
        print("Severity Score: ", row['Severity Score'])
        avg_severity_score += float(row['Severity Score'])
print("Avergae Severity Score: ", avg_severity_score/negative_cases_with_zdi.shape[0])
print("# of Negative Cases with ZDI: ", negative_cases_with_zdi.shape[0])
print("# of Negative Cases: ", negative_cases.shape[0])
print("Ratio: ", negative_cases_with_zdi.shape[0]/negative_cases.shape[0])
print("---------------------------------------------------------------")

avg_severity_score = 0
for index, row in positive_cases_with_zdi.iterrows():
    if row['In ZDI'] == 't':
        print("Severity Score: ", row['Severity Score'])
        avg_severity_score += float(row['Severity Score'])
print("Avergae Severity Score: ", avg_severity_score/positive_cases_with_zdi.shape[0])
print("# of Positive Cases with ZDI: ", positive_cases_with_zdi.shape[0])
print("# of Positive Cases: ", positive_cases.shape[0])
print("Ratio: ", positive_cases_with_zdi.shape[0]/positive_cases.shape[0])
print("---------------------------------------------------------------")
import json
import os
import pandas as pd

# Zero Day Exploit Files
zero_day_file1 = pd.read_csv("../Files/selected_zero_day_negative_cases_with_zdi.csv")
zero_day_file2 = pd.read_csv("../Files/selected_zero_day_positive_cases_with_zdi.csv")
zero_day_file3 = pd.read_csv("../Files/remaining_zero_day_negative_cases_with_zdi.csv")

zero_day_files = [zero_day_file1, zero_day_file2, zero_day_file3]

for zero_day_file in zero_day_files:
    zero_day_file['cvss_accessVector'] = 'None'
    zero_day_file['cvss_accessComplexity'] = 'None'
    zero_day_file['cvss_authentication'] = 'None'
    zero_day_file['cvss_confidentialityImpact'] = 'None'
    zero_day_file['cvss_integrityImpact'] = 'None'
    zero_day_file['cvss_availabilityImpact'] = 'None'
    zero_day_file['cvss_baseScore'] = 0
    zero_day_file['cvss_severity'] = 'None'
    zero_day_file['cvss_exploitabilityScore'] = 0
    zero_day_file['cvss_impactScore'] = 0
    zero_day_file['cvss_obtainAllPrivilege'] = 'f'
    zero_day_file['cvss_obtainUserPrivilege'] = 'f'
    zero_day_file['cvss_obtainOtherPrivilege'] = 'f'
    zero_day_file['cvss_userInteractionRequired'] = 'f'

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

        cvss_accessVector = ""
        cvss_accessComplexity = ""
        cvss_authentication = ""
        cvss_confidentialityImpact = ""
        cvss_integrityImpact = ""
        cvss_availabilityImpact = ""
        cvss_baseScore = 0
        cvss_severity = ""
        cvss_exploitabilityScore = 0
        cvss_impactScore = 0
        cvss_obtainAllPrivilege = ""
        cvss_obtainUserPrivilege = ""
        cvss_obtainOtherPrivilege = ""
        cvss_userInteractionRequired = 'FALSE'

        try:
            cvss_accessVector = xdf[i]['impact']['baseMetricV2']['cvssV2']['accessVector']
            cvss_accessComplexity = xdf[i]['impact']['baseMetricV2']['cvssV2']['accessComplexity']
            cvss_authentication = xdf[i]['impact']['baseMetricV2']['cvssV2']['authentication']
            cvss_confidentialityImpact = xdf[i]['impact']['baseMetricV2']['cvssV2']['confidentialityImpact']
            cvss_integrityImpact = xdf[i]['impact']['baseMetricV2']['cvssV2']['integrityImpact']
            cvss_availabilityImpact = xdf[i]['impact']['baseMetricV2']['cvssV2']['availabilityImpact']
            cvss_baseScore = xdf[i]['impact']['baseMetricV2']['cvssV2']['baseScore']

            cvss_severity = xdf[i]['impact']['baseMetricV2']['severity']
            cvss_exploitabilityScore = xdf[i]['impact']['baseMetricV2']['exploitabilityScore']
            cvss_impactScore = xdf[i]['impact']['baseMetricV2']['impactScore']
            cvss_obtainAllPrivilege = xdf[i]['impact']['baseMetricV2']['obtainAllPrivilege']
            cvss_obtainUserPrivilege = xdf[i]['impact']['baseMetricV2']['obtainUserPrivilege']
            cvss_obtainOtherPrivilege = xdf[i]['impact']['baseMetricV2']['obtainOtherPrivilege']
            cvss_userInteractionRequired = xdf[i]['impact']['baseMetricV2']['userInteractionRequired']
        except KeyError:
            pass

        for zero_day_file in zero_day_files:
            zero_day_file.loc[zero_day_file['CVE-ID'] == cve_id,
                              ['cvss_accessVector', 'cvss_accessComplexity', 'cvss_authentication', 'cvss_confidentialityImpact',
                               'cvss_integrityImpact', 'cvss_availabilityImpact', 'cvss_baseScore', 'cvss_severity',
                               'cvss_exploitabilityScore', 'cvss_impactScore', 'cvss_obtainAllPrivilege', 'cvss_obtainUserPrivilege',
                               'cvss_obtainOtherPrivilege', 'cvss_userInteractionRequired']] = \
                                [cvss_accessVector, cvss_accessComplexity, cvss_authentication, cvss_confidentialityImpact,
                                 cvss_integrityImpact, cvss_availabilityImpact, cvss_baseScore, cvss_severity, cvss_exploitabilityScore,
                                 cvss_impactScore, cvss_obtainAllPrivilege, cvss_obtainUserPrivilege, cvss_obtainOtherPrivilege,
                                 cvss_userInteractionRequired]
        print(cve_id)

zero_day_file1.to_csv('selected_zero_day_negative_cases_with_zdi.csv', index=False)
zero_day_file2.to_csv('selected_zero_day_positive_cases_with_zdi.csv', index=False)
zero_day_file3.to_csv('remaining_zero_day_negative_cases_with_zdi.csv', index=False)
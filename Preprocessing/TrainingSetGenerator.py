import csv
import pandas as pd
import numpy as np
import spacy

# Keep track of used negative cases so that we don't re-use the same one
already_used_negative_cases = {}
nlp = spacy.load("en_core_web_lg")

# Method that finds a negative case with the lowest text description similarity
def get_lowest_similarity(positive_case_sample, negative_case_list):
    # Put the positive case's text description into nlp
    positive_case_text = nlp(positive_case_sample["CVE Description"])

    # Go thru every negative case and put its text description into nlp
    negative_case_text_list = []
    for sample in negative_case_list:
        negative_case_text_list.append(nlp(sample[4]))

    # Find the similarity between each negative case and the positive case
    similarity_list = []
    for sample in negative_case_text_list:
        similarity_list.append(positive_case_text.similarity(sample))

    # Find the index of the negative case with the lowest similarity
    min_pos = similarity_list.index(min(similarity_list))
    print(positive_case_sample["CVE-ID"] + ": " + str(negative_case_list[min_pos][0]))

    # Return the lowest one
    return negative_case_list[min_pos]


# Finds a negative case with a similar date as the positive case, but not so similar
# description
def find_negative_case(positive_case_sample, negative_case_list):
    positive_assign_date = positive_case_sample["MITRE Assign Date"]

    # print(type(positive_assign_date))

    filtered_negative_cases = negative_case_list.loc[positive_assign_date == negative_case_list["MITRE Assign Date"]]

    # if there is no negative cases with the same date
    # allow some a margin of 1 day diff
    min_date = positive_assign_date - pd.DateOffset(days=3)
    max_date = positive_assign_date + pd.DateOffset(days=3)
    if filtered_negative_cases.shape[0] == 0:
        filtered_negative_cases = negative_case_list.loc[
            (min_date <= negative_case_list["MITRE Assign Date"]) & (negative_case_list["MITRE Assign Date"] <= max_date)]

    # Get the cve-id of a negative case with the lowest similarity
    lowest_similartiy_negative_case = get_lowest_similarity(positive_case_sample, filtered_negative_cases.values.tolist())

    # Remove the selected negative case from the master list of negative cases
    # This is to avoid duplications
    negative_case_list.drop(index=negative_case_list[negative_case_list["CVE-ID"] == lowest_similartiy_negative_case[0]].index, inplace=True)

    return lowest_similartiy_negative_case


data = pd.read_csv("../Files/preprocessed_filtered_mitre_zdi_data.csv")

data['MITRE Assign Date'] = pd.to_datetime(data["MITRE Assign Date"])

# positive_cases = sorted_data.loc[sorted_data["Label"] == 't'
positive_cases = data.loc[data["New Label"] == 't']
negative_cases = data.loc[data["New Label"] == 'f']

print(positive_cases.shape)
print(negative_cases.shape)

selected_negative_cases = []

print("Finding matching negative cases")
for index, positive_case in positive_cases.iterrows():
    selected_negative_cases.append(find_negative_case(positive_case, negative_cases))

# Add the filtered negative cases to get the full list
# Print the number of rows to check if they have the same number of rows
print("Length of Positive Cases: ", positive_cases.shape[0])
print("Length of Selected Negative Cases: ", len(selected_negative_cases))
print("Length of Remaining Negative Cases: ", negative_cases.shape[0])

# Export the selected negative cases as a csv file
selected_negative_cases_df = pd.DataFrame(selected_negative_cases, columns=['CVE-ID', 'MITRE Assign Date', 'ZDI Published Date',
                                                                            'Severity Score', 'CVE Description', 'ZDI Description',
                                                                            'OG Label', 'New Label', 'In ZDI'])
selected_negative_cases_df.to_csv("selected_negative_cases_with_zdi.csv", index=False)
negative_cases.to_csv("remaining_negative_cases_with_zdi.csv", index=False)
positive_cases.to_csv("selected_positive_cases_with_zdi.csv", index=False)


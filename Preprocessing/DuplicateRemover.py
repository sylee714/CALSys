import csv
import pandas as pd
import numpy as np
import spacy

# Finds other cve-ids that have cosine similarity < 1 and >= .92
def find_duplicates(text_descriptions, current_cve):
    current_text_description = nlp(current_cve['CVE Description'])

    similarity_list = []

    for text_description in text_descriptions:
        if 1 > text_description.similarity(current_text_description) >= .92:
            similarity_list.append(text_description)

    return similarity_list


# Load the data and combine them
positive_cases = pd.read_csv("../Files/sorted_positive_cases.csv")
negative_cases = pd.read_csv("../Files/sorted_negative_cases.csv")
data = positive_cases.append(negative_cases, ignore_index=True)

print("Before removing similar ones: ", data.shape)

# Create nlp
nlp = spacy.load("en_core_web_lg")

# Put text descriptions into nlp
text_descriptions = []

# Convert every text description as a nlp token
for text_description in data["CVE Description"].values.tolist():
    text_descriptions.append(nlp(text_description))

# Go thru eac cve-id
for index, cve in data.iterrows():
    # Find the duplicates
    duplicates = find_duplicates(text_descriptions, cve)
    # Go thru each duplicate and remove it from the data
    for duplicate in duplicates:
        data.drop(data[data["CVE Description"] == str(duplicate)].index, inplace=True)
    print("After removing similar ones: ", data.shape)


print("Final removing similar ones: ", data.shape)
data.to_csv("filtered_data.csv", index=False)

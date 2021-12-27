import csv
import pandas as pd
import numpy as np
import re
import nltk
from nltk.util import bigrams, trigrams, ngrams
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
import sklearn
import os
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from operator import itemgetter

# This script reads the initial positive and negative case files.
# It combines them into one list.
# It preprocesses the text description, removing stop-words and punctuations
# and applying stemming. Then, it sorts the data by the 'MITRE Assign Date' in
# ascending order.
# Then, it separates into two separate csv files: positive and negative

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# nltk.download('stopwords')
# nltk.download('punkt')

# -----------------------------------------------
# Global variables
# Get English stop words
stop_words = set(stopwords.words('english'))

# Get punctuations
punctuation = list(string.punctuation)

# Add extra ones that are not included in the provided one
punctuation.append('“')
punctuation.append('”')
punctuation.append('’')
punctuation.append('‘')
punctuation.append('...')

# Stemmer
ps = PorterStemmer()
# -----------------------------------------------

# -----------------------------------------------
# Methods

# Method to clean text by removing stop words and punctuations and stemming
def clean_text(text):
    tokens = nltk.word_tokenize(text)
    text_no_stop_words_punct = [ps.stem(t) for t in tokens if t not in stop_words and t not in punctuation]
    text_no_stop_words_punct = " ".join(text_no_stop_words_punct)
    return text_no_stop_words_punct
# -----------------------------------------------

# -----------------------------------------------
# Main Call
# Read csv files
data = pd.read_csv("C:/Users/SYL/Desktop/CALSysLab/Code/Files/filtered_mitre_zdi_data_with_binary.csv")
# temp_positives = pd.read_csv("../Files/positive_cases.csv")

# Fill 'na' texts with empty strings
data.fillna('', inplace=True)

# Combine them
# data.append(temp_positives)

print("Printing first 5")
print(data.head())
print("-------------------------------------------")

# Find the number of positive cases
num_real_positive = 0
for sample in data['New Label']:
    if sample == 't':
        num_real_positive = num_real_positive + 1

print("Total # of samples: " + str(len(data)))
print("Total # of negative samples: " + str(len(data) - num_real_positive))
print("Total # of positive samples: " + str(num_real_positive))
print("# of Positive/Total: " + str(num_real_positive / len(data) * 100))
print("-------------------------------------------")

# Preprocess the cve text descriptions
initial_zdi_descriptions = data["ZDI Description"]
cleaned_zdi_descriptions = []

print("Before Preprocessing")
for i in range(5):
    print(initial_zdi_descriptions[i])
print("-------------------------------------------")

for sent in initial_zdi_descriptions:
    cleaned_zdi_descriptions.append(clean_text(sent))

print("After Preprocessing")
for i in range(5):
    print(cleaned_zdi_descriptions[i])
print("-------------------------------------------")

data["ZDI Description"] = cleaned_zdi_descriptions

# print("Printing first 5")
# print(data.head())
# print("-------------------------------------------")

# print("Sorted by date")
# data['MITRE Assign Date'] = pd.to_datetime(data["MITRE Assign Date"])
# sorted_data = data.sort_values(by=['MITRE Assign Date'])
# print(data.columns)
# print("-------------------------------------------")

# positive_cases = sorted_data.loc[sorted_data["Label"] == 't']

# positive_cases_dates = positive_cases['MITRE Assign Date']
# print("Positive Cases")
# print("Max Date: ", positive_cases_dates.max())
# print("Min Date: ", positive_cases_dates.min())
# print("-------------------------------------------")

# negative_cases = sorted_data.loc[sorted_data["Label"] == 'f']

# negative_cases_dates = negative_cases['MITRE Assign Date']
# print("Positive Cases")
# print("Max Date: ", negative_cases_dates.max())
# print("Min Date: ", negative_cases_dates.min())
# print("-------------------------------------------")

# print(len(sorted_data))
# print(len(positive_cases))
# print(positive_cases.head())
# print(len(negative_cases))

# positive_cases.to_csv("sorted_positive_cases.csv", index=False)
# negative_cases.to_csv("sorted_negative_cases.csv", index=False)
data.to_csv("preprocessed_filtered_mitre_zdi_data.csv", index=False)



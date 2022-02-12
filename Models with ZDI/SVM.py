from sklearn.pipeline import Pipeline, make_pipeline
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn import svm
from sklearn import metrics

# Columns to drop
drop_cols = ['CVE-ID', 'ZDI Published Date', 'OG Label', 'ZDI Description']

# Read the files
positive_cases = pd.read_csv('../Files/selected_positive_cases_with_zdi_sample.csv')
selected_negative_cases = pd.read_csv('../Files/selected_negative_cases_with_zdi_sample.csv')
remaining_negative_cases = pd.read_csv('../Files/remaining_negative_cases_with_zdi_sample.csv')

# Drop columns that are not needed
for col in drop_cols:
    positive_cases = positive_cases.drop(col, axis=1)
    selected_negative_cases = selected_negative_cases.drop(col, axis=1)
    remaining_negative_cases = remaining_negative_cases.drop(col, axis=1)

# Replace 'NaN'
positive_cases.fillna('', inplace=True)
selected_negative_cases.fillna('', inplace=True)
remaining_negative_cases.fillna('', inplace=True)

# Convert date to datetime
positive_cases['MITRE Assign Date'] = pd.to_datetime(positive_cases["MITRE Assign Date"])
selected_negative_cases['MITRE Assign Date'] = pd.to_datetime(selected_negative_cases["MITRE Assign Date"])
remaining_negative_cases['MITRE Assign Date'] = pd.to_datetime(remaining_negative_cases["MITRE Assign Date"])

cut_off_date = pd.to_datetime("5/1/2016") # with the filtered data

# ---------------------------------------------------------
# TRAINING SET
# Get the training set from the positive set
training_data = positive_cases.loc[positive_cases['MITRE Assign Date'] < cut_off_date]
# print(training_data.shape)

# Get the training set from the negative set
training_data_2 = selected_negative_cases.loc[selected_negative_cases['MITRE Assign Date'] < cut_off_date]
# training_data_2 = negative_cases.loc[negative_cases['MITRE Assign Date'] < cut_off_date]

# Combine the training sets into one
training_data = training_data.append(training_data_2, ignore_index=True)
# print(training_data.shape)

# ---------------------------------------------------------
# TESTING SET
# Get the testing set from the positive set
testing_data = positive_cases.loc[positive_cases['MITRE Assign Date'] >= cut_off_date]

# Get the testing set from the negative set
testing_data_2 = selected_negative_cases.loc[selected_negative_cases['MITRE Assign Date'] >= cut_off_date]
testing_data_3 = remaining_negative_cases.loc[remaining_negative_cases['MITRE Assign Date'] >= cut_off_date]
testing_data_2 = testing_data_2.append(testing_data_3, ignore_index=True)

# Randomly select negative cases
# The ratio is 1 positive : 9 negative
testing_data_4 = testing_data_2.sample(n=testing_data.shape[0]*9, random_state=42)

# Combine the positive and negative testing data
testing_data = testing_data.append(testing_data_4, ignore_index=True)

# Combine the training and testing data to for the td-idf vectorizers
data = training_data.append(testing_data, ignore_index=True)

Encoder = LabelEncoder()
training_data['New Label'] = Encoder.fit_transform(training_data['New Label'])
testing_data['New Label'] = Encoder.fit_transform(testing_data['New Label'])

training_y = training_data['New Label']
test_y = testing_data['New Label']

# Drop the 'MITRE Assign Date'
training_data = training_data.drop('MITRE Assign Date', axis=1)
testing_data = testing_data.drop('MITRE Assign Date', axis=1)

# Drop the 'New Label' from the dataset, since it's the label we want to guess
training_data = training_data.drop('New Label', axis=1)
testing_data = testing_data.drop('New Label', axis=1)

# Lists to save results
ngrams = []
accuracies = []
precisions = []
recalls = []
f1s = []

features_to_encode = training_data.columns[training_data.dtypes==object].tolist()
col_trans = make_column_transformer((OneHotEncoder(handle_unknown='ignore'), features_to_encode), remainder="passthrough")

# Model
SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto', probability=True)

# Fit th model
pipe = make_pipeline(col_trans, SVM)
pipe.fit(training_data, training_y)

# Predict the labels on validation dataset
predictions = pipe.predict(testing_data)

accuracy = metrics.accuracy_score(test_y.tolist(), predictions)
precision = metrics.precision_score(test_y.tolist(), predictions)
recall = metrics.recall_score(test_y.tolist(), predictions)
f1 = metrics.f1_score(test_y.tolist(), predictions)

print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1: ", f1)
print("----------------------------")

# # Results are too good
# # Need to look into them what is happening
# for i in range(10):
#     # Initialize model and tf-idfs
#     SVM = svm.SVC(C=1.0, kernel='linear', degree=3, gamma='auto', probability=True)
#     cve_description_tfidf = TfidfVectorizer(
#         analyzer='word',
#         max_features=(1000 * (i + 1)),
#         max_df=0.8,
#         min_df=5,
#         stop_words='english'
#     )
#     zdi_description_tfidf = TfidfVectorizer(
#         analyzer='word',
#         max_features=(1000 * (i + 1)),
#         max_df=0.8,
#         min_df=5,
#         stop_words='english'
#     )
#
#     # Construct the column transformer
#     column_transformer = ColumnTransformer(
#         [('cve_description_tfidf', cve_description_tfidf, 'CVE Description'),
#          ('zdi_description_tfidf', zdi_description_tfidf, 'ZDI Description')],
#         remainder='passthrough'
#     )
#
#     # Fit th model
#     pipe = Pipeline(
#         [('tfidf', column_transformer),
#          ('classify', SVM)])
#
#     pipe.fit(training_data, training_y)
#
#     # Predict the labels on validation dataset
#     predictions = pipe.predict(testing_data)
#
#     accuracy = metrics.accuracy_score(test_y.tolist(), predictions)
#     precision = metrics.precision_score(test_y.tolist(), predictions)
#     recall = metrics.recall_score(test_y.tolist(), predictions)
#     f1 = metrics.f1_score(test_y.tolist(), predictions)
#
#     print("1-Gram Result")
#     print("Max Feature: ", 1000 * (i + 1))
#     # print("Max Feature: ", max_feature)
#     print("Accuracy: ", accuracy)
#     print("Precision: ", precision)
#     print("Recall: ", recall)
#     print("F1: ", f1)
#     print("----------------------------")
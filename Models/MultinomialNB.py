import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn import naive_bayes
from sklearn import metrics
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt
import seaborn as sns

# sorted_positive_cases.csv = all the positive cases sorted by date
# selected_nagative_cases.csv = selected negative cases for every positive case
# remaining_negative_cases.csv = remaining negative cases after removing the selected negative cases
# cases that came before 2/1/2016 -> training
# cases that came on/after 2/1/2016 -> testing
# positive:negative ratio in testing: 1:9 or 0.8:9.2

# 1. Remove similar cves
# 2. try different number of features for tf-idf
# 3. try with no 1-1 training method

# Read the csv files
# positive_cases = pd.read_csv('../Files/sorted_positive_cases.csv') # with the not filtered data
positive_cases = pd.read_csv('../Files/selected_positive_cases.csv') # with the filtered data
# positive_cases = pd.read_csv('../Files/sorted_positive_cases.csv') # with the not filtered data
# negative_cases = pd.read_csv('../Files/sorted_negative_cases.csv')
selected_negative_cases = pd.read_csv('../Files/selected_negative_cases.csv')
remaining_negative_cases = pd.read_csv('../Files/remaining_negative_cases.csv')
# selected_negative_cases = pd.read_csv('../Files/old_selected_negative_cases.csv')
# remaining_negative_cases = pd.read_csv('../Files/old_remaining_negative_cases.csv')

# Convert date to datetime
# data['MITRE Assign Date'] = pd.to_datetime(data["MITRE Assign Date"])
positive_cases['MITRE Assign Date'] = pd.to_datetime(positive_cases["MITRE Assign Date"])
# negative_cases['MITRE Assign Date'] = pd.to_datetime(negative_cases["MITRE Assign Date"])
selected_negative_cases['MITRE Assign Date'] = pd.to_datetime(selected_negative_cases["MITRE Assign Date"])
remaining_negative_cases['MITRE Assign Date'] = pd.to_datetime(remaining_negative_cases["MITRE Assign Date"])

# cut_off_date = pd.to_datetime("2/1/2016") # with the not filtered data
cut_off_date = pd.to_datetime("5/1/2016") # with the filtered data
# print(cut_off_date)

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

# # Get the testing set from the negative set
testing_data_2 = selected_negative_cases.loc[selected_negative_cases['MITRE Assign Date'] >= cut_off_date]
testing_data_3 = remaining_negative_cases.loc[remaining_negative_cases['MITRE Assign Date'] >= cut_off_date]
testing_data_2 = testing_data_2.append(testing_data_3, ignore_index=True)

# # Randomly select negative cases
# # The ratio is 1 positive : 9 negative
testing_data_4 = testing_data_2.sample(n=testing_data.shape[0]*9, random_state=42)

# Combine the positive and negative testing data
# testing_data_4 = negative_cases.loc[negative_cases['MITRE Assign Date'] >= cut_off_date]
testing_data = testing_data.append(testing_data_4, ignore_index=True)
# print(testing_data.shape)

data = training_data.append(testing_data, ignore_index=True)
# print(data.shape)

Encoder = LabelEncoder()
training_data['Label'] = Encoder.fit_transform(training_data['Label'])
testing_data['Label'] = Encoder.fit_transform(testing_data['Label'])

training_y = training_data['Label']
test_y = testing_data['Label']

ngrams = []
max_features = []
accuracies = []
precisions = []
recalls = []
f1s = []

max_feature = 500

for i in range(10):
# 1-gram TF-IDF
    tfidf_vector = TfidfVectorizer(
            analyzer='word',
            max_features=(1000*(i+1)),
            # max_features=(max_feature),
            max_df=0.8,
            min_df=5,
            stop_words='english',
            ngram_range=(1,1)
        )

    # Feed the whole text description
    tfidf_vector.fit(data['CVE Description'])

    # Transform training and testing descriptions
    train_x_tfidf = tfidf_vector.transform(training_data['CVE Description'])
    test_x_tfidf = tfidf_vector.transform(testing_data['CVE Description'])

    # Fit the training dataset on the NB classifier
    naive = naive_bayes.MultinomialNB()
    naive.fit(train_x_tfidf, training_data['Label'])

    # Predict the labels on validation dataset
    predictions = naive.predict(test_x_tfidf)
    predicted_prob = naive.predict_proba(test_x_tfidf)

    # Compute the metrics
    accuracy = metrics.accuracy_score(testing_data['Label'].tolist(), predictions)
    precision = metrics.precision_score(testing_data['Label'].tolist(), predictions)
    recall = metrics.recall_score(testing_data['Label'].tolist(), predictions)
    f1 = metrics.f1_score(testing_data['Label'].tolist(), predictions)

    classes = np.unique(testing_data['Label'].to_numpy())
    y_test_array = pd.get_dummies(testing_data['Label'], drop_first=False).values

    print("1-Gram Result")
    print("Max Feature: ", 1000*(i+1))
    # print("Max Feature: ", max_feature)
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1: ", f1)
    print("-------------------------------------------")



# auc = metrics.roc_auc_score(testing_data['Label'], predictions)
# print("Auc:", round(auc,2))
# print("Detail:")
# print(metrics.classification_report(test_y, predictions))
#
# ## Plot confusion matrix
# cm = metrics.confusion_matrix(test_y, predictions)
# fig, ax = plt.subplots()
# sns.heatmap(cm, annot=True, fmt='d', ax=ax, cmap=plt.cm.Blues,
#             cbar=False)
# ax.set(xlabel="Pred", ylabel="True", xticklabels=classes,
#        yticklabels=classes, title="Confusion matrix")
# plt.yticks(rotation=0)
#
# fig, ax = plt.subplots(nrows=1, ncols=2)
# ## Plot roc
# for i in range(len(classes)):
#     fpr, tpr, thresholds = metrics.roc_curve(y_test_array[:,i],
#                            predicted_prob[:,i]) # all the rows in i-th column
#     ax[0].plot(fpr, tpr, lw=3,
#               label='{0} (area={1:0.2f})'.format(classes[i],
#                               metrics.auc(fpr, tpr))
#                )
# ax[0].plot([0,1], [0,1], color='navy', lw=3, linestyle='--')
# ax[0].set(xlim=[-0.05,1.0], ylim=[0.0,1.05],
#           xlabel='False Positive Rate',
#           ylabel="True Positive Rate (Recall)",
#           title="Receiver operating characteristic")
# ax[0].legend(loc="lower right")
# ax[0].grid(True)
#
# ## Plot precision-recall curve
# for i in range(len(classes)):
#     precision, recall, thresholds = metrics.precision_recall_curve(
#                  y_test_array[:,i], predicted_prob[:,i]) # all the rows in i-th column
#     ax[1].plot(recall, precision, lw=3,
#                label='{0} (area={1:0.2f})'.format(classes[i],
#                                   metrics.auc(recall, precision))
#               )
#     # print(thresholds.shape)
# ax[1].set(xlim=[0.0,1.05], ylim=[0.0,1.05], xlabel='Recall',
#           ylabel="Precision", title="Precision-Recall curve")
# ax[1].legend(loc="best")
# ax[1].grid(True)


# plt.show()

#------------------------------------------------------------------------------------

# Multiple Predictors
# max_n_gram = 5
# for i in range(max_n_gram):
#     # Next is feeding the combined data to tf-idf vectorizer
#     # Create a tf-idf vectorizer
#     # Test with different ngram values
#     # Max ngram = 40
#     tfidfvectorizer = TfidfVectorizer(
#         analyzer='word',
#         max_features=1000,
#         # max_df=0.8,
#         # min_df=5,
#         stop_words='english',
#         ngram_range=(i+1,i+1)
#     )
#     # Feed the whole text description
#     tfidfvectorizer.fit(data['CVE Description'])
#
#     # Transform training and testing descriptions
#     train_x_tfidf = tfidfvectorizer.transform(training_data['CVE Description'])
#     test_x_tfidf = tfidfvectorizer.transform(testing_data['CVE Description'])
#
#     # print(tfidfvectorizer.vocabulary_)
#     # print(len(tfidfvectorizer.vocabulary_))
#     # print(train_x_tfidf)
#     # print(test_x_tfidf)
#
#     # fit the training dataset on the NB classifier
#     naive = naive_bayes.MultinomialNB()
#     naive.fit(train_x_tfidf, training_data['Label'])
#
#     # predict the labels on validation dataset
#     predictions = naive.predict(test_x_tfidf)
#     print(len(predictions))
#     print(len(testing_data['Label'].tolist()))
#
#     # print(type(testing_data['Label'].tolist()[0]))
#     # print(type(predictions[0]))
#     print("# of negative: ", testing_data['Label'].tolist().count(0))
#     print("# of positive: ", testing_data['Label'].tolist().count(1))
#
#     print("# of negative: ", predictions.tolist().count(0))
#     print("# of positive: ", predictions.tolist().count(1))
#
#     accuracy = metrics.accuracy_score(testing_data['Label'].tolist(), predictions)
#     precision = metrics.precision_score(testing_data['Label'].tolist(), predictions)
#     recall = metrics.recall_score(testing_data['Label'].tolist(), predictions)
#     f1 = metrics.f1_score(testing_data['Label'].tolist(), predictions)
#     # use accuracy_score function to get the accuracy
#     print("n_gram: ", i+1)
#     print("Accuracy: ", accuracy)
#     print("Precision: ", precision)
#     print("Recall: ", recall)
#     print("F1: ", f1)
#     print("------------------------------------")
#
#     ngrams.append(i+1)
#     accuracies.append(accuracy)
#     precisions.append(precision)
#     recalls.append(recall)
#     f1s.append(f1)
#
# fig, ax = plt.subplots()
#
# ax.set(xlim=[0.0,max_n_gram], ylim=[0.0,1.05],
#           xlabel='N-Grams',
#           ylabel="Metrics",
#           title="Metrics vs N-Grams")
#
# ax.plot(ngrams, accuracies, label = "Accuracy", linestyle='-')
# ax.plot(ngrams, precisions, label = "Precision", linestyle='--')
# ax.plot(ngrams, recalls, label = "Recall", linestyle='-.')
# ax.plot(ngrams, f1s, label = "F1", linestyle=':')
# ax.legend(loc="lower right")
# plt.show()


# ---------------------------------
#
# # font1 = {'family':'serif','color':'blue','size':20}
# # font2 = {'family':'serif','color':'darkred','size':15}
# #
# # plt.title("Metrics vs N-Grams", fontdict = font1)
# # plt.xlabel("N-Grams", fontdict = font2)
# # plt.ylabel("Metrics", fontdict = font2)
#
# # plt.plot(ngrams, accuracies, label = "Accuracy", linestyle='-')
# # plt.plot(ngrams, precisions, label = "Precision", linestyle='--')
# # plt.plot(ngrams, recalls, label = "Recall", linestyle='-.')
# # plt.plot(ngrams, f1s, label = "F1", linestyle=':')
# # plt.legend()
# # plt.show()


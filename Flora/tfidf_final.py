import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
# import re
# import jieba


# from zhon.hanzi import punctuation
# from zhon.hanzi import non_stops
# from zhon.hanzi import stops
# from nltk import word_tokenize
# from nltk.stem import WordNetLemmatizer
# import nltk
# from nltk.corpus import stopwords

# nltk.download()
# stop_words = set(stopwords.words('english'))

def tfidf(data, data2, term, N=100):
    # preproscessing
    # Get the all the rows with the column "term" name
    # Drop all na, get only the unique, and turn them to a list
    d1 = data[term].dropna().unique().tolist()

    # If the list is empty, add a 'na'
    if len(d1) == 0:
        d1.append('na')

    # Do the same
    d2 = data2[term].dropna().unique().tolist()
    if len(d2) == 0:
        d2.append('na')

    # Go thru the list and turn it as one string
    texts = ["".join(t) for t in d1]
    t1 = ["".join(t) for t in d2]
    texts.extend(t1)
    #
    # print(texts)
    # print("---------------------------------------")

    # preproscessing
    # test = pd.Series((''.join(map(str, texts))).lower().split()).value_counts()
    # test = ''.join(map(str, texts)).lower().split()
    # print(test)
    tfIdfVectorizer = TfidfVectorizer(stop_words='english', max_features=N)
    tfidf = tfIdfVectorizer.fit(texts)

    vocab = tfIdfVectorizer.vocabulary_
    print(vocab)
    sorted_vocab = dict(sorted(vocab.items(), key=lambda item: item[1]))
    print(sorted_vocab)

    print(tfIdfVectorizer.idf_)

    print(d1[0])
    vector = tfIdfVectorizer.transform([d1[0]])
    print(vector.toarray())
    # res = {tfIdfVectorizer.get_feature_names()[i]: tfidf.idf_[i] for i in
    #        range(len(tfIdfVectorizer.get_feature_names()))}
    # print(res)
    # print("---------------------------------------")

    # temp = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
    # print(temp)
    # print("---------------------------------------")
    #
    # label = list(temp.keys())
    # print(label)
    # print("---------------------------------------")
    #
    # dict_t = {key: [] for key in label}
    # for index, row in data.iterrows():
    #     current_text = row[term]
    #
    #     if current_text is None:
    #         current_text = 'na'
    #
    #     new_vector = tfidf.transform([str(current_text)]).toarray()
    #     for i in range(len(label)):
    #         dict_t[label[i]].append(new_vector[0][i])
    #
    # df = pd.DataFrame.from_dict(dict_t, orient='columns')
    #
    # for i in dict_t.keys():
    #     data[i] = df[i]
    #     # print(i)
    # # data.to_csv('pos_tfidf_description.csv')
    # print(term, len(data.columns))
    #
    # return data


train = pd.read_csv("training_final.csv")
test = pd.read_csv("testing_final.csv")

terms = ['cve_description', 'reference_tag', 'reference_source', 'cpe_products', 'cpe_vendors',
         'dw_post_content']  # ,'dw_market_item']
# for term in terms:
#     train = tfidf(train, test, term)
#     test = tfidf(test, train, term)

tfidf(train, test, 'cve_description')
# train = tfidf(train, test, 'cve_description')
# test = tfidf(test, train, 'cve_description')
#
# train.to_csv("training.csv")
# test.to_csv("testing.csv")

# trc = train.columns.tolist()
# tec = test.columns.tolist()
# print("train", len(trc))
# print("test", len(tec))

# train.to_csv("c7.csv")
# test.to_csv("c8.csv")

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf():
    pass

data = pd.read_csv("../Files/preprocessed_filtered_mitre_zdi_data.csv")

d1 = data['CVE Description'].dropna().unique().tolist()
d2 = data['ZDI Description'].dropna().unique().tolist()

texts1 = ["".join(t) for t in d1]
texts2 = ["".join(t) for t in d2]

cve_description_tfIdf_vect = TfidfVectorizer(analyzer='word',
                                             max_features=1000,
                                             max_df=0.8,
                                             min_df=5,
                                             stop_words='english')

zdi_description_tfIdf_vect = TfidfVectorizer(analyzer='word',
                                             max_features=1000,
                                             max_df=0.8,
                                             min_df=5,
                                             stop_words='english')

cve_dscription_tfidf = cve_description_tfIdf_vect.fit(texts1)
zdi_dscription_tfidf = zdi_description_tfIdf_vect.fit(texts2)

print(cve_dscription_tfidf.get_feature_names())

# Make a dict = {key:idf}
res = {cve_description_tfIdf_vect.get_feature_names()[i]: cve_dscription_tfidf.idf_[i] for i in
       range(len(cve_description_tfIdf_vect.get_feature_names()))}

# Sort the dict by the idf
# dict.items returns key:value pairs as tuples. {key:value} -> (key,value)
# sorted(iterable, key= to decide the order, reverse=(True=Descending, False=Ascending))
temp = dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
print(temp)

# Get the keys as a list
labels = list(temp.keys())

print(labels)

# For each label, make a list
dict_t = {key:[] for key in labels}

new_vector = cve_dscription_tfidf.transform(["heap-bas buffer overflow __nss_hostname_digits_dot function glibc 2.2 2.x version 2.18 allow context-depend attack execut arbitrari code via vector relat 1 gethostbynam 2 gethostbyname2 function aka `` ghost ''"])
# print(new_vector.toarray())
# print(len(new_vector.toarray()[0]))

# for index, row in data.iterrows():
#     current_text = row['CVE Description']
#     if current_text is None:
#         current_text = 'na'
#     new_vector = cve_dscription_tfidf.transform([str(current_text)]).toarray()
#     for i in range(len(labels)):
#         dict_t[labels[i].append(new_vector[0][i])]



import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# CVE Description TF-IDF = 1000
# ZDI Description TF-IDF = 100
# The size of ZDI TF-IDF  is much smaller, because not many CVEs are in ZDI.
def tfidf_file(file, labels, col_name, tf_idf_vect):
    vocab_keys = {key: [] for key in labels}

    # Go thru each row of a file
    for index, row in file.iterrows():
        # Get the col name
        current_text = row[col_name]

        if current_text is None:
            current_text = 'na'

        # Transform the text and get the result
        new_vector = tf_idf_vect.transform([str(current_text)]).toarray()

        # Add the result to the corresponding key
        for i in range(len(labels)):
            vocab_keys[labels[i]].append(new_vector[0][i])

    df = pd.DataFrame.from_dict(vocab_keys, orient='columns')

    for vocab_key in vocab_keys.keys():
        file[vocab_key] = df[vocab_key]

    # No need to return?
    return file


def tfidf(files, col_name):

    # Get the all the rows with the column "term" name
    # Drop all na, get only the unique, and turn them to a list
    d1 = files[0][col_name].dropna().unique().tolist()
    d2 = files[1][col_name].dropna().unique().tolist()
    d3 = files[2][col_name].dropna().unique().tolist()

    # If the list is empty, add a 'na'
    if len(d1) == 0:
        d1.append('na')

    if len(d2) == 0:
        d2.append('na')

    if len(d3) == 0:
        d3.append('na')

    # Go thru the list and turn it as one string
    texts = ["".join(t) for t in d1]
    t2 = ["".join(t) for t in d2]
    t3 = ["".join(t) for t in d3]
    texts.extend(t2)
    texts.extend(t3)

    max_feature = 1000
    if col_name == "ZDI Description":
        max_feature = 50

    # Create the tf-idf
    tfIdfVectorizer = TfidfVectorizer(
        analyzer='word',
        max_features=max_feature,
        max_df=0.8,
        min_df=5,
        stop_words='english'
    )

    # Fit the corpus
    tfIdfVectorizer.fit(texts)

    # Get the chosen vocabs
    vocab = tfIdfVectorizer.vocabulary_

    # Sort the vocabs by the index
    sorted_vocab = dict(sorted(vocab.items(), key=lambda item: item[1]))

    # Make a list of strings with the keys
    labels = list(sorted_vocab.keys())

    # Initialize a dict; key = vocab and value = [tfidf results]
    # file1_keys = {key: [] for key in labels}
    updated_files = []

    for file in files:
        updated_files.append(tfidf_file(file, labels, col_name, tfIdfVectorizer))

    # No need to return?
    return updated_files


# Read the files
selected_positive = pd.read_csv('../Files/selected_positive_cases_with_zdi.csv')
selected_negative = pd.read_csv('../Files/selected_negative_cases_with_zdi.csv')
remaining_negative = pd.read_csv('../Files/remaining_negative_cases_with_zdi.csv')

file_names = ["selected_positive_cases_with_zdi_sample.csv", "selected_negative_cases_with_zdi_sample.csv",
              "remaining_negative_cases_with_zdi_sample.csv"]

file_list = [selected_positive, selected_negative, remaining_negative]

# Replace 'NaN'
for f in file_list:
    f.fillna('', inplace=True)

col_names = ["CVE Description", "ZDI Description"]

for feature in col_names:
    if feature == "CVE Description":
        tfidf(file_list, feature)

for index, f in enumerate(file_list):
    f.to_csv(file_names[index], index=False)


import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

# Create the encoders
label_encoder = LabelEncoder()
encoder = OneHotEncoder(handle_unknown='ignore')

# Read the files
zero_day_file1 = pd.read_csv("../Files/selected_zero_day_negative_cases_with_zdi.csv")
zero_day_file2 = pd.read_csv("../Files/selected_zero_day_positive_cases_with_zdi.csv")
zero_day_file3 = pd.read_csv("../Files/remaining_zero_day_negative_cases_with_zdi.csv")

print("Zero Day File1 Shape: ", zero_day_file1.shape)
print("Zero Day File2 Shape: ", zero_day_file2.shape)
print("Zero Day File3 Shape: ", zero_day_file3.shape)

# Only the training set
train_frames = [zero_day_file1, zero_day_file2]
train_df = pd.concat(train_frames)

# Training and Testing Set
frames = [zero_day_file1, zero_day_file2, zero_day_file3]
combined_df = pd.concat(frames)

# Fit and transform on the whole data for the label encoding
label_encoder.fit(combined_df['CWE ID'])
train_df['CWE ID'] = label_encoder.transform(train_df['CWE ID'])
combined_df['CWE ID'] = label_encoder.transform(combined_df['CWE ID'])

# Only fit on the train data for one-hot encoding
encoder.fit(train_df[['CWE ID']])

# One-hot encoding transform on the whole data set
encoder_df = pd.DataFrame(encoder.transform(combined_df[['CWE ID']]).toarray())

# Need to reset the index before doing 'concat' or 'join' to avoid weird mix of indices
combined_df.reset_index(drop=True, inplace=True)
encoder_df.reset_index(drop=True, inplace=True)

# Combined the original and the encoded df
encoded_df = combined_df.join(encoder_df)

# Split the data
selected_negative_cases = encoded_df.iloc[:149, :]
selected_positive_cases = encoded_df.iloc[149:298, :]
remain_negative_cases = encoded_df.iloc[299:, :]

# Export as csv files
selected_negative_cases.to_csv('selected_zero_day_negative_cases_with_zdi.csv', index=False)
selected_positive_cases.to_csv('selected_zero_day_positive_cases_with_zdi.csv', index=False)
remain_negative_cases.to_csv('remaining_zero_day_negative_cases_with_zdi.csv', index=False)
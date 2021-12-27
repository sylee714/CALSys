import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn import naive_bayes
from sklearn import metrics
import matplotlib.pyplot as plt
import gensim
import gensim.downloader as gensim_api

# Useful tutorial
# https://towardsdatascience.com/text-classification-with-nlp-tf-idf-vs-word2vec-vs-bert-41ff868d1794
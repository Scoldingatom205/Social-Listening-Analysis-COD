import praw

import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import unicodedata
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic

import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime


# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Analyze sentiment
df['sentiment_compound_score'] = df['comment_body'].apply(lambda x: sia.polarity_scores(x)['compound'])

# Define sentiment categories
def sentiment_category(score):
    if score > 0:
        return "Positive"
    elif score <0:
        return "Negative"
    else:
        return "Neutral"


# Perform Preprocessing
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    text = re.sub(r'http\S+|www\S+|bit.ly/\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)


embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
bertopic_model = BERTopic(embedding_model=embedding_model, verbose=True)
embeddings = embedding_model.encode(df['cleaned_comment'].tolist())
topics, probabilities = bertopic_model.fit_transform(df['cleaned_comment'], embeddings)


# Define a dictionary to map multiple topics to custom cluster labels after analysis of topic_modeling results
manual_topic_labels = {
    
    'Map Design': [0, 11, 14, 19, 31, 46, 52, 53, 57, 59, 88, 108],
    'Gameplay Experience': [17, 23, 32, 34, 41, 44, 47, 51, 56, 66, 67, 77, 86, 112, 115],
    'Weapon Balance': [10, 28, 35, 36, 49, 64, 65, 71, 74, 80, 81, 100, 101, 109], 
    'Server Performance/Connectivity': [15, 16, 20, 26, 29, 43, 78, 97],
    'Game/Engine Features': [2, 5, 6, 8, 13, 24, 25, 73, 83, 113],
    'Community Discussions': [3, 12, 27, 42, 48, 50, 70, 89, 91, 114],
}
def map_manual_cluster(topic):
    for cluster, topics in manual_topic_labels.items():
        if topic in topics:
            return cluster
    return 'Other'

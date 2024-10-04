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

def perform_sentiment_and_topic_modeling(steam_reviews_df, reddit_comments_df):
    """Performs sentiment analysis and topic modeling on collected data."""
    
    # Sentiment Analysis
    sia = SentimentIntensityAnalyzer()

    # Apply sentiment analysis to Steam reviews and Reddit comments
    steam_reviews_df['sentiment_score'] = steam_reviews_df['cleaned_review_text'].apply(lambda x: sia.polarity_scores(x)['compound'])
    reddit_comments_df['sentiment_score'] = reddit_comments_df['cleaned_comment_text'].apply(lambda x: sia.polarity_scores(x)['compound'])
    
    # Define sentiment categories based on the sentiment score
    def sentiment_category(score):
        if score > 0:
            return 'Positive'
        elif score < 0:
            return 'Negative'
        else:
            return 'Neutral'
    
    # Apply the sentiment categories
    steam_reviews_df['sentiment_label'] = steam_reviews_df['sentiment_score'].apply(sentiment_category)
    reddit_comments_df['sentiment_label'] = reddit_comments_df['sentiment_score'].apply(sentiment_category)
    
    # Logging that sentiment analysis is complete
    logging.info("Sentiment analysis completed.")

    # Topic Modeling with BERTopic
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    bertopic_model = BERTopic(embedding_model=embedding_model)

    # Generate embeddings for Steam reviews and Reddit comments
    embeddings_steam = embedding_model.encode(steam_reviews_df['cleaned_review_text'].tolist())
    topics_steam, _ = bertopic_model.fit_transform(steam_reviews_df['cleaned_review_text'], embeddings_steam)

    embeddings_reddit = embedding_model.encode(reddit_comments_df['cleaned_comment_text'].tolist())
    topics_reddit, _ = bertopic_model.fit_transform(reddit_comments_df['cleaned_comment_text'], embeddings_reddit)

    # Store topic results in the DataFrame
    steam_reviews_df['topic'] = topics_steam
    reddit_comments_df['topic'] = topics_reddit

    # Logging that topic modeling is complete
    logging.info("Topic modeling completed.")

    return steam_reviews_df, reddit_comments_df
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

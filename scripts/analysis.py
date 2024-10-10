 # Sentiment analysis and topic modeling

def run_analysis():
    """
    Performs sentiment analysis and topic modeling on preprocessed Steam and Reddit data.
    Updates MongoDB with the analysis results.
    """
    # Fetch preprocessed data from MongoDB
    steam_reviews_df = steam_collection.find()
    reddit_comments_df = reddit_collection.find()

    # Perform sentiment analysis
    steam_reviews_df, reddit_comments_df = perform_sentiment_analysis(steam_reviews_df, reddit_comments_df)

    # Perform topic modeling
    steam_reviews_df, reddit_comments_df = perform_topic_modeling(steam_reviews_df, reddit_comments_df)

    # Update MongoDB with the results (e.g., steam_collection.update_many(...))

if __name__ == "__main__":
    run_analysis()


# ------------------------------------------------------ Sentiment Analysis ------------------------------------------------------
def perform_sentiment_analysis(steam_reviews_df, reddit_comments_df):
    """Perform sentiment analysis using VADER."""
    
    sia = SentimentIntensityAnalyzer()
    
    # Analyze sentiment for Steam reviews
    steam_reviews_df['sentiment_score'] = steam_reviews_df['cleaned_review_text'].apply(lambda x: sia.polarity_scores(x)['compound'])
    
    # Analyze sentiment for Reddit comments
    reddit_comments_df['sentiment_score'] = reddit_comments_df['cleaned_comment_text'].apply(lambda x: sia.polarity_scores(x)['compound'])
    
    # Define sentiment categories based on score
    def sentiment_category(score):
        if score > 0:
            return 'Positive'
        elif score < 0:
            return 'Negative'
        else:
            return 'Neutral'

    steam_reviews_df['sentiment_label'] = steam_reviews_df['sentiment_score'].apply(sentiment_category)
    reddit_comments_df['sentiment_label'] = reddit_comments_df['sentiment_score'].apply(sentiment_category)
    
    return steam_reviews_df, reddit_comments_df

# ------------------------------------------------------ Topic Modeling ------------------------------------------------------
def perform_topic_modeling(steam_reviews_df, reddit_comments_df, max_topics=70):
    """Perform topic modeling on Steam reviews and Reddit comments using BERTopic."""
    
    # Load pre-trained embedding model
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Initialize HDBSCAN and BERTopic models with options to limit the number of topics
    hdbscan_model = hdbscan.HDBSCAN(min_cluster_size=15, min_samples=10, prediction_data=True)
    bertopic_model = BERTopic(hdbscan_model=hdbscan_model, nr_topics=max_topics)
    
    logging.info(f"Starting topic modeling with a maximum of {max_topics} topics...")

    # Topic modeling for Steam reviews
    logging.info("Performing topic modeling for Steam reviews...")
    embeddings_steam = embedding_model.encode(steam_reviews_df['cleaned_review_text'].to_numpy())
    topics_steam, _ = bertopic_model.fit_transform(steam_reviews_df['cleaned_review_text'], embeddings_steam)
    steam_reviews_df['topic'] = topics_steam

    logging.info(f"Topic modeling completed for Steam reviews with {len(set(topics_steam))} topics identified.")

    # Topic modeling for Reddit comments
    logging.info("Performing topic modeling for Reddit comments...")
    embeddings_reddit = embedding_model.encode(reddit_comments_df['cleaned_comment_text'].to_numpy())
    topics_reddit, _ = bertopic_model.fit_transform(reddit_comments_df['cleaned_comment_text'], embeddings_reddit)
    reddit_comments_df['topic'] = topics_reddit

    logging.info(f"Topic modeling completed for Reddit comments with {len(set(topics_reddit))} topics identified.")

    # Return updated dataframes with topic assignments
    return steam_reviews_df, reddit_comments_df

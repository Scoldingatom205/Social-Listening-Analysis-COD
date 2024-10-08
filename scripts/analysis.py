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

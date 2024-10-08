 # Text preprocessing functions

def run_preprocessing():
    """
    Retrieves raw data from MongoDB, applies text preprocessing, and stores
    the cleaned text back into MongoDB.
    """
    # Retrieve data from MongoDB
    steam_reviews_df = steam_collection.find()  
    reddit_comments_df = reddit_collection.find()

    # Apply preprocessing to both datasets
    steam_reviews_df['cleaned_review_text'] = steam_reviews_df['review_text'].apply(preprocess_text)
    reddit_comments_df['cleaned_comment_text'] = reddit_comments_df['comment_body'].apply(preprocess_text)

    # Optionally, update MongoDB with cleaned data (this could be in another function)
    # Example: steam_collection.update_many(...)

if __name__ == "__main__":
    run_preprocessing()


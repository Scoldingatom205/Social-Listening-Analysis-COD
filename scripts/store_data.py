# Storing results in MongoDB

def run_storage():
    # Fetch the analyzed data (same process from the previous steps)
    steam_reviews_df = steam_collection.find()
    reddit_comments_df = reddit_collection.find()

    # Store analysis results back into MongoDB
    store_full_analysis_results(steam_reviews_df, reddit_comments_df, steam_collection, reddit_collection)


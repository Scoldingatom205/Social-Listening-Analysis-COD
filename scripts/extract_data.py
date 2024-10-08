# Steam/Reddit data extraction functions

def run_data_collection():
    """
    Collects Steam reviews and Reddit comments, and stores the new data in MongoDB.
    Runs daily without a need for specifying date ranges.
    """
    # Collect and store Steam reviews
    check_and_store_steam_reviews(app_id='1938090', mongo_collection=steam_collection)

    # Collect and store Reddit comments and posts
    check_and_store_reddit_comments(db=reddit_collection, subreddits=["blackops6"])

if __name__ == "__main__":
    run_data_collection()

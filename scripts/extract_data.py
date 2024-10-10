# DAGs Steam/Reddit data collection function

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


# ------------------------------------------------------Steam Data Collection------------------------------------------------------
# Steam Review Collection with Date Range
def get_steam_reviews(app_id, start_date, end_date, max_reviews=1000, retries=5):
    """Collects Steam reviews between specified dates and returns a DataFrame of the results."""
    reviews_list = []
    cursor = '*'
    base_url = f"https://store.steampowered.com/appreviews/{app_id}"

    while len(reviews_list) < max_reviews and retries > 0:
        try:
            params = {
                "cursor": cursor,
                "json": 1,
                "filter": "recent",
                "num_per_page": 100,
                "language": "english"
            }

            response = requests.get(base_url, params=params, timeout=10)
            response.raise_for_status()  # Raise an error for bad HTTP status codes
            data = response.json()

            # If no reviews, exit
            if 'reviews' not in data or not data['reviews']:
                logging.info("No more reviews available.")
                break

            # Collecting reviews within the date range
            for review in data['reviews']:
                review_timestamp = pd.to_datetime(review.get('timestamp_created'), unit='s')
                if start_date <= review_timestamp <= end_date:
                    review_details = {
                        'review_id': review.get('recommendationid'),
                        'author': review['author'].get('steamid'),
                        'review_text': review.get('review'),
                        'votes_up': review.get('votes_up'),
                        'votes_funny': review.get('votes_funny'),
                        'comment_count': review.get('comment_count'),
                        'timestamp_created': review_timestamp,
                        'voted_up': review.get('voted_up'),
                        'playtime_at_review': review['author'].get('playtime_at_review')
                    }
                    reviews_list.append(review_details)

            cursor = data.get('cursor', '')
            if cursor == '':
                break

            time.sleep(5)  # To avoid rate-limiting

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
        except pymongo.errors.PyMongoError as e:
            logging.error(f"MongoDB error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            retries -= 1

    # Convert to DataFrame before returning
    df_reviews = pd.DataFrame(reviews_list)
    logging.info(f"Collected {len(df_reviews)} Steam reviews.")
    
    return df_reviews

# Function to avoid duplicates and store new Steam reviews
def check_and_store_steam_reviews(db, app_id, start_date, end_date):
    """Fetches Steam reviews, checks for duplicates, and stores new reviews in MongoDB."""
    
    # Access the SteamReviews collection from the db object
    steam_collection = db['SteamReviews']  # Correctly accessing the SteamReviews collection

    # Get Steam reviews
    steam_reviews_df = get_steam_reviews(app_id, start_date, end_date)

    if steam_reviews_df.empty:
        logging.info("No new reviews fetched.")
        return steam_reviews_df
    
    # Fetch existing review IDs from MongoDB
    existing_reviews = steam_collection.find({}, {'review_id': 1})
    existing_ids = {doc['review_id'] for doc in existing_reviews}
    
    # Filter out reviews that already exist in MongoDB
    new_reviews = steam_reviews_df[~steam_reviews_df['review_id'].isin(existing_ids)]
    
    # Insert new reviews to MongoDB
    if not new_reviews.empty:
        steam_collection.insert_many(new_reviews.to_dict('records'))
        logging.info(f"Inserted {len(new_reviews)} new Steam reviews into MongoDB.")
    else:
        logging.info("No new Steam reviews to insert.")
    
    return steam_reviews_df


# ------------------------------------------------------ Reddit Data Collection ------------------------------------------------------
# Configure Reddit API connection
reddit = praw.Reddit(
    client_id="blank",          # Replace with your client_id
    client_secret="blank-kM3w",  # Replace with your client_secret
    user_agent="blank",        # Replace with your user_agent
)

def collect_reddit_data(subreddits, post_limit=50, comment_limit=200, min_votes=2, start_date=None, end_date=None):
    posts = []
    comments = []

    for subreddit in subreddits:
        subreddit_instance = reddit.subreddit(subreddit)

        for submission in subreddit_instance.top(limit=post_limit):
            # Convert the submission creation date to a pandas datetime object
            submission_created_utc = pd.to_datetime(submission.created_utc, unit='s')
            
            # Apply date range filter for posts
            if start_date and end_date:
                if not (start_date <= submission_created_utc <= end_date):
                    continue

            # Extract post data
            post_data = {
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "upvote_ratio": submission.upvote_ratio,
                "num_comments": submission.num_comments,
                "created_utc": submission_created_utc,
                "url": submission.url
            }
            posts.append(post_data)

            # Replace MoreComments objects
            submission.comments.replace_more(limit=0)

            # Collect main comments
            for comment in submission.comments:
                comment_created_utc = pd.to_datetime(comment.created_utc, unit='s')

                # Apply date range filter for comments
                if start_date and end_date:
                    if not (start_date <= comment_created_utc <= end_date):
                        continue

                # Ignore downvoted comments
                if comment.score <= 0:
                    continue

                # Store all main comments (comments directly under the post)
                if comment.depth == 0:
                    comments.append({
                        "post_id": submission.id,
                        "comment_id": comment.id,
                        "comment_body": comment.body,
                        "comment_score": comment.score,
                        "comment_author": comment.author.name if comment.author else "Unknown",
                        "comment_created_utc": comment_created_utc,
                        "comment_depth": comment.depth
                    })

                # Collect replies only if the main comment has more than 2 upvotes
                elif comment.depth > 0 and comment.parent() and hasattr(comment.parent(), 'score') and comment.parent().score >= min_votes:
                    if comment.body not in ["[removed]", "[deleted]"]:
                        comments.append({
                            "post_id": submission.id,
                            "comment_id": comment.id,
                            "comment_body": comment.body,
                            "comment_score": comment.score,
                            "comment_author": comment.author.name if comment.author else "Unknown",
                            "comment_created_utc": comment_created_utc,
                            "comment_depth": comment.depth
                        })

    df_posts = pd.DataFrame(posts)
    df_comments = pd.DataFrame(comments)
    
    logging.info(f"Collected {len(posts)} posts and {len(comments)} comments.")
    
    return df_posts, df_comments


def check_and_store_reddit_comments(db, subreddits, start_date, end_date):
    try:
        logging.info(f"Fetching Reddit comments for subreddits: {subreddits} between {start_date} and {end_date}")
        
        # Fetch Reddit posts and comments
        reddit_posts_df, reddit_comments_df = collect_reddit_data(subreddits, start_date=start_date, end_date=end_date)

        # Access collections from the db object
        reddit_comments_collection = db['RedditComments']  # Access the RedditComments collection
        reddit_posts_collection = db['RedditPosts']  # Access the RedditPosts collection

        logging.info("Checking for duplicate Reddit comments.")

        # Handle inserting comments
        existing_comments = reddit_comments_collection.find({}, {'comment_id': 1})
        existing_ids = {doc['comment_id'] for doc in existing_comments}
        new_comments = reddit_comments_df[~reddit_comments_df['comment_id'].isin(existing_ids)]

        if not new_comments.empty:
            reddit_comments_collection.insert_many(new_comments.to_dict('records'))
            logging.info(f"Inserted {len(new_comments)} new Reddit comments into MongoDB.")
        else:
            logging.info("No new Reddit comments to insert.")

        # Handle inserting posts
        existing_posts = reddit_posts_collection.find({}, {'id': 1})
        existing_post_ids = {doc['id'] for doc in existing_posts}
        new_posts = reddit_posts_df[~reddit_posts_df['id'].isin(existing_post_ids)]

        if not new_posts.empty:
            reddit_posts_collection.insert_many(new_posts.to_dict('records'))
            logging.info(f"Inserted {len(new_posts)} new Reddit posts into MongoDB.")
        else:
            logging.info("No new Reddit posts to insert.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
    except pymongo.errors.PyMongoError as e:
        logging.error(f"MongoDB error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    return reddit_posts_df, reddit_comments_df

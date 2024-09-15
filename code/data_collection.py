def get_steam_reviews(app_id, max_reviews=1000, num_per_page=100):
    reviews_list = []
    cursor = '*'
    base_url = f"https://store.steampowered.com/appreviews/{app_id}"
    
    # Define start and end dates for filtering
    start_date = pd.Timestamp("2024-08-30")
    end_date = pd.Timestamp("2024-09-11")
    
    while len(reviews_list) < max_reviews:
        # Set up parameters for the API request
        params = {
            'json': 1,
            'num_per_page': num_per_page,
            'cursor': cursor,
            'filter': 'recent',
            'language': 'english'
        }
        
        # Make the request to Steam API
        response = requests.get(base_url, params=params)
        data = response.json()

        # Break if no more reviews are available
        if not data['reviews']:
            break

        # Process the reviews
        for review in data['reviews']:
            review_timestamp = pd.to_datetime(review['timestamp_created'], unit='s')
            
            # Only collect reviews within the date range
            if start_date <= review_timestamp <= end_date:
                review_data = {
                    'review_id': review['recommendationid'],
                    'author': review['author']['steamid'],
                    'review_text': review['review'],
                    'votes_up': review['votes_up'],
                    'votes_funny': review['votes_funny'],
                    'weighted_vote_score': review['weighted_vote_score'],
                    'comment_count': review['comment_count'],
                    'timestamp_created': review_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'voted_up': review['voted_up'],  # True for positive reviews, False for negative
                    'language': review['language'],
                    'playtime_at_review': review['author']['playtime_at_review']
                }
                reviews_list.append(review_data)

        # Update the cursor for the next batch
        cursor = data['cursor']

        # Sleep to avoid rate-limiting
        time.sleep(1)

    # Convert list of reviews into a DataFrame
    df_reviews = pd.DataFrame(reviews_list)
    
    return df_reviews

# Configure Reddit API connection
reddit = praw.Reddit(
    client_id="CLIENT_ID",          # Replace with your client_id
    client_secret="CLIENT_SECRET",  # Replace with your client_secret
    user_agent="USERNAME",        # Replace with your user_agent
)

# Define subreddits related to Black Ops 6
def collect_reddit_data(subreddits, post_limit=50, comment_limit=150, min_comments=40):
    posts = []
    comments = []

    for subreddit in subreddits:
        print(f"Collecting posts from subreddit: {subreddit}")
        subreddit_instance = reddit.subreddit(subreddit)

        # Get the top posts
        for submission in subreddit_instance.top(limit=post_limit):
            post_data = {
                "id": submission.id,
                "subreddit": subreddit,
                "title": submission.title,
                "selftext": submission.selftext,
                "score": submission.score,
                "upvote_ratio": submission.upvote_ratio,
                "num_comments": submission.num_comments,
                "created_utc": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                "url": submission.url
            }
            posts.append(post_data)

            # Fetch comments for each post
            submission.comments.replace_more(limit=0)  # Remove 'MoreComments' objects
            comment_counter = 0  # Ensure not to exceed comment limit

            for comment in submission.comments.list():
                if comment.body not in ["[removed]", "[deleted]"] and comment_counter < comment_limit:
                    comment_data = {
                        "post_id": submission.id,
                        "comment_id": comment.id,
                        "comment_body": comment.body,
                        "comment_score": comment.score,
                        "comment_author": comment.author.name if comment.author else "Unknown",
                        "comment_created_utc": datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                        "comment_depth": comment.depth
                    }
                    comments.append(comment_data)
                    comment_counter += 1

    df_posts = pd.DataFrame(posts)
    df_comments = pd.DataFrame(comments)
    print(f"Collected {len(posts)} posts and {len(comments)} comments.")
    
    # Save the data only at the end
    return df_posts, df_comments


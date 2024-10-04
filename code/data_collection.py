# Steam Review Collection
def get_steam_reviews(app_id, max_reviews=100, num_per_page=50):
    """Collects Steam reviews and returns a DataFrame of the results."""
    reviews_list = []
    cursor = '*'
    base_url = f"https://store.steampowered.com/appreviews/{app_id}"
    
    try:
        while len(reviews_list) < max_reviews:
            params = {
                'json': 1,
                'num_per_page': num_per_page,
                'cursor': cursor,
                'filter': 'recent',
                'language': 'english'
            }
            response = requests.get(base_url, params=params)
            data = response.json()

            if not data['reviews']:
                break

            for review in data['reviews']:
                reviews_list.append({
                    'review_id': review['recommendationid'],
                    'author': review['author']['steamid'],
                    'review_text': review['review'],
                    'votes_up': review['votes_up'],
                    'votes_funny': review['votes_funny'],
                    'comment_count': review['comment_count'],
                    'timestamp_created': pd.to_datetime(review['timestamp_created'], unit='s'),
                    'voted_up': review['voted_up'],
                    'playtime_at_review': review['author']['playtime_at_review']
                })

            cursor = data['cursor']
            time.sleep(1)  # To avoid rate-limiting

        df_reviews = pd.DataFrame(reviews_list)
        logging.info(f"Collected {len(df_reviews)} Steam reviews.")
        return df_reviews

    except Exception as e:
        logging.error(f"Error collecting Steam reviews: {e}")
        return pd.DataFrame()

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Reddit Data Collection
def collect_reddit_data(subreddits, post_limit=10, comment_limit=200):
    """Collect Reddit posts and comments."""
    posts = []
    comments = []
    
    try:
        for subreddit in subreddits:
            subreddit_instance = reddit.subreddit(subreddit)

            for submission in subreddit_instance.top(limit=post_limit):
                post_data = {
                    "id": submission.id,
                    "subreddit": subreddit,
                    "title": submission.title,
                    "selftext": submission.selftext,
                    "score": submission.score,
                    "upvote_ratio": submission.upvote_ratio,
                    "num_comments": submission.num_comments,
                    "created_utc": pd.to_datetime(submission.created_utc, unit='s'),
                    "url": submission.url
                }
                posts.append(post_data)

                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list()[:comment_limit]:
                    if comment.body not in ["[removed]", "[deleted]"]:
                        comments.append({
                            "post_id": submission.id,
                            "comment_id": comment.id,
                            "comment_body": comment.body,
                            "comment_score": comment.score,
                            "comment_author": comment.author.name if comment.author else "Unknown",
                            "comment_created_utc": pd.to_datetime(comment.created_utc, unit='s'),
                            "comment_depth": comment.depth
                        })

        df_posts = pd.DataFrame(posts)
        df_comments = pd.DataFrame(comments)
        logging.info(f"Collected {len(df_posts)} Reddit posts and {len(df_comments)} comments.")
        return df_posts, df_comments

    except Exception as e:
        logging.error(f"Error collecting Reddit data: {e}")
        return pd.DataFrame(), pd.DataFrame()

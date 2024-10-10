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


# ------------------------------------------------------------------------ Preprocess Function ------------------------------------------------------------------------
# Ensure that stopwords and other necessary resources are downloaded
import nltk
nltk.download('stopwords')
nltk.download('punkt')

# Define a preprocessing function
def preprocess_text(text):
    """Preprocesses the text by cleaning and tokenizing it."""
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|bit.ly/\S+', '', text)

    # Remove non-alphabetical characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()

    # Tokenize and remove stopwords
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    
    return ' '.join(filtered_words)

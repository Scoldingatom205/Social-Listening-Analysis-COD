# Preprocessing function to clean the text data
def preprocess_text(text):
        # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        # Remove URLs
    text = re.sub(r'http\S+|www\S+|bit.ly/\S+', '', text)
        # Remove special characters, numbers, and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Convert to lowercase
    text = text.lower()
        # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in text.split() if word not in stop_words]
    return ' '.join(words)

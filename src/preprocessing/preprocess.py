import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    """Cleans and preprocesses complaint text."""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^a-z\s]', '', text)  # Remove punctuation and special characters
    words = nltk.word_tokenize(text)  # Tokenize text
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]  # Lemmatization
    return ' '.join(words)

# # Load complaints CSV
# input_file = "data/complaints.csv"  # Update path as needed
# output_file = "data/cleaned_complaints.csv"
# df = pd.read_csv(input_file)

# df['cleaned_complaint'] = df['complaint'].astype(str).apply(preprocess_text)

# # Save cleaned data to new CSV
# df[['cleaned_complaint']].to_csv(output_file, index=False)
# print(f"Preprocessed data saved to {output_file}")

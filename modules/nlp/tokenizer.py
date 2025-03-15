import re
import nltk
import string
from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Ensure required nltk resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

class Tokenizer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.tokenizer = TreebankWordTokenizer()

    def preprocess(self, text, use_stemming=False, use_lemmatization=True):
        """
        Preprocesses the input text by converting it to lowercase, removing punctuation,
        tokenizing, filtering out stopwords, and applying stemming or lemmatization.
        """
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = self.tokenizer.tokenize(text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        
        if use_stemming:
            filtered_tokens = [self.stemmer.stem(word) for word in filtered_tokens]
        elif use_lemmatization:
            filtered_tokens = [self.lemmatizer.lemmatize(word) for word in filtered_tokens]
        
        return filtered_tokens

if __name__ == "__main__":
    tokenizer = Tokenizer()
    
    test_sentences = [
        "Hey there!", "Can you play some music?", "Stop the movie", "Launch the game",
        "Remind me to buy groceries", "Tell me about Python programming", "Goodbye!",
        "What's the weather like?", "Tell me a joke", "Take a note about the meeting", 
        "Set an alarm for 7 AM", "Give me the latest news", "What time is it?", "What's today's date?"
    ]
    
    for sentence in test_sentences:
        tokens = tokenizer.preprocess(sentence)
        print(f"Input: {sentence} -> Tokens: {tokens}")
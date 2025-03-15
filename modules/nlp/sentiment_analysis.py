import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from memory import MemoryModule
nltk.download('vader_lexicon')

class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()
        self.memory = MemoryModule()  # Tracks sentiment over time
    
    def analyze_sentiment(self, text):
        """
        Analyzes sentiment and classifies it as positive, neutral, or negative.
        Also updates sentiment history in memory.
        """
        scores = self.analyzer.polarity_scores(text)
        sentiment = "neutral"
        
        if scores['compound'] >= 0.05:
            sentiment = "positive"
        elif scores['compound'] <= -0.05:
            sentiment = "negative"
        
        # Store sentiment history
        self.memory.add_to_history("sentiment", {"text": text, "sentiment": sentiment, "score": scores['compound']})
        
        return {
            "text": text,
            "compound_score": scores['compound'],
            "sentiment": sentiment
        }
    
    def get_sentiment_trend(self, last_n=5):
        """
        Retrieves the sentiment trend based on the last N interactions.
        """
        history = self.memory.get_history()[-last_n:]
        
        if not history:
            return "No sentiment history available."
        
        pos_count = sum(1 for entry in history if entry["ai"] == "positive")
        neg_count = sum(1 for entry in history if entry["ai"] == "negative")
        
        if pos_count > neg_count:
            return "User's sentiment is trending positive."
        elif neg_count > pos_count:
            return "User's sentiment is trending negative."
        else:
            return "User's sentiment appears neutral."

if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    test_sentences = [
        "I love this! It's amazing!",
        "I'm not sure how I feel about this.",
        "This is the worst experience ever!",
        "The weather is nice today.",
        "I absolutely hate doing chores."
    ]
    
    for sentence in test_sentences:
        result = analyzer.analyze_sentiment(sentence)
        print(f"Input: {result['text']} -> Sentiment: {result['sentiment']} (Score: {result['compound_score']})")
    
    # Check sentiment trend
    print(analyzer.get_sentiment_trend())
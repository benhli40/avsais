# Intent recognition module with fuzzy matching and multiple intent detection
import re
from fuzzywuzzy import process

class IntentRecognizer:
    def __init__(self):
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
            "farewell": ["bye", "goodbye", "see you", "later"],
            "music_play": ["play music", "start song", "play a track"],
            "music_stop": ["stop music", "pause song", "end track"],
            "movie_play": ["play movie", "start film", "watch movie"],
            "movie_stop": ["stop movie", "pause film", "end movie"],
            "game_launch": ["launch game", "start game", "play game"],
            "game_close": ["close game", "exit game", "stop game"],
            "reminder_set": ["set reminder", "remind me", "schedule task"],
            "query": ["what is", "how to", "tell me about"],
            "weather_check": ["what's the weather", "weather update", "check forecast"],
            "joke_telling": ["tell me a joke", "make me laugh", "say something funny"],
            "note_taking": ["take a note", "save this note", "remember this"],
            "alarm_set": ["set an alarm", "wake me up at", "schedule an alarm"],
            "news_check": ["what's the news", "latest headlines", "news update"],
            "time_check": ["what time is it", "current time", "tell me the time"],
            "date_check": ["what's today's date", "current date", "tell me the date"]
        }

    def recognize_intent(self, text):
        text = text.lower()
        detected_intents = []
        
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if re.search(rf"\b{keyword}\b", text):
                    detected_intents.append(intent)

        if not detected_intents:
            # Use fuzzy matching to find the closest intent
            all_keywords = [kw for intent in self.intents.values() for kw in intent]
            closest_match, confidence = process.extractOne(text, all_keywords)
            if confidence > 75:
                for intent, keywords in self.intents.items():
                    if closest_match in keywords:
                        return [intent]

            return ["unknown"]

        return detected_intents

if __name__ == "__main__":
    recognizer = IntentRecognizer()
    test_inputs = [
        "Hey there!", "Can you play some music?", "Stop the movie", "Launch the game", 
        "Remind me to buy groceries", "Tell me about Python programming", "Goodbye!",
        "What's the weather like?", "Tell me a joke", "Take a note about the meeting", 
        "Set an alarm for 7 AM", "Give me the latest news", "What time is it?", "What's today's date?",
        "Play music and set a reminder"
    ]
    
    for text in test_inputs:
        intents = recognizer.recognize_intent(text)
        print(f"Input: {text} -> Recognized Intents: {intents}")
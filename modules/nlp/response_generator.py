import re
import random
import json
import os
from reinforcement_learning import ReinforcementLearning
from memory import MemoryModule
from intent_recognizer import IntentRecognizer

class ResponseGenerator:
    def __init__(self):
        self.responses = {
            "greeting": ["Hello, {name}! How can I assist you?", "Hey {name}, what's up?", "Hi {name}! What can I do for you?"],
            "farewell": ["Goodbye, {name}! Have a great day!", "See you later, {name}!", "Bye {name}, stay safe!"],
            "music_play": ["Playing your favorite music!", "Starting playback now.", "Enjoy your music!"],
            "music_stop": ["Stopping the music.", "Music playback paused.", "Music stopped."],
            "movie_play": ["Starting the movie now!", "Enjoy your film!", "Playing your selected movie."],
            "movie_stop": ["Pausing the movie.", "Movie playback stopped.", "Movie paused."],
            "game_launch": ["Launching your game!", "Starting the game now!", "Game is loading.", "Have fun gaming!"],
            "game_close": ["Closing the game.", "Game session ended.", "Game is now closed."],
            "reminder_set": ["Reminder set successfully!", "I will remind you on time.", "Your reminder is scheduled."],
            "query": ["Let me look that up for you.", "Here’s what I found.", "I can help with that. Let’s see..."],
            "weather_check": ["Fetching the latest weather update.", "Here’s today’s weather forecast.", "Checking the weather now."],
            "joke_telling": ["Why don’t scientists trust atoms? Because they make up everything!", "Want to hear a joke? You! Just kidding!", "Here's a joke: I told my wife she should embrace her mistakes. She gave me a hug."],
            "note_taking": ["Note saved successfully!", "I’ve recorded your note.", "Your note has been stored."],
            "alarm_set": ["Alarm set successfully!", "Your alarm is scheduled.", "I will wake you up on time."],
            "news_check": ["Fetching the latest news for you.", "Here’s what’s happening in the world.", "Getting today’s headlines."],
            "time_check": ["Checking the current time.", "The time is now displayed on your screen.", "Here’s the current time."],
            "date_check": ["Today's date is displayed.", "Checking the current date.", "Here’s today’s date for you."]
        }
        self.memory = MemoryModule()
        self.reinforcement = ReinforcementLearning()
        self.intent_recognizer = IntentRecognizer()
    
    def generate_response(self, text, user_name="User"):
        intent = self.intent_recognizer.recognize_intent(text)
        
        if intent in self.responses:
            response = random.choice(self.responses[intent]).format(name=user_name)
            self.reinforcement.provide_feedback(intent, 1, f"Generated response: {response}")
            self.memory.add_to_history(text, response)
            return response
        else:
            return "I'm not sure how to respond to that. Would you like me to learn this?"

if __name__ == "__main__":
    responder = ResponseGenerator()
    
    test_inputs = [
        "Hey there!", "Can you play some music?", "Stop the movie", "Launch the game", 
        "Remind me to buy groceries", "Tell me about Python programming", "Goodbye!",
        "What's the weather like?", "Tell me a joke", "Take a note about the meeting", 
        "Set an alarm for 7 AM", "Give me the latest news", "What time is it?", "What's today's date?"
    ]
    
    for text in test_inputs:
        response = responder.generate_response(text, user_name="Alex")
        print(f"Input: {text} -> Response: {response}")
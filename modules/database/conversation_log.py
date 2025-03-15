# Stores chat history
import json
import os
from datetime import datetime

LOG_FILE = "conversation_log.json"

class ConversationLog:
    def __init__(self):
        self.log_data = self.load_log()
    
    def load_log(self):
        """Loads conversation logs from a file."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []
    
    def save_log(self):
        """Saves the updated conversation logs to a file."""
        with open(LOG_FILE, "w") as f:
            json.dump(self.log_data, f, indent=4)
    
    def log_conversation(self, user_input, ai_response):
        """Logs a conversation entry with timestamp."""
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user_input,
            "ai": ai_response
        }
        self.log_data.append(entry)
        self.save_log()
    
    def retrieve_conversation(self, keyword=None, date=None):
        """Retrieves conversations based on keyword or date."""
        results = []
        for entry in self.log_data:
            if keyword and keyword.lower() in entry["user"].lower() or keyword.lower() in entry["ai"].lower():
                results.append(entry)
            elif date and date in entry["timestamp"]:
                results.append(entry)
        return results if results else "No matching conversations found."

if __name__ == "__main__":
    convo_log = ConversationLog()
    
    # Example usage
    convo_log.log_conversation("Hello!", "Hi there! How can I assist you?")
    convo_log.log_conversation("What is AI?", "AI stands for Artificial Intelligence.")
    
    print("🔍 Retrieving conversations containing 'AI':")
    print(convo_log.retrieve_conversation(keyword="AI"))
    
    print("📅 Retrieving conversations from today:")
    print(convo_log.retrieve_conversation(date=datetime.now().strftime("%Y-%m-%d")))
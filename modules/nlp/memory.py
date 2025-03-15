import json
import os
from collections import deque
from fuzzywuzzy import process
from reinforcement_learning import ReinforcementLearning

class MemoryModule:
    def __init__(self, memory_file="memory.json", history_limit=10):
        self.memory_file = memory_file
        self.history_limit = history_limit
        self.memory = self.load_memory()
        self.conversation_history = deque(self.memory.get("conversation_history", []), maxlen=history_limit)
        self.reinforcement = ReinforcementLearning()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        return {}

    def save_memory(self):
        self.memory["conversation_history"] = list(self.conversation_history)
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=4)

    def remember(self, category, key, value):
        if category not in self.memory:
            self.memory[category] = {}
        if key not in self.memory[category]:
            self.memory[category][key] = []
        self.memory[category][key].append(value)
        self.save_memory()

    def recall(self, category, key):
        if category in self.memory and key in self.memory[category]:
            self.reinforcement.provide_feedback(key, 1)  # Reinforcement Learning prioritizes frequently accessed info
            return self.memory[category][key]
        
        # Fuzzy matching for misremembered terms
        all_keys = [k for cat in self.memory.values() for k in cat]
        closest_match, confidence = process.extractOne(key, all_keys)
        if closest_match and confidence > 75:
            for category in self.memory:
                if closest_match in self.memory[category]:
                    return self.memory[category][closest_match]
        
        return "I don't remember that."

    def add_to_history(self, user_input, response):
        self.conversation_history.append({"user": user_input, "ai": response})
        self.save_memory()

    def get_history(self, last_n=5):
        return list(self.conversation_history)[-last_n:]

if __name__ == "__main__":
    memory = MemoryModule()

    # Example: Storing and Retrieving Memories
    memory.remember("Personal", "favorite_color", "Blue")
    memory.remember("Work", "project_deadline", "March 15th")

    print("Recalling favorite color:", memory.recall("Personal", "favorite_color"))
    print("Recalling project deadline:", memory.recall("Work", "project_deadline"))
    print("Recalling misremembered key (fuzzy match):", memory.recall("Personal", "fav color"))

    # Adding conversation history
    memory.add_to_history("Hey there!", "Hello! How can I assist you?")
    print("Last 3 conversations:", memory.get_history(3))
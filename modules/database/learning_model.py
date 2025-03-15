# AI learning module
import json
import os
import random
from nlp.reinforcement_learning import ReinforcementLearning
from nlp.knowledge_base import KnowledgeBase

LEARNING_MODEL_FILE = "learning_model.json"

class LearningModel:
    def __init__(self):
        """Initializes the learning model, reinforcement learning, and knowledge base."""
        self.learning_data = self.load_learning_data()
        self.reinforcement = ReinforcementLearning()
        self.knowledge_base = KnowledgeBase()
    
    def load_learning_data(self):
        """Loads the learning model data from a file."""
        if os.path.exists(LEARNING_MODEL_FILE):
            with open(LEARNING_MODEL_FILE, "r") as f:
                return json.load(f)
        return {}
    
    def save_learning_data(self):
        """Saves the learning model data to a file."""
        with open(LEARNING_MODEL_FILE, "w") as f:
            json.dump(self.learning_data, f, indent=4)
    
    def learn_from_interaction(self, user_input, ai_response, feedback):
        """Learns from user interactions based on feedback."""
        if user_input not in self.learning_data:
            self.learning_data[user_input] = {"responses": [], "feedback": []}
        
        self.learning_data[user_input]["responses"].append(ai_response)
        self.learning_data[user_input]["feedback"].append(feedback)
        
        # Reinforcement learning integration
        self.reinforcement.provide_feedback(user_input, feedback, f"Response: {ai_response}")
        self.save_learning_data()
    
    def suggest_response(self, user_input):
        """Suggests a response based on previous interactions and reinforcement learning."""
        if user_input in self.learning_data:
            responses = self.learning_data[user_input]["responses"]
            return random.choice(responses)
        
        return self.knowledge_base.get_fact("General", user_input) or "I'm not sure. Would you like to teach me?"
    
    def improve_knowledge(self, key, value):
        """Allows AVSAIS to learn new knowledge from user inputs."""
        self.knowledge_base.add_fact("General", key, value)
        print("✅ Knowledge updated!")
    
    def review_learning_data(self):
        """Returns learned interactions for review."""
        return self.learning_data

if __name__ == "__main__":
    model = LearningModel()
    
    # Example learning interactions
    model.learn_from_interaction("What is AI?", "AI stands for Artificial Intelligence.", 1)
    model.learn_from_interaction("Tell me a joke", "Why did the chicken cross the road?", 2)
    
    print("🔍 Suggested Response:", model.suggest_response("What is AI?"))
    print("📚 Learning Data Review:", model.review_learning_data())
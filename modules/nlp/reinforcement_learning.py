import json
import os
from collections import deque

class ReinforcementLearning:
    def __init__(self, learning_file="learning_data.json", history_limit=10, decay_factor=0.9, min_confidence=0.5):
        self.learning_file = learning_file
        self.history_limit = history_limit  # Limits how much recent feedback matters
        self.decay_factor = decay_factor  # Older actions gradually lose impact
        self.min_confidence = min_confidence  # Minimum confidence required to suggest an action
        self.learning_data = self.load_learning_data()
        self.recent_actions = deque(maxlen=history_limit)  # Tracks recent actions for weighted learning
    
    def load_learning_data(self):
        if os.path.exists(self.learning_file):
            with open(self.learning_file, "r") as f:
                return json.load(f)
        return {}
    
    def save_learning_data(self):
        with open(self.learning_file, "w") as f:
            json.dump(self.learning_data, f, indent=4)
    
    def provide_feedback(self, action, reward, details="None"):
        """
        Updates the reinforcement learning system with user feedback and tracks details of the action.
        """
        if action not in self.learning_data:
            self.learning_data[action] = {"count": 0, "reward_sum": 0, "history": []}
        
        self.learning_data[action]["count"] += 1
        self.learning_data[action]["reward_sum"] += reward
        self.learning_data[action]["history"].append(details)
        
        # Apply decay to older rewards
        self.learning_data[action]["reward_sum"] *= self.decay_factor
        
        # Store recent actions for weighted learning
        self.recent_actions.append((action, reward))
        
        self.save_learning_data()
    
    def get_action_score(self, action, weighted=True):
        """
        Returns the average reward score of an action.
        Uses weighted learning, giving more importance to recent feedback.
        """
        if action not in self.learning_data or self.learning_data[action]["count"] == 0:
            return 0  # Default score if no data is available
        
        base_score = self.learning_data[action]["reward_sum"] / self.learning_data[action]["count"]
        
        if weighted and action in dict(self.recent_actions):
            recent_rewards = [r for a, r in self.recent_actions if a == action]
            weight_factor = len(recent_rewards) / self.history_limit
            return base_score * (1 - weight_factor) + (sum(recent_rewards) / len(recent_rewards)) * weight_factor
        
        return base_score
    
    def suggest_best_action(self):
        """
        Suggests the best action based on previous feedback, factoring in recent feedback weight.
        """
        if not self.learning_data:
            return "No data available yet."
        
        best_action = max(self.learning_data, key=lambda action: self.get_action_score(action))
        best_score = self.get_action_score(best_action)
        
        if best_score < self.min_confidence:
            return "No confident suggestion available, user input needed."
        
        return best_action, best_score
    
    def remove_low_relevance_actions(self, threshold=-5):
        """
        Removes actions that have a consistently low score.
        """
        self.learning_data = {action: data for action, data in self.learning_data.items() 
                              if data["reward_sum"] >= threshold}
        self.save_learning_data()
    
    def get_action_history(self, action):
        """
        Returns detailed history of an action's past occurrences.
        """
        if action in self.learning_data and "history" in self.learning_data[action]:
            return self.learning_data[action]["history"]
        return ["No recorded history for this action."]

if __name__ == "__main__":
    rl = ReinforcementLearning()
    
    # Example user feedback with detailed tracking
    rl.provide_feedback("Play Music", 1, "User played 'Bohemian Rhapsody'")
    rl.provide_feedback("Stop Music", -1, "User stopped music after 10 seconds")
    rl.provide_feedback("Search Weather", 2, "User searched for today's weather in New York")
    rl.provide_feedback("Play Music", 3, "User played 'Stairway to Heaven'")
    
    print("Score for 'Play Music':", rl.get_action_score("Play Music"))
    print("Score for 'Stop Music':", rl.get_action_score("Stop Music"))
    print("Best Suggested Action:", rl.suggest_best_action())
    print("Action History for 'Play Music':", rl.get_action_history("Play Music"))
    
    # Remove actions with very low relevance
    rl.remove_low_relevance_actions()
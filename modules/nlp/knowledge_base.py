import json
import os
from fuzzywuzzy import process
from reinforcement_learning import ReinforcementLearning
from web_scraper import WebScraper

class KnowledgeBase:
    def __init__(self, knowledge_file="knowledge.json"):
        self.knowledge_file = knowledge_file
        self.knowledge = self.load_knowledge()
        self.reinforcement = ReinforcementLearning()
        self.web_scraper = WebScraper()
    
    def load_knowledge(self):
        if os.path.exists(self.knowledge_file):
            with open(self.knowledge_file, "r") as f:
                return json.load(f)
        return {}
    
    def save_knowledge(self):
        with open(self.knowledge_file, "w") as f:
            json.dump(self.knowledge, f, indent=4)
    
    def add_fact(self, category, key, value):
        if category not in self.knowledge:
            self.knowledge[category] = {}
        if key not in self.knowledge[category]:
            self.knowledge[category][key] = []
        self.knowledge[category][key].append(value[:500])  # Store only first 500 characters for summarization
        self.save_knowledge()
    
    def get_fact(self, category, key):
        if category in self.knowledge and key in self.knowledge[category]:
            self.reinforcement.provide_feedback(key, 1)  # Reinforcement learning tracks frequently accessed knowledge
            return self.knowledge[category][key]
        return ["I don't have information on that."]
    
    def search_knowledge(self, query):
        query = query.lower()
        results = {}
        
        # Search through categories, keys, and values
        for category, facts in self.knowledge.items():
            if query in category.lower():
                results[category] = facts
            for key, values in facts.items():
                if query in key.lower() or any(query in v.lower() for v in values):
                    results.setdefault(category, {})[key] = values
        
        if results:
            return results
        
        # Fuzzy Matching for Similar Results (Categories, Keys, and Values)
        all_categories = list(self.knowledge.keys())
        closest_category_match = process.extractOne(query, all_categories)
        if closest_category_match and closest_category_match[1] > 75:
            return {closest_category_match[0]: self.knowledge[closest_category_match[0]]}
        
        all_keys = [key for cat in self.knowledge.values() for key in cat]
        closest_key_match = process.extractOne(query, all_keys)
        if closest_key_match and closest_key_match[1] > 75:
            for category in self.knowledge:
                if closest_key_match[0] in self.knowledge[category]:
                    return {category: {closest_key_match[0]: self.get_fact(category, closest_key_match[0])}}

        # If no knowledge is found, trigger web scraping
        print("No matching information found. Searching the web...")
        web_result = self.web_scraper.fetch_information(query)
        return web_result if web_result else "Still couldn't find relevant information."

if __name__ == "__main__":
    knowledge = KnowledgeBase()
    
    # Example: Adding categorized facts to the knowledge base
    knowledge.add_fact("Programming", "Python", "Python is a programming language known for its simplicity.")
    knowledge.add_fact("AI", "Machine Learning", "A subset of AI that enables systems to learn from data.")
    knowledge.add_fact("Programming", "Python", "Python is widely used for AI and data science.")
    knowledge.add_fact("Science", "Gravity", "Gravity is a force that pulls objects toward Earth.")
    
    # Example: Retrieving categorized facts
    print("Fact about Python:", knowledge.get_fact("Programming", "Python"))
    print("Fact about Machine Learning:", knowledge.get_fact("AI", "Machine Learning"))
    print("Searching for 'intelligence':", knowledge.search_knowledge("intelligence"))
    print("Searching for 'Pythn' (fuzzy match):", knowledge.search_knowledge("Pythn"))
    print("Searching for 'Sciense' (fuzzy category match):", knowledge.search_knowledge("Sciense"))
    print("Searching for unknown topic (triggers web search):", knowledge.search_knowledge("Quantum Computing"))

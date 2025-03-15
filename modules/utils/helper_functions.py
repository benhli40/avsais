# Helper functions
import os
import json
import datetime
import random
import hashlib


def get_current_timestamp():
    """Returns the current timestamp in a readable format."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_unique_id(data):
    """Generates a unique hash ID for a given data string."""
    return hashlib.sha256(data.encode()).hexdigest()


def load_json(file_path):
    """Loads data from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}


def save_json(file_path, data):
    """Saves data to a JSON file."""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def get_random_choice(choices):
    """Returns a random item from a given list."""
    return random.choice(choices) if choices else None


def clean_text(text):
    """Cleans input text by removing extra spaces and converting to lowercase."""
    return " ".join(text.lower().strip().split())


def validate_input(text, valid_choices):
    """Validates user input against a list of valid choices."""
    return text.lower() in [choice.lower() for choice in valid_choices]


def ensure_directory_exists(directory):
    """Ensures that a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    print("✅ Helper Functions Ready")
    print("📅 Current Timestamp:", get_current_timestamp())
    print("🔑 Unique ID for 'AVSAIS':", generate_unique_id("AVSAIS"))
    print("🎲 Random Choice Example:", get_random_choice(["Option A", "Option B", "Option C"]))
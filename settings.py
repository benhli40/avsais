import os
import json
from dotenv import load_dotenv
import pyttsx3

# Load environment variables
load_dotenv()

SETTINGS_FILE = "avsais_settings.json"

def load_settings():
    """Loads settings from a JSON file, or initializes default settings."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {
        "theme": "dark",  # Options: dark, light, futuristic, minimalistic
        "voice": "male",  # Options: male, american_female, british_female
        "volume": 1.0,  # Range: 0.0 - 1.0
        "speech_rate": 150  # Speech speed
    }

def save_settings(settings):
    """Saves the current settings to a JSON file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def apply_voice_settings(engine, voice):
    """Applies voice settings based on user selection."""
    voices = engine.getProperty("voices")
    
    if voice == "american_female":
        for v in voices:
            if "Zira" in v.name:
                engine.setProperty("voice", v.id)
                break
    elif voice == "british_female":
        for v in voices:
            if "British" in v.name:
                engine.setProperty("voice", v.id)
                break
    else:  # Default to male
        engine.setProperty("voice", voices[0].id)

def configure_speech_engine():
    """Configures the text-to-speech engine based on settings."""
    settings = load_settings()
    engine = pyttsx3.init()
    engine.setProperty("rate", settings["speech_rate"])
    engine.setProperty("volume", settings["volume"])
    apply_voice_settings(engine, settings["voice"])
    return engine

def display_current_settings():
    """Displays the current settings for the user."""
    settings = load_settings()
    print("🛠️ AVSAIS Settings:")
    for key, value in settings.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    settings = load_settings()
    display_current_settings()
    
    # Example: Modify settings
    settings["theme"] = "futuristic"
    settings["voice"] = "american_female"
    settings["volume"] = 0.8
    settings["speech_rate"] = 170
    
    save_settings(settings)
    print("✅ Settings updated successfully!")
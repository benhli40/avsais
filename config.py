# Configuration settings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration settings for AVSAIS."""
    
    # Database Configuration
    DB_FILE = os.getenv("DB_FILE", "avsais_database.db")
    
    # Logging Configuration
    LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "logs")
    LOG_FILE = os.path.join(LOG_DIRECTORY, "avsais.log")
    
    # Weather API Configuration
    WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Marble Falls")
    
    # Email Configuration (Gmail by default)
    EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
    EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", 465))
    EMAIL_IMAP_SERVER = os.getenv("EMAIL_IMAP_SERVER", "imap.gmail.com")
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    
    # System Monitoring Thresholds
    CPU_THRESHOLD = int(os.getenv("CPU_THRESHOLD", 85))  # Alert when CPU usage exceeds 85%
    RAM_THRESHOLD = int(os.getenv("RAM_THRESHOLD", 85))  # Alert when RAM usage exceeds 85%
    DISK_THRESHOLD = int(os.getenv("DISK_THRESHOLD", 90)) # Alert when Disk usage exceeds 90%
    
    # Paths for Entertainment & Data Storage
    MOVIE_DIRECTORY = os.getenv("MOVIE_DIRECTORY", r"H:\\Media Overall\\Movies")
    MUSIC_DIRECTORY = os.getenv("MUSIC_DIRECTORY", os.path.expanduser("~/Music"))
    
    # Smart Device Future Support
    ENABLE_SMART_DEVICES = bool(int(os.getenv("ENABLE_SMART_DEVICES", 0)))  # Disabled by default
    
    # Reinforcement Learning Configuration
    LEARNING_MODEL_FILE = os.getenv("LEARNING_MODEL_FILE", "learning_model.json")
    
    @classmethod
    def display_config(cls):
        """Displays current configuration settings."""
        config_vars = {attr: getattr(cls, attr) for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("__")}
        for key, value in config_vars.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    print("🔧 AVSAIS Configuration Settings:")
    Config.display_config()
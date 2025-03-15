import os
import requests
import json
import time
import threading
from dotenv import load_dotenv
import subprocess
from datetime import datetime
import pyttsx3
import re
from email_manager import GmailManager

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY = "Marble Falls"  # Default city, can be changed
UNIT = "imperial"  # Set to 'imperial' for Fahrenheit
LOG_FILE = "weather_log.json"
ALERT_THRESHOLD = {"wind_speed": 50, "low_temp": 10, "high_temp": 110}

class WeatherMonitor:
    def __init__(self, city=CITY, unit=UNIT, check_interval=900):  # Default check every 15 minutes
        self.city = city
        self.unit = unit
        self.api_key = API_KEY
        self.check_interval = check_interval
        self.weather_log = self.load_weather_log()
        self.tts = pyttsx3.init()
        self.gmail = GmailManager()
    
    def get_weather(self):
        """Fetches weather data from OpenWeather API."""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&units={self.unit}&appid={self.api_key}"
        response = requests.get(url)
        if response.status_code != 200:
            return {"error": "Failed to retrieve weather data."}
        return response.json()
    
    def parse_weather(self, weather_data):
        """Extracts relevant weather details."""
        if "error" in weather_data:
            return weather_data["error"], False
        
        description = weather_data["weather"][0]["description"].capitalize()
        temperature = weather_data["main"]["temp"]
        wind_speed = weather_data["wind"]["speed"]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        weather_entry = {
            "timestamp": timestamp,
            "description": description,
            "temperature": temperature,
            "wind_speed": wind_speed
        }
        self.log_weather_data(weather_entry)
        
        alert_message = f"[{timestamp}] Weather Alert: {description}, Temp: {temperature}°F, Wind: {wind_speed} mph."
        return alert_message, self.check_severe_weather(wind_speed, temperature)
    
    def check_severe_weather(self, wind_speed, temp):
        """Determines if weather conditions are severe enough for shutdown."""
        if wind_speed >= ALERT_THRESHOLD["wind_speed"] or temp <= ALERT_THRESHOLD["low_temp"] or temp >= ALERT_THRESHOLD["high_temp"]:
            return True
        return False
    
    def alert_user(self, message, severe=False):
        """Displays alerts, logs warnings, and provides voice and email alerts."""
        print(message)  # Print to console
        self.speak(message)
        self.log_weather_data({"alert": message})
        
        if severe:
            shutdown_warning = "Severe weather detected! System will shut down in 1 minute unless canceled."
            print(shutdown_warning)
            self.speak(shutdown_warning)
            self.log_weather_data({"alert": shutdown_warning})
            self.gmail.send_email("your_email@gmail.com", "Severe Weather Alert", shutdown_warning)
            
            for i in range(60):  # Give the user 60 seconds to cancel
                time.sleep(1)
                response = input("Type 'cancel' to stop shutdown: ").strip().lower()
                if response == "cancel":
                    print("Shutdown canceled.")
                    self.speak("Shutdown canceled.")
                    return
            
            self.shutdown_system()
    
    def shutdown_system(self):
        """Shuts down the system."""
        shutdown_message = "System shutting down due to severe weather."
        print(shutdown_message)
        self.speak(shutdown_message)
        self.log_weather_data({"alert": shutdown_message})
        
        if os.name == "nt":  # Windows
            subprocess.run("shutdown /s /t 0", shell=True)
        else:  # Linux/macOS
            subprocess.run("shutdown -h now", shell=True)
    
    def speak(self, message):
        """Speaks the alert message aloud."""
        self.tts.say(message)
        self.tts.runAndWait()
    
    def log_weather_data(self, entry):
        """Logs weather data and alerts into a JSON file."""
        self.weather_log.append(entry)
        with open(LOG_FILE, "w") as f:
            json.dump(self.weather_log, f, indent=4)
    
    def load_weather_log(self):
        """Loads existing weather log or creates a new one."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []
    
    def monitor_weather(self):
        """Continuously checks weather conditions in the background."""
        def check_loop():
            while True:
                weather_data = self.get_weather()
                message, severe = self.parse_weather(weather_data)
                self.alert_user(message, severe)
                time.sleep(self.check_interval)
        
        thread = threading.Thread(target=check_loop, daemon=True)
        thread.start()
    
if __name__ == "__main__":
    weather_monitor = WeatherMonitor()
    weather_monitor.monitor_weather()
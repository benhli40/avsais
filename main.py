# Entry point for the AI System
import tkinter as tk
from tkinter import ttk
import threading
import time
import psutil
import random
from speech_recognition import SpeechRecognizer
from modules.nlp.text_to_speech import TextToSpeech
from modules.system.system_monitor import SystemMonitor
from modules.automation.weather import WeatherMonitor
from modules.entertainment.play_music import play_music
from modules.entertainment.stop_music import stop_music
from modules.entertainment.play_movie import play_movie
from modules.entertainment.stop_movie import stop_movie
from modules.entertainment.launch_game import launch_game
from modules.entertainment.close_game import close_game
from modules.automation.reminders import ReminderSystem
from modules.automation.daily_diary import DailyDiary
from modules.automation.email_manager import GmailManager
from settings import load_settings

class AVSAISGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AVSAIS - AI Assistant")
        self.root.geometry("800x600")
        
        self.settings = load_settings()
        self.speech_recognizer = SpeechRecognizer()
        self.tts = TextToSpeech()
        self.system_monitor = SystemMonitor()
        self.weather_monitor = WeatherMonitor()
        self.reminders = ReminderSystem()
        self.diary = DailyDiary()
        self.email_manager = GmailManager()
        
        self.create_ui()
        self.update_system_stats()
        self.start_listening()
        
    def create_ui(self):
        """Creates the main GUI layout."""
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # System Stats Panel
        self.stats_label = ttk.Label(self.main_frame, text="System Stats: Loading...", font=("Arial", 12))
        self.stats_label.pack(pady=5)
        
        # Weather Panel
        self.weather_label = ttk.Label(self.main_frame, text="Weather: Checking...", font=("Arial", 12))
        self.weather_label.pack(pady=5)
        
        # Command Panel
        self.command_entry = ttk.Entry(self.main_frame, font=("Arial", 12), width=50)
        self.command_entry.pack(pady=10)
        self.command_entry.bind("<Return>", self.process_command)
        
        self.execute_button = ttk.Button(self.main_frame, text="Execute", command=self.process_command)
        self.execute_button.pack()
        
    def update_system_stats(self):
        """Updates system stats in the GUI."""
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        
        self.stats_label.config(text=f"CPU: {cpu_usage}% | RAM: {ram_usage}% | Disk: {disk_usage}%")
        
        # Update weather
        weather_data = self.weather_monitor.get_weather()
        self.weather_label.config(text=f"Weather: {weather_data}")
        
        self.root.after(5000, self.update_system_stats)  # Refresh every 5 seconds
        
    def process_command(self, event=None):
        """Processes user commands from the text entry."""
        command = self.command_entry.get().strip().lower()
        self.command_entry.delete(0, tk.END)
        
        if "play music" in command:
            play_music()
        elif "stop music" in command:
            stop_music()
        elif "play movie" in command:
            play_movie()
        elif "stop movie" in command:
            stop_movie()
        elif "launch game" in command:
            launch_game()
        elif "close game" in command:
            close_game()
        elif "set reminder" in command:
            self.reminders.set_reminder(command)
        elif "write diary" in command:
            self.diary.write_entry(command)
        elif "check email" in command:
            self.email_manager.check_inbox()
        elif "weather" in command:
            self.weather_label.config(text=f"Weather: {self.weather_monitor.get_weather()}")
        else:
            self.tts.speak("I'm not sure how to handle that command yet.")
        
    def start_listening(self):
        """Runs the speech recognition in a background thread."""
        threading.Thread(target=self.listen_for_commands, daemon=True).start()
        
    def listen_for_commands(self):
        """Continuously listens for voice commands."""
        while True:
            response = self.speech_recognizer.recognize_speech()
            if response:
                self.command_entry.insert(0, response)
                self.process_command()
            time.sleep(1)  # Prevent excessive CPU usage

if __name__ == "__main__":
    root = tk.Tk()
    app = AVSAISGUI(root)
    root.mainloop()
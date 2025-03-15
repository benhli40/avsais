import time
import json
import os
import threading
from datetime import datetime, timedelta
import pyttsx3
import re
from email_manager import GmailManager

class ReminderManager:
    def __init__(self, reminder_file="reminders.json"):
        self.reminder_file = reminder_file
        self.reminders = self.load_reminders()
        self.tts = pyttsx3.init()
        self.gmail = GmailManager()
    
    def load_reminders(self):
        if os.path.exists(self.reminder_file):
            with open(self.reminder_file, "r") as f:
                return json.load(f)
        return []
    
    def save_reminders(self):
        with open(self.reminder_file, "w") as f:
            json.dump(self.reminders, f, indent=4)
    
    def parse_time_input(self, time_input):
        """Converts natural language time inputs into a timestamp."""
        now = datetime.now()
        match = re.match(r"in (\d+) (minutes|hours|days|weeks|months)", time_input)
        if match:
            value, unit = int(match.group(1)), match.group(2)
            if unit == "minutes":
                return (now + timedelta(minutes=value)).strftime("%Y-%m-%d %H:%M")
            elif unit == "hours":
                return (now + timedelta(hours=value)).strftime("%Y-%m-%d %H:%M")
            elif unit == "days":
                return (now + timedelta(days=value)).strftime("%Y-%m-%d %H:%M")
            elif unit == "weeks":
                return (now + timedelta(weeks=value)).strftime("%Y-%m-%d %H:%M")
            elif unit == "months":
                return (now + timedelta(weeks=value * 4)).strftime("%Y-%m-%d %H:%M")
        return time_input  # Assume direct timestamp input
    
    def add_reminder(self, message, reminder_time, priority="normal", recurring=None, email_alert=False):
        """
        Adds a new reminder with a message, scheduled time, priority, and optional recurring setting.
        """
        reminder_time = self.parse_time_input(reminder_time)
        self.reminders.append({
            "message": message,
            "time": reminder_time,
            "priority": priority,
            "recurring": recurring,
            "email_alert": email_alert
        })
        self.save_reminders()
        return f"Reminder set for {reminder_time}: {message} (Priority: {priority})"
    
    def check_reminders(self):
        """
        Checks if any reminders are due and processes them accordingly.
        """
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        triggered = [r for r in self.reminders if r["time"] == current_time]
        
        if triggered:
            remaining_reminders = []
            for reminder in self.reminders:
                if reminder in triggered:
                    print(f"Reminder: {reminder['message']}")
                    self.speak(f"Reminder: {reminder['message']}")
                    
                    # Repeat high-priority reminders twice
                    if reminder["priority"] == "high":
                        self.speak(f"Reminder: {reminder['message']}, repeating due to high priority.")
                    
                    # Send email alert if enabled
                    if reminder["email_alert"]:
                        self.gmail.send_email("your_email@gmail.com", "Reminder Alert", reminder["message"])
                    
                    # Handle recurring reminders
                    if reminder["recurring"]:
                        next_time = datetime.strptime(reminder["time"], "%Y-%m-%d %H:%M")
                        if reminder["recurring"] == "daily":
                            next_time += timedelta(days=1)
                        elif reminder["recurring"] == "weekly":
                            next_time += timedelta(weeks=1)
                        elif reminder["recurring"] == "monthly":
                            next_time += timedelta(weeks=4)
                        reminder["time"] = next_time.strftime("%Y-%m-%d %H:%M")
                        remaining_reminders.append(reminder)
                else:
                    remaining_reminders.append(reminder)
            
            self.reminders = remaining_reminders
            self.save_reminders()
    
    def speak(self, message):
        """Speaks the reminder message aloud."""
        self.tts.say(message)
        self.tts.runAndWait()
    
    def start_reminder_checker(self, interval=60):
        """
        Starts a background thread to continuously check reminders at the given interval.
        """
        def check_loop():
            while True:
                self.check_reminders()
                time.sleep(interval)
        
        thread = threading.Thread(target=check_loop, daemon=True)
        thread.start()
    
if __name__ == "__main__":
    reminder_manager = ReminderManager()
    reminder_manager.start_reminder_checker()
    
    # Example: Adding reminders
    print(reminder_manager.add_reminder("Meeting with Alex", "in 30 minutes", priority="high", email_alert=True))
    print(reminder_manager.add_reminder("Doctor's appointment", "in 2 days", recurring="daily"))
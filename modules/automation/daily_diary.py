import json
import os
import speech_recognition as sr
from datetime import datetime
from email_manager import GmailManager

class DailyDiary:
    def __init__(self, diary_file="daily_diary.json"):
        self.diary_file = diary_file
        self.entries = self.load_entries()
        self.gmail = GmailManager()
        self.recognizer = sr.Recognizer()
    
    def load_entries(self):
        if os.path.exists(self.diary_file):
            with open(self.diary_file, "r") as f:
                return json.load(f)
        return {}
    
    def save_entries(self):
        with open(self.diary_file, "w") as f:
            json.dump(self.entries, f, indent=4)
    
    def add_entry(self, content):
        """
        Adds a new diary entry for the current date.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        if date_str not in self.entries:
            self.entries[date_str] = []
        self.entries[date_str].append(content)
        self.save_entries()
        return f"Diary entry added for {date_str}."
    
    def get_entries(self, date=None):
        """
        Retrieves diary entries for a specific date or the most recent date.
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        return self.entries.get(date, ["No entries found for this date."])
    
    def send_diary_to_email(self, recipient_email):
        """
        Sends the latest diary entry to the specified email address.
        """
        date_str = datetime.now().strftime("%Y-%m-%d")
        if date_str not in self.entries:
            return "No entries found for today to send."
        
        subject = f"Daily Diary Entry - {date_str}"
        body = "\n".join(self.entries[date_str])
        
        return self.gmail.send_email(recipient_email, subject, body)
    
    def record_voice_entry(self):
        """Records a diary entry using speech-to-text."""
        with sr.Microphone() as source:
            print("Recording diary entry... Speak now!")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized: {text}")
                return self.add_entry(text)
            except sr.UnknownValueError:
                return "Sorry, I couldn't understand that. Try again."
            except sr.RequestError:
                return "Speech recognition service is unavailable."
            except sr.WaitTimeoutError:
                return "No speech detected. Please try again."
    
if __name__ == "__main__":
    diary = DailyDiary()
    
    # Example: Adding an entry
    print(diary.add_entry("Today was a productive day. I made great progress on my AI system!"))
    print(diary.add_entry("Feeling good about how things are coming together."))
    
    # Example: Recording a voice entry
    print(diary.record_voice_entry())
    
    # Example: Retrieving today's diary entries
    print("Today's Entries:", diary.get_entries())
    
    # Example: Sending the diary entry to email
    print(diary.send_diary_to_email("benhli40@gmail.com"))
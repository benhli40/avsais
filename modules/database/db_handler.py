# Database interface
import sqlite3
import os

DB_FILE = "avsais_database.db"

class DBHandler:
    def __init__(self):
        """Initializes the database connection and creates necessary tables."""
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Creates necessary tables if they don't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                timestamp TEXT,
                                user_input TEXT,
                                ai_response TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                reminder_text TEXT,
                                remind_at TEXT)''')
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS system_logs (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                log_message TEXT,
                                log_time TEXT)''')
        
        self.conn.commit()
    
    def log_conversation(self, user_input, ai_response):
        """Logs a conversation entry into the database."""
        self.cursor.execute("INSERT INTO conversations (timestamp, user_input, ai_response) VALUES (datetime('now'), ?, ?)",
                            (user_input, ai_response))
        self.conn.commit()
    
    def retrieve_conversations(self, keyword=None, date=None):
        """Retrieves conversations based on keyword or date."""
        query = "SELECT timestamp, user_input, ai_response FROM conversations WHERE 1=1"
        params = []
        
        if keyword:
            query += " AND (user_input LIKE ? OR ai_response LIKE ?)"
            params.extend((f"%{keyword}%", f"%{keyword}%"))
        
        if date:
            query += " AND timestamp LIKE ?"
            params.append(f"{date}%")
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def add_reminder(self, reminder_text, remind_at):
        """Adds a new reminder entry."""
        self.cursor.execute("INSERT INTO reminders (reminder_text, remind_at) VALUES (?, ?)", (reminder_text, remind_at))
        self.conn.commit()
    
    def fetch_reminders(self):
        """Fetches all reminders from the database."""
        self.cursor.execute("SELECT * FROM reminders")
        return self.cursor.fetchall()
    
    def log_system_event(self, message):
        """Logs system events into the database."""
        self.cursor.execute("INSERT INTO system_logs (log_message, log_time) VALUES (?, datetime('now'))", (message,))
        self.conn.commit()
    
    def fetch_system_logs(self):
        """Retrieves system logs."""
        self.cursor.execute("SELECT * FROM system_logs")
        return self.cursor.fetchall()
    
    def close_connection(self):
        """Closes the database connection."""
        self.conn.close()

if __name__ == "__main__":
    db = DBHandler()
    
    # Example usage
    db.log_conversation("Hello!", "Hi there! How can I help?")
    db.add_reminder("Doctor's appointment", "2025-04-01 10:00:00")
    db.log_system_event("System started successfully")
    
    print("🗂️ Conversations:", db.retrieve_conversations())
    print("🔔 Reminders:", db.fetch_reminders())
    print("📜 System Logs:", db.fetch_system_logs())
    
    db.close_connection()
import json
import os
from datetime import datetime

LOG_FILE = "system_event_log.json"

class SystemLogger:
    def __init__(self):
        self.log_data = self.load_log()
    
    def load_log(self):
        """Loads existing system event log or creates a new one."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []
    
    def log_event(self, event_type, message):
        """Logs an event with a timestamp."""
        event_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "message": message
        }
        self.log_data.append(event_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(self.log_data, f, indent=4)
    
    def get_recent_logs(self, last_n=10):
        """Retrieves the last N log entries."""
        return self.log_data[-last_n:]
    
    def clear_logs(self):
        """Clears the log file."""
        self.log_data = []
        with open(LOG_FILE, "w") as f:
            json.dump(self.log_data, f, indent=4)
        print("System logs cleared.")
    
if __name__ == "__main__":
    logger = SystemLogger()
    
    # Example logs
    logger.log_event("INFO", "System started successfully.")
    logger.log_event("WARNING", "High CPU usage detected.")
    logger.log_event("ERROR", "Application crashed unexpectedly.")
    
    print("Recent Logs:", logger.get_recent_logs())

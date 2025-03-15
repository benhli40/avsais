import json
import os
from datetime import datetime, timedelta

LOG_FILES = [
    "system_event_log.json",
    "system_monitor_log.json",
    "disk_usage_log.json",
    "network_monitor_log.json",
    "process_monitor_log.json"
]
LOG_RETENTION_DAYS = 30  # Auto-delete logs older than 30 days

class LogManager:
    def __init__(self):
        self.cleanup_logs()
    
    def cleanup_logs(self):
        """Removes log entries older than the retention period."""
        for log_file in LOG_FILES:
            if os.path.exists(log_file):
                with open(log_file, "r") as f:
                    try:
                        log_data = json.load(f)
                    except json.JSONDecodeError:
                        log_data = []
                
                new_log_data = [entry for entry in log_data if self.is_recent(entry)]
                
                with open(log_file, "w") as f:
                    json.dump(new_log_data, f, indent=4)
                
                print(f"✅ Cleaned {log_file}: {len(log_data) - len(new_log_data)} old entries removed.")
    
    def is_recent(self, log_entry):
        """Checks if a log entry is within the retention period."""
        try:
            log_time = datetime.strptime(log_entry["timestamp"], "%Y-%m-%d %H:%M:%S")
            return log_time >= datetime.now() - timedelta(days=LOG_RETENTION_DAYS)
        except (KeyError, ValueError):
            return True  # Keep malformed or incorrectly formatted logs
    
if __name__ == "__main__":
    log_manager = LogManager()
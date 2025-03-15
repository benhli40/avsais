import psutil
import json
import os
import time
import threading
from datetime import datetime
import pyttsx3

LOG_FILE = "disk_usage_log.json"
ALERT_THRESHOLD = {"disk": 90}  # Alert when disk usage exceeds 90%

class DiskUsageMonitor:
    def __init__(self, check_interval=300):  # Default check every 5 minutes
        self.check_interval = check_interval
        self.disk_log = self.load_disk_log()
        self.tts = pyttsx3.init()
    
    def get_disk_usage(self):
        """Retrieves disk usage statistics."""
        partitions = psutil.disk_partitions()
        usage_stats = {}
        
        for partition in partitions:
            if os.name == "nt" and 'cdrom' in partition.opts:
                continue  # Skip CD-ROM drives on Windows
            usage = psutil.disk_usage(partition.mountpoint)
            usage_stats[partition.device] = {
                "total": usage.total // (1024**3),  # Convert bytes to GB
                "used": usage.used // (1024**3),
                "free": usage.free // (1024**3),
                "percent": usage.percent
            }
        return usage_stats
    
    def log_disk_usage(self):
        """Logs disk usage stats into a JSON file."""
        stats = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "disk_usage": self.get_disk_usage()
        }
        self.disk_log.append(stats)
        with open(LOG_FILE, "w") as f:
            json.dump(self.disk_log, f, indent=4)
        
        self.check_alerts(stats["disk_usage"])
        return stats
    
    def load_disk_log(self):
        """Loads existing disk usage log or creates a new one."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []
    
    def check_alerts(self, disk_usage):
        """Checks if disk usage exceeds the threshold and gives alerts."""
        alerts = []
        
        for device, usage in disk_usage.items():
            if usage["percent"] >= ALERT_THRESHOLD["disk"]:
                alerts.append(f"⚠️ High Disk Usage on {device}: {usage['percent']}% - Consider cleaning up storage or upgrading.")
        
        if alerts:
            self.speak_alert("\n".join(alerts))
            self.log_alerts(alerts)
    
    def speak_alert(self, message):
        """Speaks alerts aloud using text-to-speech."""
        self.tts.say(message)
        self.tts.runAndWait()
    
    def log_alerts(self, alerts):
        """Logs alerts into the system log file."""
        alert_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "alerts": alerts
        }
        self.disk_log.append(alert_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(self.disk_log, f, indent=4)
    
    def monitor_disk_usage(self):
        """Continuously checks disk health in the background."""
        def check_loop():
            while True:
                stats = self.log_disk_usage()
                print(f"Logged Disk Stats: {stats}")
                time.sleep(self.check_interval)
        
        thread = threading.Thread(target=check_loop, daemon=True)
        thread.start()
    
if __name__ == "__main__":
    disk_monitor = DiskUsageMonitor()
    disk_monitor.monitor_disk_usage()
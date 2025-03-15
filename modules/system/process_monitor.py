import psutil
import json
import time
import os
import threading
from datetime import datetime
import pyttsx3

LOG_FILE = "process_monitor_log.json"
ALERT_THRESHOLD = {"cpu": 50, "ram": 500}  # CPU usage in %, RAM usage in MB

class ProcessMonitor:
    def __init__(self, check_interval=300):  # Check every 5 minutes
        self.check_interval = check_interval
        self.process_log = self.load_process_log()
        self.tts = pyttsx3.init()
    
    def get_running_processes(self):
        """Retrieves the list of currently running processes with their CPU and RAM usage."""
        processes = []
        for process in psutil.process_iter(attrs=["pid", "name", "cpu_percent", "memory_info"]):
            try:
                process_info = process.info
                processes.append({
                    "pid": process_info["pid"],
                    "name": process_info["name"],
                    "cpu_usage": process_info["cpu_percent"],
                    "ram_usage": process_info["memory_info"].rss // (1024**2)  # Convert bytes to MB
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        return processes
    
    def log_processes(self):
        """Logs running processes into a JSON file."""
        stats = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processes": self.get_running_processes()
        }
        self.process_log.append(stats)
        with open(LOG_FILE, "w") as f:
            json.dump(self.process_log, f, indent=4)
        
        self.check_alerts(stats["processes"])
        return stats
    
    def load_process_log(self):
        """Loads existing process log or creates a new one."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []
    
    def check_alerts(self, processes):
        """Checks if any process is using too much CPU or RAM and alerts the user."""
        alerts = []
        
        for process in processes:
            if process["cpu_usage"] >= ALERT_THRESHOLD["cpu"]:
                alerts.append(f"⚠️ High CPU Usage: {process['name']} (PID {process['pid']}) is using {process['cpu_usage']}% CPU.")
            if process["ram_usage"] >= ALERT_THRESHOLD["ram"]:
                alerts.append(f"⚠️ High RAM Usage: {process['name']} (PID {process['pid']}) is using {process['ram_usage']}MB RAM.")
        
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
        self.process_log.append(alert_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(self.process_log, f, indent=4)
    
    def monitor_processes(self):
        """Continuously checks system processes in the background."""
        def check_loop():
            while True:
                stats = self.log_processes()
                print(f"Logged Process Stats: {stats}")
                time.sleep(self.check_interval)
        
        thread = threading.Thread(target=check_loop, daemon=True)
        thread.start()
    
if __name__ == "__main__":
    process_monitor = ProcessMonitor()
    process_monitor.monitor_processes()
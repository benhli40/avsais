import psutil
import json
import time
import threading
from datetime import datetime
import os
import pyttsx3

LOG_FILE = "system_monitor_log.json"
ALERT_THRESHOLD = {"cpu": 90, "ram": 90, "disk": 95, "gpu": 90}

class SystemMonitor:
    def __init__(self, check_interval=60):  # Check every 60 seconds
        self.check_interval = check_interval
        self.monitor_log = self.load_monitor_log()
        self.tts = pyttsx3.init()
    
    def get_system_stats(self):
        """Retrieves system statistics including CPU, RAM, and disk usage."""
        stats = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cpu_usage": psutil.cpu_percent(interval=1),
            "ram_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "gpu_usage": self.get_gpu_usage(),
            "uptime": self.get_system_uptime()
        }
        return stats
    
    def get_gpu_usage(self):
        """Attempts to get GPU usage if available."""
        try:
            import GPUtil
            gpus = GPUtil.getGPUs()
            return {gpu.name: gpu.load * 100 for gpu in gpus} if gpus else "No GPU detected"
        except ImportError:
            return "GPU monitoring not available (GPUtil missing)"
    
    def get_system_uptime(self):
        """Returns system uptime in hours and minutes."""
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_hours = uptime_seconds // 3600
        uptime_minutes = (uptime_seconds % 3600) // 60
        return f"{int(uptime_hours)}h {int(uptime_minutes)}m"
    
    def log_system_stats(self):
        """Logs system stats into a JSON file for later review."""
        stats = self.get_system_stats()
        self.monitor_log.append(stats)
        with open(LOG_FILE, "w") as f:
            json.dump(self.monitor_log, f, indent=4)
        
        # Check for system issues and suggest improvements
        self.check_alerts(stats)
        return stats
    
    def load_monitor_log(self):
        """Loads existing system monitoring log or creates a new one."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []
    
    def check_alerts(self, stats):
        """Checks if any system component exceeds safe thresholds and suggests upgrades."""
        alerts = []
        suggestions = []

        if stats["cpu_usage"] >= ALERT_THRESHOLD["cpu"]:
            alerts.append(f"⚠️ High CPU Usage: {stats['cpu_usage']}% - Consider upgrading your CPU.")
        if stats["ram_usage"] >= ALERT_THRESHOLD["ram"]:
            alerts.append(f"⚠️ High RAM Usage: {stats['ram_usage']}% - Adding more RAM could improve performance.")
        if stats["disk_usage"] >= ALERT_THRESHOLD["disk"]:
            alerts.append(f"⚠️ Low Disk Space: {stats['disk_usage']}% used - Consider upgrading storage or cleaning up files.")
        
        if isinstance(stats["gpu_usage"], dict):
            for gpu, usage in stats["gpu_usage"].items():
                if usage >= ALERT_THRESHOLD["gpu"]:
                    alerts.append(f"⚠️ High GPU Usage: {gpu} at {usage}% - A better cooling system might be needed.")
                
                # Check if GPU, CPU, and RAM are not well balanced
                if usage > 85 and stats["cpu_usage"] < 50 and stats["ram_usage"] > 80:
                    suggestions.append("🔍 Your GPU is under heavy load while your CPU is underutilized. Consider upgrading to a more balanced system.")
        
        if alerts:
            self.speak_alert("\n".join(alerts))
            self.log_alerts(alerts)
        if suggestions:
            self.log_alerts(suggestions)
    
    def speak_alert(self, message):
        """Speaks alerts aloud using text-to-speech."""
        self.tts.say(message)
        self.tts.runAndWait()
    
    def log_alerts(self, alerts):
        """Logs alerts and upgrade suggestions into the system log file."""
        alert_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "alerts": alerts
        }
        self.monitor_log.append(alert_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(self.monitor_log, f, indent=4)
    
    def monitor_system(self):
        """Continuously checks system health in the background."""
        def check_loop():
            while True:
                stats = self.log_system_stats()
                print(f"Logged System Stats: {stats}")
                time.sleep(self.check_interval)
        
        thread = threading.Thread(target=check_loop, daemon=True)
        thread.start()
    
if __name__ == "__main__":
    system_monitor = SystemMonitor()
    system_monitor.monitor_system()
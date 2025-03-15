import psutil
import json
import time
import threading
import os
import speedtest
from datetime import datetime
import pyttsx3

LOG_FILE = "network_monitor_log.json"
ALERT_THRESHOLD = {"download_speed": 10, "upload_speed": 2, "ping": 100}  # Speeds in Mbps, ping in ms

class NetworkMonitor:
    def __init__(self, check_interval=300):  # Check every 5 minutes
        self.check_interval = check_interval
        self.network_log = self.load_network_log()
        self.tts = pyttsx3.init()
    
    def get_network_stats(self):
        """Measures download speed, upload speed, and ping."""
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            ping = st.results.ping
        except Exception as e:
            return {"error": f"Network test failed: {e}"}
        
        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "download_speed": round(download_speed, 2),
            "upload_speed": round(upload_speed, 2),
            "ping": round(ping, 2)
        }
    
    def log_network_stats(self):
        """Logs network speed test results into a JSON file."""
        stats = self.get_network_stats()
        if "error" in stats:
            print(stats["error"])
            return stats
        
        self.network_log.append(stats)
        with open(LOG_FILE, "w") as f:
            json.dump(self.network_log, f, indent=4)
        
        self.check_alerts(stats)
        return stats
    
    def load_network_log(self):
        """Loads existing network log or creates a new one."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        return []
    
    def check_alerts(self, stats):
        """Checks if network performance is below thresholds and alerts the user."""
        alerts = []
        
        if stats["download_speed"] < ALERT_THRESHOLD["download_speed"]:
            alerts.append(f"⚠️ Low Download Speed: {stats['download_speed']} Mbps - Check your internet connection.")
        if stats["upload_speed"] < ALERT_THRESHOLD["upload_speed"]:
            alerts.append(f"⚠️ Low Upload Speed: {stats['upload_speed']} Mbps - This may affect video calls or uploads.")
        if stats["ping"] > ALERT_THRESHOLD["ping"]:
            alerts.append(f"⚠️ High Ping: {stats['ping']} ms - You may experience lag or latency issues.")
        
        if alerts:
            self.speak_alert("\n".join(alerts))
            self.log_alerts(alerts)
    
    def speak_alert(self, message):
        """Speaks alerts aloud using text-to-speech."""
        self.tts.say(message)
        self.tts.runAndWait()
    
    def log_alerts(self, alerts):
        """Logs network alerts into the system log file."""
        alert_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "alerts": alerts
        }
        self.network_log.append(alert_entry)
        with open(LOG_FILE, "w") as f:
            json.dump(self.network_log, f, indent=4)
    
    def monitor_network(self):
        """Continuously checks network performance in the background."""
        def check_loop():
            while True:
                stats = self.log_network_stats()
                print(f"Logged Network Stats: {stats}")
                time.sleep(self.check_interval)
        
        thread = threading.Thread(target=check_loop, daemon=True)
        thread.start()
    
if __name__ == "__main__":
    network_monitor = NetworkMonitor()
    network_monitor.monitor_network()
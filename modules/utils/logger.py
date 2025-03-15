# Logging utility
import logging
import os
from helper_functions import get_current_timestamp, ensure_directory_exists

LOG_DIRECTORY = "logs"
LOG_FILE = os.path.join(LOG_DIRECTORY, "avsais.log")

# Ensure log directory exists
ensure_directory_exists(LOG_DIRECTORY)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_info(message):
    """Logs an informational message."""
    logging.info(message)
    print(f"[INFO] {get_current_timestamp()} - {message}")

def log_warning(message):
    """Logs a warning message."""
    logging.warning(message)
    print(f"[WARNING] {get_current_timestamp()} - {message}")

def log_error(message):
    """Logs an error message."""
    logging.error(message)
    print(f"[ERROR] {get_current_timestamp()} - {message}")

def get_logs():
    """Retrieves the log file contents."""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return f.readlines()
    return ["No logs available."]

if __name__ == "__main__":
    log_info("AVSAIS Logger initialized.")
    log_warning("This is a test warning.")
    log_error("This is a test error.")
    
    print("📜 Log Contents:")
    for log in get_logs():
        print(log.strip())
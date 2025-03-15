# Stops movie playback
import psutil
import os
import signal

def get_running_movies():
    """Gets a list of currently running movie players."""
    media_players = ["vlc.exe", "mpv.exe", "mplayer.exe", "wmplayer.exe", "potplayer.exe", "kmplayer.exe", "quicktimeplayer.exe"]
    running_players = []
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'].lower() in media_players:
            running_players.append(process.info)
    return running_players

def stop_movie():
    """Attempts to stop a running movie player."""
    running_players = get_running_movies()
    if not running_players:
        print("❌ No running movie players detected.")
        return
    
    for player in running_players:
        try:
            os.kill(player['pid'], signal.SIGTERM)
            print(f"✅ Successfully stopped {player['name']}.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print(f"❌ Could not stop {player['name']}. It may require manual intervention.")

if __name__ == "__main__":
    print("🔍 Checking for running movie players...")
    stop_movie()
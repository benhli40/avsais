# Stops music playback
import psutil
import os
import signal

def get_running_music_players():
    """Gets a list of currently running music players."""
    music_players = ["spotify.exe", "wmplayer.exe", "vlc.exe", "itunes.exe", "chrome.exe", "firefox.exe", "brave.exe", "edge.exe"]
    running_players = []
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'].lower() in music_players:
            running_players.append(process.info)
    return running_players

def stop_music():
    """Attempts to stop a running music player."""
    running_players = get_running_music_players()
    if not running_players:
        print("❌ No running music players detected.")
        return
    
    for player in running_players:
        try:
            os.kill(player['pid'], signal.SIGTERM)
            print(f"✅ Successfully stopped {player['name']}.")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            print(f"❌ Could not stop {player['name']}. It may require manual intervention.")

if __name__ == "__main__":
    print("🔍 Checking for running music players...")
    stop_music()
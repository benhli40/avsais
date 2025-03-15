# Starts music playback
import os
import subprocess
import webbrowser

# Define available music sources
SPOTIFY_APP_PATH = r"C:\Program Files\Spotify\Spotify.exe"
SPOTIFY_WEB_URL = "https://open.spotify.com"
PANDORA_URL = "https://www.pandora.com"
MUSIC_DIRECTORY = os.path.expanduser("~/Music")

def list_local_music():
    """Lists all available local music files."""
    if not os.path.exists(MUSIC_DIRECTORY):
        print("❌ Local music directory not found.")
        return []
    return [f for f in os.listdir(MUSIC_DIRECTORY) if f.endswith((".mp3", ".wav", ".flac", ".aac"))]

def play_music_local(song_name):
    """Plays a selected local music file using the default player."""
    song_path = os.path.join(MUSIC_DIRECTORY, song_name)
    if os.path.exists(song_path):
        print(f"🎵 Playing: {song_name}")
        subprocess.Popen([song_path], shell=True)
    else:
        print("❌ Song not found.")

def play_music_spotify():
    """Opens Spotify (App if installed, otherwise web player)."""
    if os.path.exists(SPOTIFY_APP_PATH):
        print("🎵 Opening Spotify App...")
        subprocess.Popen([SPOTIFY_APP_PATH])
    else:
        print("🌐 Opening Spotify Web Player...")
        webbrowser.open(SPOTIFY_WEB_URL)

def play_music_pandora():
    """Opens Pandora Web Player."""
    print("🌐 Opening Pandora...")
    webbrowser.open(PANDORA_URL)

if __name__ == "__main__":
    print("🎶 Where would you like to play music?")
    print("1. Local Music Files")
    print("2. Spotify")
    print("3. Pandora")
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        print("📂 Available Local Music:")
        songs = list_local_music()
        if songs:
            for song in songs:
                print(f"- {song}")
            selected_song = input("Enter the song name to play: ")
            play_music_local(selected_song)
        else:
            print("❌ No music files found in directory.")
    elif choice == "2":
        play_music_spotify()
    elif choice == "3":
        play_music_pandora()
    else:
        print("❌ Invalid choice.")
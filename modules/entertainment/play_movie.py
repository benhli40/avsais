# Starts movie playback
import os
import subprocess
import webbrowser

MOVIE_DIRECTORY = r"H:\\Media Overall\\Movies"
STREAMING_SERVICES = {
    "Netflix": "https://www.netflix.com",
    "Paramount+": "https://www.paramountplus.com"
}
PLEX_URL = "http://localhost:32400/web"
EMBY_URL = "http://localhost:8096"

def list_movies():
    """Lists all available movie files in the directory."""
    if not os.path.exists(MOVIE_DIRECTORY):
        print("❌ Movie directory not found.")
        return []
    return [f for f in os.listdir(MOVIE_DIRECTORY) if f.endswith((".mp4", ".mkv", ".avi", ".mov", ".wmv"))]

def play_movie_local(movie_name):
    """Plays the selected movie using the default media player."""
    movie_path = os.path.join(MOVIE_DIRECTORY, movie_name)
    if os.path.exists(movie_path):
        print(f"🎬 Playing locally: {movie_name}")
        subprocess.Popen([movie_path], shell=True)
    else:
        print("❌ Movie not found.")

def play_movie_streaming(service):
    """Opens the selected streaming service in a browser."""
    if service in STREAMING_SERVICES:
        print(f"🌐 Opening {service}...")
        webbrowser.open(STREAMING_SERVICES[service])
    else:
        print("❌ Streaming service not supported.")

def play_movie_server(server):
    """Opens Plex or Emby in a browser."""
    if server == "Plex":
        print("🎥 Opening Plex...")
        webbrowser.open(PLEX_URL)
    elif server == "Emby":
        print("🎥 Opening Emby...")
        webbrowser.open(EMBY_URL)
    else:
        print("❌ Media server not recognized.")

if __name__ == "__main__":
    print("📽️ Where would you like to play a movie?")
    print("1. Local files")
    print("2. Netflix")
    print("3. Paramount+")
    print("4. Plex")
    print("5. Emby")
    choice = input("Enter your choice (1-5): ")
    
    if choice == "1":
        print("📂 Available Movies:")
        movies = list_movies()
        if movies:
            for movie in movies:
                print(f"- {movie}")
            selected_movie = input("Enter the movie name to play: ")
            play_movie_local(selected_movie)
        else:
            print("❌ No movies found in directory.")
    elif choice == "2":
        play_movie_streaming("Netflix")
    elif choice == "3":
        play_movie_streaming("Paramount+")
    elif choice == "4":
        play_movie_server("Plex")
    elif choice == "5":
        play_movie_server("Emby")
    else:
        print("❌ Invalid choice.")
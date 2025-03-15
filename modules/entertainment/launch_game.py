# Launches a game
import os
import json
import subprocess

# Predefined game directories
GAME_DIRECTORIES = [
    r"C:\Program Files\Bluestacks_nxt",
    r"C:\Program Files\EA Games",
    r"C:\Program Files\Electronic Arts",
    r"C:\Program Files\Riot Vanguard",
    r"C:\Riot Games\League of Legends",
    r"C:\Program Files (x86)\Diablo II",
    r"C:\Program Files (x86)\Epic Games",
    r"C:\Program Files (x86)\Need for Speed(TM) Most Wanted",
    r"C:\Program Files (x86)\Plants vs. Zombies",
    r"C:\Program Files (x86)\Simcity",
    r"C:\Program Files (x86)\Syberia II",
    r"C:\Program Files (x86)\The Sims 4",
    r"C:\Program Files (x86)\Wildtangent Games",
    r"C:\Program Files (x86)\Zuma's Revenge",
    r"E:\Eve",
    r"E:\Program Files (x86)\Battle.net\Diablo III",
    r"E:\Program Files (x86)\Battle.net\Diablo Immortal",
    r"E:\Program Files (x86)\Battle.net\Diablo IV",
    r"E:\Program Files (x86)\Battle.net\Hearthstone",
    r"E:\Program Files (x86)\Battle.net\Heroes of the Storm",
    r"E:\Program Files (x86)\Battle.net\Overwatch",
    r"E:\Program Files (x86)\Battle.net\StarCraft II",
    r"E:\Program Files (x86)\Battle.net\World of Warcraft",
    r"E:\Program Files (x86)\Electronic Arts\Bioware\Star Wars - The Old Republic",
    r"E:\Program Files (x86)\Steam"
]

GAMES_DB = "games.json"

def scan_games():
    """Scans predefined directories for executable game files."""
    games = {}
    for directory in GAME_DIRECTORIES:
        if os.path.exists(directory):
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".exe"):
                        game_name = os.path.splitext(file)[0]
                        games[game_name] = os.path.join(root, file)
    with open(GAMES_DB, "w") as f:
        json.dump(games, f, indent=4)
    return games

def load_games():
    """Loads games from the JSON database."""
    if os.path.exists(GAMES_DB):
        with open(GAMES_DB, "r") as f:
            return json.load(f)
    return {}

def launch_game(game_name):
    """Launches a selected game if found."""
    games = load_games()
    if game_name in games:
        print(f"🎮 Launching {game_name}...")
        subprocess.Popen(games[game_name], shell=True)
    else:
        print("❌ Game not found. Try rescanning.")

if __name__ == "__main__":
    print("🔍 Scanning for installed games...")
    game_list = scan_games()
    print(f"✅ Found {len(game_list)} games!")
    print("Enter the name of the game you want to launch:")
    user_choice = input("Game Name: ")
    launch_game(user_choice)
# Closes a running game
import psutil
import os
import signal

def get_running_games():
    """Gets a list of currently running games based on known executables."""
    running_games = []
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['name'].endswith(".exe"):
            running_games.append(process.info)
    return running_games

def close_game(game_name):
    """Attempts to close a running game by name."""
    found = False
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if game_name.lower() in process.info['name'].lower():
            try:
                os.kill(process.info['pid'], signal.SIGTERM)
                print(f"✅ Successfully closed {game_name}.")
                found = True
                break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                print(f"❌ Could not close {game_name}. It may require manual intervention.")
    if not found:
        print(f"⚠️ No running instance of {game_name} found.")

if __name__ == "__main__":
    print("🔍 Checking for running games...")
    running_games = get_running_games()
    if running_games:
        print("🎮 Running Games:")
        for game in running_games:
            print(f"- {game['name']}")
        game_to_close = input("Enter the game name to close: ")
        close_game(game_to_close)
    else:
        print("❌ No running games detected.")
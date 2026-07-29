```gdscript
# File: res://scripts/leaderboard.gd
extends Node

var leaderboard_data = {}
const DATA_FILE_PATH = "user://leaderboard.json"

func _ready():
    load_leaderboard_data()
    update_leaderboard()

func save_leaderboard_data():
    var file = FileAccess.open(DATA_FILE_PATH, FileAccess.WRITE)
    if file:
        file.store_string(to_json(leaderboard_data))
        file.close()

func load_leaderboard_data():
    leaderboard_data = {}
    var file = FileAccess.open(DATA_FILE_PATH, FileAccess.READ)
    if file:
        leaderboard_data = parse_json(file.get_as_text())
        file.close()

func add_player_score(player_id: String, score: int):
    if not leaderboard_data.has(player_id):
        leaderboard_data[player_id] = {"score": 0}
    leaderboard_data[player_id]["score"] += score
    save_leaderboard_data()
    update_leaderboard()

func update_leaderboard():
    # Sort the leaderboard by score in descending order
    var sorted_entries = []
    for player_id in leaderboard_data.keys():
        sorted_entries.append({player_id: leaderboard_data[player_id]["score"]})
    sorted_entries.sort_custom(compare_scores)
    print(sorted_entries)

func compare_scores(a, b):
    if a.value() < b.value():
        return -1
    elif a.value() > b.value():
        return 1
    else:
        return 0

# Multiplayer sync functions
remote func rpc_add_player_score(player_id: String, score: int):
    add_player_score(player_id, score)

func _on_PlayerConnected(player_id):
    rpc_unreliable(rpc_add_player_score, player_id, 0) # Initialize new players with a default score

# Example usage (to be called when the game ends)
func end_game(player_id: String, score: int):
    add_player_score(player_id, score)

```

This script is designed to be attached to a Node in Godot Engine. It provides the following functionalities:
- Load and save leaderboard data from/to a JSON file.
- Add player scores and update the leaderboard.
- Sort and display the leaderboard.
- Support for multiplayer sync through RPC calls.

The script uses `FileAccess` for reading/writing JSON files and handles remote procedure calls (RPC) for synchronizing scores across multiple players.
"""
savegame.py

This module handles saving and loading game state data for the RPG project.
Game data is serialized to and from JSON format for readability and portability.

Functions:
- save_game(state, filename="savegame.json"): Saves the current game state to a JSON file.
- load_game(filename="savegame.json"): Loads the game state from a JSON file.

Note:
- Only standard Python data types (dict, list, str, int, etc.) should be used in the game state.
- Custom objects must be converted to serializable formats before saving.

Author: Francois Piche
Date: [2025-06-04]
"""

#Standard libraries imports
import json
import os
import datetime
#Third party libraries imports
#Local application imports

SAVE_FILE = "savegame.json"

def save_game(game_state):
    character = game_state.get("character")
    if not character:
        print("No character found in game state.")
        return

    data = {
        "character": character.to_dict(),
        "saved_at": datetime.datetime.now().isoformat()
    }

    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    game_state["last_saved"] = data["saved_at"]
    print("Game saved successfully.")

def load_game(game_state, character, item_lookup_func):
    if not os.path.exists(SAVE_FILE):
        print("No save file found.")
        return False

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    game_state["last_saved"] = data.get("saved_at", "Unknown")

    char_data = data.get("character")
    if not char_data:
        print("No character data found in save file.")
        return False

    # Reconstruct inventory items
    reconstructed_inventory = {}
    for item_name, item_info in char_data["inventory"].items():
        quantity = item_info["quantity"]
        item = item_lookup_func(item_name)
        if item:
            reconstructed_inventory[item_name] = {"quantity": quantity, "item": item}

    # Reconstruct equipped items
    reconstructed_equipment = {}
    for slot, item_name in char_data["equipment"].items():
        item = item_lookup_func(item_name)
        if item:
            reconstructed_equipment[slot] = item

    # Update character
    character.name = char_data["name"]
    character.constitution = char_data["constitution"]
    character.strength = char_data["strength"]
    character.stamina = char_data["stamina"]
    character.hp = char_data["hp"]
    character.gold = char_data["gold"]
    character.position = char_data["position"]
    character.inventory = reconstructed_inventory
    character.equipment = reconstructed_equipment

    game_state["character"] = character
    print("Game loaded successfully.")
    return True



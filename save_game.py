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
#Third party libraries imports
#Local application imports
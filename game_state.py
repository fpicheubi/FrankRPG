
"""
game_state.py

This module defines the initial game state for the medieval RPG.
It includes the character, world data, merchant inventory,
and other core elements of the game.

The game state is structured as a dictionary and is designed to be
easily serialized to JSON for saving and loading.

Usage:
- Import this module to access or reset the game state.
- Modify the structure here to expand the game with new features
  like quests, skills, or additional NPCs.

Author: Francois Piche
Date: 2025-06-04
"""
#Standard libraries imports
#Third party libraries imports
#Local application imports 

def initialize_game_state(character):
    return {
        "character": character,
        "world": {
            "current_area": "starting_village",
            "visited_areas": ["starting_village"]
        },
        "monsters_defeated": [],
        "merchant": {
            "location": {"x": 5, "y": 7},
            "inventory": [
                {"item": "Health Potion", "price": 10},
                {"item": "Iron Sword", "price": 50}
            ]
        },
    }

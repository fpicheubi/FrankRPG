"""
enemies.py

This module defines enemy types, behaviors, and attributes used throughout the game.
It provides functionality for creating and managing enemy instances, including their
stats, abilities, and interactions during combat.

Classes:
- Enemy: Base class representing a generic enemy with health, attack, and defense stats.
- [Optional] Specific enemy subclasses (e.g., Goblin, Skeleton) with unique traits or abilities.

Functions:
- generate_enemy(level): Returns a new enemy instance scaled to the player's level or game area.
- get_enemy_stats(enemy): Returns a formatted string or dictionary of enemy stats for display or logging.

Dependencies:
- random: For generating enemy stats or selecting enemy types.
- character: (Optional) For balancing enemy difficulty relative to the player.
- items/equipment: (Optional) If enemies can drop loot or use gear.

This module is used by the combat system and world generation logic to populate encounters.

Author: Francois Piche
Date: 2025-06-06
"""
#Standard libraries imports
import random
import inspect
#Third party libraries imports
#Local application imports
import items

class Enemy:
    def __init__(self, name, constitution, strength,experience):
        self.name = name
        self.constitution = constitution
        self.strength = strength
        self.hp = 10 * constitution
        self.stamina = 5 * constitution
        self.experience = experience

# Get all variables in the items module that are instances of Item
ALL_ITEMS = {
    name: obj for name, obj in inspect.getmembers(items)
    if isinstance(obj, items.Item)
}

ENEMY_TEMPLATES = {
    "Goblin": {"constitution": 5, "strength": 5, "experience": 10},
    "Goblin King": {"constitution": 10, "strength": 7, "experience": 20},
    "Skeleton": {"constitution": 6, "strength": 6, "experience": 12},
    "Orc": {"constitution": 8, "strength": 9, "experience": 16},
    "Bandit": {"constitution": 7, "strength": 6, "experience": 14},
    "Wolf": {"constitution": 4, "strength": 5, "experience": 10},
    "Zombie": {"constitution": 9, "strength": 4, "experience": 18},
    "Dark Knight": {"constitution": 12, "strength": 10, "experience": 24},
    "Slime": {"constitution": 3, "strength": 2, "experience": 6},
    "Witch": {"constitution": 6, "strength": 8, "experience": 12},
    "Troll": {"constitution": 11, "strength": 9, "experience": 22},
    "Vampire": {"constitution": 8, "strength": 10, "experience": 16},
}

ENEMY_LOOT_TABLE = {
    "Goblin": [ALL_ITEMS["POTION"]],
    "Goblin King": [ALL_ITEMS["MITHRIL_SWORD"], ALL_ITEMS["ELVEN_ARMOR"]],
    "Skeleton": [ALL_ITEMS["POTION"]],
    "Orc": [ALL_ITEMS["COPPER_SWORD"], ALL_ITEMS["LEATHER_ARMOR"]],
    "Bandit": [ALL_ITEMS["POTION"]],
    "Wolf": [ALL_ITEMS["POTION"]],
    "Zombie": [ALL_ITEMS["IRON_SWORD"], ALL_ITEMS["IRON_ARMOR"]],
    "Dark Knight": [ALL_ITEMS["METEORITE_SWORD"], ALL_ITEMS["METEORITE_ARMOR"]],
    "Slime": [ALL_ITEMS["POTION"]],
    "Witch": [ALL_ITEMS["COPPER_SWORD"], ALL_ITEMS["LEATHER_ARMOR"]],
    "Troll": [ALL_ITEMS["OBSIDIAN_SWORD"], ALL_ITEMS["DRAKESCALE_ARMOR"]],
    "Vampire": [ALL_ITEMS["COPPER_SWORD"], ALL_ITEMS["LEATHER_ARMOR"]],
}


def generate_enemy():
    name = random.choice(list(ENEMY_TEMPLATES.keys()))
    stats = ENEMY_TEMPLATES[name]
    return Enemy(name, stats["constitution"], stats["strength"],stats["experience"])


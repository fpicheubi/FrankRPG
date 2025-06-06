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
#Third party libraries imports
#Local application imports


class Goblin:
    def __init__(self):
        self.name = "Goblin"
        self.constitution = 5
        self.strength = 5
        self.hp = 10 * constitution
        self.stamina = 5 * constitution
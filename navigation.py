
"""
navigation.py

This module handles character movement within the game world.
It includes functions to update the character's position based on
directional input.

Functions:
- move_character(character, direction): Updates the character's position
  based on the given direction.

Author: Francois Piche
Date: 2025-06-06
"""

#Standard libraries imports
#Third party libraries imports
#Local application imports
from world_map import WORLD_BOUNDS


def move_character(character, direction):
    x, y = character.position['x'], character.position['y']

    if direction == 'north' and y > WORLD_BOUNDS['y_min']:
        character.position['y'] -= 1
    elif direction == 'south' and y < WORLD_BOUNDS['y_max']:
        character.position['y'] += 1
    elif direction == 'east' and x < WORLD_BOUNDS['x_max']:
        character.position['x'] += 1
    elif direction == 'west' and x > WORLD_BOUNDS['x_min']:
        character.position['x'] -= 1
    else:
        print(f"Invalid or blocked direction: {direction}")




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

def move_character(character, direction):
    """
    Moves the character in the specified direction.

    Parameters:
    - character (dict): The character dictionary with 'position' key.
    - direction (str): The direction to move ('north', 'south', 'east', 'west').

    Returns:
    None
    """
    if direction == 'north':
        character['position']['y'] += 1
    elif direction == 'south':
        character['position']['y'] -= 1
    elif direction == 'east':
        character['position']['x'] += 1
    elif direction == 'west':
        character['position']['x'] -= 1
    else:
        print(f"Invalid direction: {direction}")


"""
utils.py

This module contains utility functions and helper methods used across various parts of the game.
These functions are designed to be generic, reusable, and independent of specific game logic.

Typical responsibilities include:
- String formatting and text wrapping.
- Random number generation or dice rolls.
- Data validation and conversion.
- Common calculations or stat modifiers.

Functions:
- roll_dice(sides, times): Simulates rolling a die with a given number of sides.
- format_text_block(text, width): Wraps and formats text for display in the UI.
- clamp(value, min_value, max_value): Restricts a value to a specified range.

Dependencies:
- random: For RNG-based utilities.
- textwrap: For formatting text output.
- math: For general-purpose calculations.

This module is intended to support other modules like combat, UI, items, and navigation.

Author: Francois Piche
Date: 2025-06-06
"""

#Standard libraries imports
import os
#Third party libraries imports
#Local application imports

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
"""
decorators.py

This module defines custom decorators used throughout the game to enhance or modify
function behavior in a reusable and expressive way.

Typical use cases include:
- Logging function calls or game events.
- Validating game state before executing actions.
- Managing turn-based logic or cooldowns.
- Displaying messages or UI updates after certain actions.

Functions:
- @log_action: Logs the execution of decorated functions for debugging or analytics.
- @require_combat_state: Ensures a function only runs during combat.
- @cooldown(seconds): Prevents a function from being called again until a cooldown period has passed.

Dependencies:
- functools: For preserving function metadata.
- time: For managing cooldowns or delays.
- game_state: (Optional) For accessing or modifying shared game state.

This module is intended to be imported and used by other core modules like combat, navigation, or items.

Author: Francois Piche
Date: 2025-06-06
"""
#Standard libraries imports
#Third party libraries imports
#Local application imports
import character

# def stamina_check(Character,stamina):
#    def decorator(func):
#        def wrapper(*args, kwargs*):
#            if Character.stamina >= stamina
#                printf(f"Stamina check successfull! {Character} had {Character.stamina} stamina, the stamina cost was {stamina} and now  ")
#        return(func)
#    return (*args, kwargs*)

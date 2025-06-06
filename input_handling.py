"""
input_handling.py

This module is responsible for processing and interpreting player input during the game loop.
It translates key presses into in-game actions such as movement, inventory access, or quitting the game.

Functions:
- handle_input(key, game_state): Main input dispatcher that routes key presses to appropriate game actions.
- show_inventory(game_state): Displays the character's inventory in the game context panel.

Dependencies:
- navigation: For handling character movement.
- game_state: For accessing and modifying the current game state.

Intended to be used with a curses-based UI in main.py.

Author: Francois Piche
Date: 2025-06-06
"""
#Standard libraries imports
#Third party libraries imports
#Local application imports 
import navigation
import combat
import game_state as gs

def handle_input(key, game_state):
    """
    Handles player input based on the key pressed.
    """
    if key in (ord('w'), curses.KEY_UP):
        navigation.move_character(game_state, direction="north")
    elif key in (ord('s'), curses.KEY_DOWN):
        navigation.move_character(game_state, direction="south")
    elif key in (ord('a'), curses.KEY_LEFT):
        navigation.move_character(game_state, direction="east")
    elif key in (ord('d'), curses.KEY_RIGHT):
        navigation.move_character(game_state, direction="west")
    elif key == ord('i'):
        show_inventory(game_state)
    elif key == ord('q'):
        game_state['running'] = False
    else:
        game_state['message'] = "Unknown command."

def show_inventory(game_state):
    """
    Displays the character's inventory.
    """
    inventory = game_state['character'].inventory
    if not inventory:
        game_state['message'] = "Your inventory is empty."
    else:
        game_state['message'] = "Inventory: " + ", ".join(item.name for item in inventory)

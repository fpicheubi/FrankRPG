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
import curses
#Local application imports 
import navigation
import combat
import game_state as gs
from world_map import get_poi_at

def move_and_report(character, direction, game_state):
    ''' This simplifies repeating logic block for each movement directions'''
    navigation.move_character(character, direction)
    position = character.position
    poi = get_poi_at(position['x'], position['y'])
    if poi:
        game_state['context_view'] = f"poi:{poi['name']}"
        game_state['message'] = f"You arrived at {poi['name']}."
    else:
        game_state['context_view'] = "world"
        game_state['message'] = f"You moved to ({position['x']}, {position['y']})."

def handle_input(key, game_state):
    ''' Handles player input based on the key pressed '''
    if key in (ord('w'), curses.KEY_UP):
        move_and_report(game_state['character'], "north", game_state)
    elif key in (ord('s'), curses.KEY_DOWN):
        move_and_report(game_state['character'], "south", game_state)
    elif key in (ord('a'), curses.KEY_LEFT):
        move_and_report(game_state['character'], "west", game_state)
    elif key in (ord('d'), curses.KEY_RIGHT):
        move_and_report(game_state['character'], "east", game_state)
    elif key == ord('i'):
        game_state['context_view'] = 'inventory'
    elif key == ord('c'):
        game_state['context_view'] = 'character'
    elif key == 27: # ESC  <- This might cause problems and would need future fixing. i.e. if the character is located on a POI, pressing ESC won't handle it and still flip to the world view
        game_state['context_view'] = 'world'
    elif key == ord('o'):
        game_state['context_view'] = 'options'
    elif key == ord('q'):
        game_state['running'] = False
    else:
        game_state['message'] = "Unknown command."

def show_inventory(game_state):
    """ Displays the character's inventory """
    inventory = game_state['character'].inventory
    if not inventory:
        game_state['message'] = "Your inventory is empty."
    else:
        game_state['message'] = "Inventory: " + ", ".join(item.name for item in inventory)

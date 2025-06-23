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
Date: 2025-06-20
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
    success = navigation.move_character(character, direction)
    if not success:
            game_state['message'] = f"Invalid or blocked direction: {direction}"
    position = character.position
    poi = get_poi_at(position['x'], position['y'])
    if poi:
        game_state['context_view'] = f"poi:{poi['name']}"
        game_state['message'] = f"You arrived at {poi['name']}."
    else:
        game_state['context_view'] = "world"
        if success: # Making sure that the navigation was successfull before displaying where the character moved
            game_state['last_position'] = dict(character.position)
            game_state['message'] = f"You moved to ({position['x']}, {position['y']})."


def handle_input(key, game_state):
    context = game_state.get("context_view", "world")

    ''' Provides combat-based input handling '''
    if context == 'combat':
        if game_state.get('combat_state') == 'awaiting_input':
            if key in [ord('a'), ord('A')]:
                game_state['combat_state'] = 'player_attack'
                combat.perform_attack(game_state)
            elif key in [ord('f'), ord('F')]:
                game_state['combat_state'] = 'flee_attempt'
                combat.flee_combat(game_state)
            # Continue combat flow after player action
            if game_state.get('combat_state') == 'enemy_turn':
                combat.enemy_turn(game_state)
            elif game_state.get('combat_state') == 'flee_attempt':
                combat.flee_combat(game_state)
            return  # Prevents fall-through to movement logic

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
    elif key == 27: # ESC  <- This might cause problems and would need future fixing. i.e. if the character is located on a POI, pressing ESC won't handle it properly and still flip to the world view
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


def use_item(game_state, item_name):
    character = game_state['character']
    if character.has_item(item_name):
        item = character.inventory[item_name]['item']
        item.use(character)
        character.remove_item(item_name)
        game_state['message'] = f"You used {item_name}."
    else:
        game_state['message'] = f"You don't have a {item_name}."

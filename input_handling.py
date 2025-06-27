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
    context = game_state.get("context_view")

    # Inventory navigation and selection
    if context == "inventory":
        inventory_items = list(game_state['character'].inventory.items())
        if not inventory_items:
            return
        if key in (ord('w'), ord('W')):
            game_state['inventory_index'] = max(0, game_state['inventory_index'] - 1)
        elif key in (ord('s'), ord('S')):
            game_state['inventory_index'] = min(len(inventory_items) - 1, game_state['inventory_index'] + 1)
        elif key in (curses.KEY_ENTER, 10, 13):  # Enter key
            item_name, data = inventory_items[game_state['inventory_index']]
            item = data['item']
            character = game_state['character']

            if item.equippable:
                if any(e.name == item_name for e in character.equipment.values()):
                    item.unequip(character)
                    game_state['message'] = f"{item_name} unequipped."
                else:
                    item.equip(character)
                    game_state['message'] = f"{item_name} equipped."
            elif "potion" in item.name.lower():
                item.use(character)
                character.remove_item(item_name)
                game_state['message'] = f"You used {item_name}"
        elif key in (27, ord('i'), ord('I')):  # ESC or i/I to return to world view
            game_state['context_view'] = 'world'
        return

    # Handle follow-up input
    if game_state.get('awaiting_input') == 'equip_item':
        item_name = game_state.get('typed_input', '').strip()
        character = game_state['character']
        item_data = character.inventory.get(item_name)
        if item_data and item_data['item'].equippable:
            item_data['item'].equip(character)
            game_state['message'] = f"{item_name} equipped."
        else:
            game_state['message'] = f"Cannot equip {item_name}."
        game_state['awaiting_input'] = None

    elif game_state.get('awaiting_input') == 'unequip_slot':
        slot = game_state.get('typed_input', '').strip().lower()
        character = game_state['character']
        equipped_item = character.equipment.get(slot)
        if equipped_item:
            equipped_item.unequip(character)
            game_state['message'] = f"{slot.capitalize()} unequipped."
        else:
            game_state['message'] = f"No item equipped in {slot}."
        game_state['awaiting_input'] = None

    # Combat input
    if context == 'combat':
        if game_state.get('combat_state') == 'awaiting_input':
            if key in [ord('a'), ord('A')]:
                game_state['combat_state'] = 'player_attack'
                combat.perform_attack(game_state)
                return
            elif key in [ord('f'), ord('F')]:
                game_state['combat_state'] = 'flee_attempt'
                combat.flee_combat(game_state)
                return
            elif key in [ord('p'), ord('P')]:
                character = game_state['character']
                for item_name, data in character.inventory.items():
                    item = data['item']
                    if "potion" in item.name.lower():
                        item.use(character)
                        character.remove_item(item_name)
                        game_state['message'] = f"You used {item_name}."
                        break
                else:
                    game_state['message'] = "You have no potions to use."
                return
        if game_state.get('combat_state') == 'enemy_turn':
            combat.enemy_turn(game_state)
            return
        elif game_state.get('combat_state') == 'flee_attempt':
            combat.flee_combat(game_state)
            return
        # Wait for any key to acknowledge victory
        if game_state.get('combat_state') == 'combat_end':
            game_state['combat_state'] = None
            game_state['context_view'] = 'world'
            game_state['combat_just_ended'] = True
            return


    # Movement and general input
    if context != 'combat':
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
            game_state['inventory_index'] = 0  # Reset selection when entering inventory
        elif key == ord('c'):
            game_state['context_view'] = 'character'
        elif key == 27:  # ESC
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

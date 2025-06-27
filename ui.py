"""
ui.py

This module handles all user interface rendering using the curses library.
It is responsible for drawing the main game panels, including:

- World View Panel: Displays the game world or map.
- Contextual Panel: Shows character stats, combat info, inventory, and other contextual data.
- Input Panel: Displays messages and prompts for player input.

Functions:
- draw_world_panel(stdscr, game_state): Renders the left-side world view.
- draw_context_panel(stdscr, game_state): Renders the top-right contextual information.
- draw_input_panel(stdscr, game_state): Renders the bottom-right input and message area.

Dependencies:
- curses: For terminal-based UI rendering.
- game_state: Provides access to current game data for display.

This module is designed to be called from the main game loop in main.py.

Author: Francois Piche
Date: 2025-06-06

"""

#Standard libraries imports
#Third party libraries imports
import curses
#Local application imports
from world_map import WORLD_BOUNDS
from world_map import POINTS_OF_INTEREST

GREEN_TEXT = None

def init_colors():
    global GREEN_TEXT
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    GREEN_TEXT = curses.color_pair(1)

def render_map(player_position):
    ''' Map rendering function for Pure logic.  It builds a 2D representation of the game world as a list of strings to keep it independant from the Curse UI system.  
    It makes it easier to test without needing a terminal and can be re-used in other contexts (e.g. saving a snapshot of the map, debugging, logging)'''
    
    # Prepares the grid inside world bounds
    width = WORLD_BOUNDS['x_max'] - WORLD_BOUNDS['x_min'] + 1
    height = WORLD_BOUNDS['y_max'] - WORLD_BOUNDS['y_min'] + 1
    map_grid = [['.' for _ in range(width)] for _ in range(height)]

    # Place POIs symbols dynamically 
    for (x, y), poi in POINTS_OF_INTEREST.items():
        symbol = poi.get('symbol', '?') # Fallback to '?' if symbol is missing
        if 0 <= x < width and 0 <= y < height:
            map_grid[y][x] = symbol

    # Place the player   
    x, y = player_position
    if 0 <= x < width and 0 <= y < height:
        map_grid[y][x] = '@'
    return [''.join(row) for row in map_grid]


def draw_world_panel(stdscr, game_state):
    ''' UI rendering function.  Takes the rendered map and displays it using curses.  It keeps all curses-specific logic in one place and makes it easier to adapt 
    or replace the UI layer later (e.g. switching to a GUI or web interface) '''
    height, width = stdscr.getmaxyx()
    world_width = width // 2
    world_win = curses.newwin(height, world_width, 0, 0)
    world_win.box()
    world_win.addstr(0, 2, " World View ")

    player_position = game_state['character'].position
    map_lines = render_map((player_position['x'], player_position['y']))

    for i, line in enumerate(map_lines[:height - 2]):
        world_win.addstr(i + 1, 1, line[:world_width - 2])

    world_win.refresh()


def draw_context_panel(stdscr, game_state):
    height, width = stdscr.getmaxyx()
    context_height = height - 7 # Leaving enough space at the bottom of the screen for the input panel
    context_width = width // 2 # Located in the rightmost half of the screen
    context_win = curses.newwin(context_height, context_width, 0, width // 2)
        
    view = game_state.get("context_view", "world") # Retrieve current context value.  If none exist, defaults to world view
    title = view.capitalize() if not view.startswith("poi:") else view.split(":",1)[1].capitalize() # Capitalizes the first letter of the view name. For POIs, removes the "poi:" part of the string
    context_win.box()
    context_win.addstr(0, 2, f" {title} View ")

    character = game_state.get("character")

    if view == "character" and character:
        context_win.addstr(2, 2, f"Name: {character.name}")
        context_win.addstr(3, 2, f"Level: {character.level}")
        context_win.addstr(4, 2, f"HP: {character.hp}/{character.max_hp}")
        context_win.addstr(5, 2, f"Experience: {character.experience}/{50*(1+character.level)}")
        con_bonus = character.constitution - character.base_constitution
        str_bonus = character.strength - character.base_strength
        context_win.addstr(6, 2, f"Constitution: {character.base_constitution}")
        if con_bonus > 0:
            context_win.addstr(f" + {con_bonus}", GREEN_TEXT)
        context_win.addstr(7, 2, f"Strength: {character.base_strength}")
        if str_bonus > 0:
            context_win.addstr(f" + {str_bonus}", GREEN_TEXT)
        context_win.addstr(8, 2, f"Stamina: {character.stamina}")

    elif view == "combat":
        line1 = game_state.get('combat_line1', '')
        line2 = game_state.get('combat_line2', '')
        line3 = game_state.get('combat_line3', '')
        line4 = game_state.get('combat_line4', '')
        context_win.addstr(2, 2, line1)
        context_win.addstr(3, 2, line2)
        context_win.addstr(4, 2, line3)
        context_win.addstr(5, 2, line4)
        message = game_state.get("message", "") 
        if message:
            context_win.addstr(height -9, 2, f"Msg: {message[:context_width - 4]}")

    elif view == "inventory" and character:
        context_win.addstr(2, 2, "Inventory:")
        line = 3
        inventory_items = list(character.inventory.items())
        selected_index = min(game_state.get('inventory_index', 0), len(inventory_items) - 1)

        for idx, (item_name, data) in enumerate(inventory_items):
            qty = data['quantity']
            item = data['item']
            equipped = any(e.name == item_name for e in character.equipment.values())
            label = f"- {item_name} x{qty}"
            if item.equippable:
                label += " (Equipped)" if equipped else ""

            if idx == selected_index:
                context_win.attron(curses.A_REVERSE)
                context_win.addstr(line, 4, label)
                context_win.attroff(curses.A_REVERSE)
            else:
                context_win.addstr(line, 4, label)
            line += 1

        context_win.addstr(line, 4, f"Gold: {character.gold}")
        message = game_state.get("message", "") 
        if message:
            context_win.addstr(height -9, 2, f"Msg: {message[:context_width - 4]}")

    elif view.startswith("poi:"):
        poi_name = view.split(":", 1)[1]
        context_win.addstr(2, 2, f"{poi_name} Dashboard")
        # Fountain-specific logic placeholder:
        # City-specific logic placeholder:
        # Merchant-Specific logic placeholder:

    elif view == "world" and character:
        context_win.addstr(2, 2, f"Name: {character.name}")
        context_win.addstr(3, 2, f"HP: {character.hp}/{character.max_hp}")
        context_win.addstr(4, 2, f"Level: {character.level}")      
        message = game_state.get("message", "")
        if message:
            context_win.addstr(height -9, 2, f"Msg: {message[:context_width - 4]}")

    context_win.refresh()


def draw_input_panel(stdscr, game_state):
    height, width = stdscr.getmaxyx()
    input_height = 7
    input_width = width // 2
    input_win = curses.newwin(input_height, input_width, height - input_height, width // 2)
    input_win.box()
    input_win.addstr(0, 2, " Input ")

    context = game_state.get("context_view", "world")

    if context == "combat":
        input_win.addstr(1, 2, "Combat Options:")
        input_win.addstr(2, 4, "(A)ttack  (P)otion  (F)lee")
        input_win.addstr(3, 4, "ESC = Return to world view")
    elif context == "world":
        input_win.addstr(1, 2, "Directional keys: A = West , W = North , S = South , D = East")
        input_win.addstr(2, 2, "Contextual windows: C = Character, I = Inventory, O = Options")
        input_win.addstr(3, 2, "ESC = Return to world view")
        input_win.addstr(4, 2, "Q = Quit game")
    elif context == "inventory":
        input_win.addstr(1, 2, "Inventory Options:")
        input_win.addstr(2, 4, "W/S = Selection up and down")
        input_win.addstr(3, 4, "<Enter> = Toggle equip/unequip")
        input_win.addstr(4, 4, "ESC or I = Return to world view")
    # Logic for for other POIs
    else:
        input_win.addstr(1, 2, "Directional keys: A = West , W = North , S = South , D = East")
        input_win.addstr(2, 2, "Contextual windows: C = Character, I = Inventory, O = Options")
        input_win.addstr(3, 2, "ESC = Return to world view")
        input_win.addstr(4, 2, "Q = Quit game")

    input_win.refresh()
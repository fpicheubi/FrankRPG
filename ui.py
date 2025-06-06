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


def draw_world_panel(stdscr, game_state):
    height, width = stdscr.getmaxyx()
    world_width = width // 2
    world_win = curses.newwin(height, world_width, 0, 0)
    world_win.box()
    world_win.addstr(0, 2, " World View ")
    
    # Example content
    world_map = game_state.get("world_map", [])
    for i, line in enumerate(world_map[:height - 2]):
        world_win.addstr(i + 1, 1, line[:world_width - 2])
    
    world_win.refresh()

def draw_context_panel(stdscr, game_state):
    height, width = stdscr.getmaxyx()
    context_height = height - 5
    context_width = width // 2
    context_win = curses.newwin(context_height, context_width, 0, width // 2)
    context_win.box()
    context_win.addstr(0, 2, " Context ")

    character = game_state.get("character")
    if character:
        context_win.addstr(2, 2, f"Name: {character.name}")
        context_win.addstr(3, 2, f"HP: {character.hp}/{character.max_hp}")
        context_win.addstr(4, 2, f"Level: {character.level}")
        # Add more character stats or context info here

    context_win.refresh()

def draw_input_panel(stdscr, game_state):
    height, width = stdscr.getmaxyx()
    input_height = 5
    input_width = width // 2
    input_win = curses.newwin(input_height, input_width, height - input_height, width // 2)
    input_win.box()
    input_win.addstr(0, 2, " Input ")

    message = game_state.get("message", "")
    input_win.addstr(2, 2, message[:input_width - 4])

    input_win.refresh()

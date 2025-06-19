"""
main.py

This is the main entry point of the game. It initializes the game state, sets up the curses-based
user interface, and runs the main game loop. The loop handles rendering, input processing, and
game state updates.

Key Responsibilities:
- Initialize the curses screen and configure UI settings.
- Create the player character and load or initialize the game state.
- Continuously render the UI panels (world view, context, input).
- Capture and delegate player input to the input handling system.
- Update the game state based on player actions and game logic.

Functions:
- main(stdscr): The main game loop wrapped by curses.wrapper().

Dependencies:
- curses: For terminal-based UI rendering.
- character: For creating and managing the player character.
- game_state: For initializing and updating the game state.
- navigation, combat, enemies, items, utils, decorators: Core game logic modules.
- input_handling: For interpreting and responding to player input.
- ui: For rendering the game interface.

This module should be run directly to start the game.

Author: Francois Piche
Date: 2025-06-06
"""
#Standard libraries imports
import os
import math
import logging
#Third party libraries imports
import curses
# local application imports 
import character as character_module
import combat
import decorators
import enemies
import equipment
import game_state as game_state_module
import input_handling
import items
import navigation
import save_game
import ui
import utils
import world_map


logging.basicConfig(filename="debug.log", level=logging.DEBUG)

def update_game_state(game_state):
    pass # Placeholder for future game state updates

def main(stdscr, player):
    # Setup
    curses.curs_set(0)
    stdscr.clear()

    # Initialize game state
    game_state = game_state_module.initialize_game_state(player)
    game_state['context_view'] = 'world' # Default view is set to world

    # Initial UI Draw before entering the game loop    
    ui.draw_world_panel(stdscr, game_state)
    ui.draw_context_panel(stdscr, game_state)
    ui.draw_input_panel(stdscr, game_state)
    stdscr.refresh()

    # Main game loop
    while game_state['running']:
        # 1. Draw UI Panels
        ui.draw_world_panel(stdscr, game_state)
        ui.draw_context_panel(stdscr, game_state)
        ui.draw_input_panel(stdscr, game_state)

        # 2. Get Player Input
        key = stdscr.getch()
        # 3. Handle Input
        input_handling.handle_input(key, game_state)

        # 4. Update Game State (if needed)
        update_game_state(game_state)

        # 5. Refresh screen
        stdscr.refresh()

if __name__ == "__main__":
    player = character_module.create_character() #Initialize the player, happens before curses starts to prevent the curses UI from hiding character creation
    curses.wrapper(lambda stdscr: main(stdscr, player))

"""
combat.py

This module manages all combat-related mechanics in the game, including turn-based battles,
damage calculation, enemy attacks, and player actions during combat encounters.

Functions:
- initiate_combat(player, enemy): Starts a combat sequence between the player and an enemy.
- player_attack(player, enemy): Handles the player's attack logic and damage output.
- enemy_attack(enemy, player): Handles the enemy's attack logic and damage output.
- is_combat_over(player, enemy): Checks if the combat has ended based on health or other conditions.
- calculate_damage(attacker, defender): Computes damage dealt based on stats, equipment, and modifiers.

Dependencies:
- character: For accessing player stats and abilities.
- enemies: For enemy definitions and behavior.
- items/equipment: For applying item or gear effects during combat.
- game_state: For updating and tracking combat status.

This module is intended to be called from the main game loop or input handler when a combat scenario is triggered.

Author: Francois Piche
Date: 2025-06-20
"""
#Standard libraries imports
import random
#Third party libraries imports
#Local application imports
from enemies import generate_enemy


def start_combat(game_state):
    # Phase one: Initialize enemy and set combat state
    player = game_state['character']
    enemy = generate_enemy()
    enemy.max_hp = enemy.hp
    game_state['enemy'] = enemy
    game_state['combat_line1'] = f"A wild {enemy.name} appears!"
    game_state['combat_line2'] = ""
    game_state['combat_state'] = 'awaiting_input'

    # turn-based combat loop
    while player.hp > 0 and enemy.hp > 0 and game_state['combat_state'] != 'fled':
        if game_state['combat_state'] == 'awaiting_input':
            # Wait for player input (attack, flee, etc.)
            break # Exit loop to wait for input from UI or main loop
        elif game_state['combat_state'] == 'player_attack':
            perform_attack(game_state)
        elif game_state['combat_state'] == 'enemy_turn':
            enemy_turn(game_state)
        elif game_state['combat_state'] == 'flee_attempt':
            flee_combat(game_state)


def perform_attack(game_state):
    player = game_state['character']
    enemy = game_state['enemy']
    damage = max(1, player.strength - enemy.constitution)
    enemy.hp -= damage
    #First line to be displayed in the combat-context window
    game_state['combat_line1'] = f"You hit the {enemy.name} for {damage} damage!"
    #Second line to be displayed in the combat-context window
    game_state['combat_line2'] = f"The {enemy.name} has ({enemy.hp}/{enemy.max_hp} HP remaining.  Meanwhile, you have {player.hp}/{player.max_hp} HP remaining"


    if enemy.hp <= 0:
        game_state['combat_line1'] = f" You defeated the {enemy.name} and gained {enemy.experience} experience!"
        player.gain_experience(enemy.experience)
        game_state['combat_state'] = None
        game_state['context_view'] = 'world'
        game_state['combat_just_ended'] = True #This ensures that after defeating an enemy, combat won't retrigger immediately
    else:
        game_state['combat_state'] = 'enemy_turn'


def enemy_turn(game_state):
    player = game_state['character']
    enemy = game_state['enemy']
    damage = max(1, enemy.strength - player.constitution)
    player.hp -= damage

    #First line to be displayed in the combat-context window
    game_state['combat_line1'] = f"The {enemy.name} hits you for {damage} damage!"
    #Second line to be displayed in the combat-context window
    game_state['combat_line2'] = f"The {enemy.name} has {enemy.hp}/{enemy.max_hp} HP remaining.  Meanwhile, you have {player.hp}/{player.max_hp} HP remaining"

    if player.hp <= 0:
        game_state['combat_line1'] = " You were defeated, this is the end of the game!"
        game_state['context_view'] = 'world'
        game_state['combat_state'] = None
    else:
        game_state['combat_state'] = 'awaiting_input'


def flee_combat(game_state):
    success_chance = 0.5 #50% chance to flee successfully
    if random.random() > success_chance:
        game_state['combat_line1'] = "You sucessfully fled the battle!"
        game_state['context_view'] = 'world'
        game_state['combat_state'] = None
        game_state.pop('enemy', None) #Removes the enemy from game state
    else:
        game_state['combat_line1'] = "You failed to flee the battle!"
        game_state['combat_state'] = 'enemy_turn'
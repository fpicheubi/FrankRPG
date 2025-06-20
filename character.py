"""
character.py

This module defines the Character class and the character creation logic
for the medieval RPG. It includes randomized attribute generation with
reroll options and a method to convert the character object into a
dictionary format suitable for saving and game state integration.

Classes:
- Character: Represents the character' attributes and inventory.

Functions:
- create_character(): Handles user input and random generation to create
  a new Character instance.

Note:
- The Character class includes a to_dict() method for JSON serialization.
- This module is intended to be used during game initialization.

Author: Francois Piche
Date: 2025-06-04
"""

#Standard libraries imports
import random
import os
#Third party libraries imports
#Local application imports 
import utils
import items

class Character:
    def __init__(self, name, constitution, strength): #The only initialization arguments passed are what the player input and randomized stats.  The rest is static and won't requirement arguments.
        self.name = name
        self.level = 1
        self.experience = 0
        self.constitution = constitution
        self.strength = strength
        self.stamina = 5 * constitution
        self.hp = 10 * constitution
        self.max_hp = 10 * constitution
        self.gold = 50
        self.position = {"x": 21, "y": 13}
        self.inventory = {}
        # Initialize items inventory slots
        self.item = {}
        # Initialize equipment slots
        self.equipment = {}
        # Adds starting equipment to character inventory
        self.add_item(items.WOODEN_SWORD)
        self.add_item(items.RAGS_ARMOR)
        # Equip sword and armor to gain bonuses
        items.WOODEN_SWORD.equip(self)
        items.RAGS_ARMOR.equip(self)

    def to_dict(self):
        # Used for saving the game
        return {
            "name": self.name,
            "constitution": self.constitution,
            "strength": self.strength,
            "stamina": self.stamina,
            "hp": self.hp,
            "gold": self.gold,
            "position": self.position,
            "inventory": self.inventory,
            "equipment": self.equipment
        }

    def from_dict(self):
        # Used for loading the game
        return {
            "name": self.name,
            "constitution": self.constitution,
            "strength": self.strength,
            "stamina": self.stamina,
            "hp": self.hp,
            "gold": self.gold,
            "position": self.position,
            "inventory": self.inventory,
            "equipment": self.equipment
        }

    def add_item(self, item, quantity=1):
        if item.name in self.inventory:
            self.inventory[item.name]['quantity'] += quantity
        else:
            self.inventory[item.name] = {'item': item, 'quantity': quantity}

    def remove_item(self, item_name, quantity=1):
        if item_name in self.inventory:
            self.inventory[item_name]['quantity'] -= quantity
            if self.inventory[item_name]['quantity'] <= 0:
                del self.inventory[item_name]

    def has_item(self, item_name):
        return item_name in self.inventory and self.inventory[item_name]['quantity'] > 0

def create_character():
    print(f"=== Character Creator ==={os.linesep}")
    name = input("Enter character name: ")
    print(f" ")
    attributes = {
         "constitution": random.randint(5, 20),
         "strength": random.randint(5, 20),
    }
    confirm_stats = ""
    rerolls_remaining = 3
    while confirm_stats != "Y" and rerolls_remaining > 0:
        if rerolls_remaining == 3:
            print(f"The following character will be created: {os.linesep}")
            print(f"Name: {name}")
            print(f"Constitution: {attributes['constitution']}")
            print(f"Strength: {attributes['strength']}{os.linesep}")
            print(f"Rerolls remaining: {rerolls_remaining}{os.linesep}")
            print(f"Are you satisfied with these attributes? (If not you can reroll)")
            print(f"(Y)Yes (R)Reroll")
        confirm_stats = input().upper()
        if confirm_stats == "R":
            rerolls_remaining -= 1
            attributes = {
                "constitution": random.randint(5, 20),
                "strength": random.randint(5, 20),
            }
            print(f"The following character will be created: {os.linesep}")
            print(f"Name: {name}")
            print(f"Constitution: {attributes['constitution']}")
            print(f"Strength: {attributes['strength']}{os.linesep}")
            print(f"Are you satisfied with these attributes? (If not you can reroll)")
            print(f"(Y)Yes (R)Reroll")
    if rerolls_remaining == 0:
        print(f"You ran out of rerolls!")
    return Character(name, **attributes)

def gain_experience(self, amount):
    #Used to level up the character when successfully executing certain actions (e.g. Killing an enemy, finishing a quest)
    self.experience += amount
    if self.experience >= self.experience_to_next_level():
        self.level_up()

def experience_to_next_level(self):
    return 100 * self.level  # Example formula. Lvl 2 = 100XP, Lvl 3 = 200XP, Lvl 4 = 300XP

def level_up(self):
    self.level += 1
    self.experience = 0 #Each time we level up, XP goes back to zero
    self.constitution += 1
    self.strength += 1
    self.max_hp = 10 * self.constitution
    self.hp = self.max_hp # Each time we level up, we get full HP as a bonus! YAY

"""
items.py

This module defines all general items in the game, including consumables, quest items,
and base item functionality. It provides item classes, effects, and inventory interactions.

Classes:
- Item: Base class for all items with common properties (name, description, value). These also contain the following:
    - Consumable: Subclass for items that can be used (e.g., potions, scrolls).
    - QuestItem: Subclass for items related to quests or story progression.
    - Equipment: Armors, weapons, ring, etc.

Functions:
- use_item(character, item): Applies the item's effect to the character.
- get_item_description(item): Returns a formatted string describing the item.

Dependencies:
- character: For applying item effects to the player.
- game_state: For updating inventory or triggering events.
- utils: (Optional) For formatting or helper functions.

This module is used by inventory systems, combat (for consumables), and quest logic.

Author: Francois Piche
Date: 2025-06-20
"""
#Standard libraries imports
import inspect
#Third party libraries imports
#Local application imports

class Item:
    def __init__(self, name, description, effect=None, equippable=False, slot=None, bonus=None):
        self.name = name
        self.description = description
        self.effect = effect or {}  # e.g., {"hp": +20}
        self.equippable = equippable
        self.slot = slot  # e.g., "weapon", "armor"
        self.bonus = bonus or {}  # e.g., {"strength": +2}


    def use(self, target):
        if self.equippable:
            self.equip(target)
        else:
            for stat, value in self.effect.items():
                if hasattr(target, stat):
                    setattr(target, stat, min(getattr(target, f"max_{stat}", getattr(target, stat)), getattr(target, stat) + value))


    def equip(self, character):
        if self.slot:
            # Unequip existing item in the same slot
            if self.slot in character.equipment:
                character.equipment[self.slot].unequip(character)
            character.equipment[self.slot] = self
            for stat, value in self.bonus.items():
                if hasattr(character, stat):
                    setattr(character, stat, getattr(character, stat) + value)


    def unequip(self, character):
        if self.slot and character.equipment.get(self.slot) == self:
            for stat, value in self.bonus.items():
                if hasattr(character, stat):
                    setattr(character, stat, getattr(character, stat) - value)
            del character.equipment[self.slot]


# Healing potion
POTION = Item("Healing Potion", "Restores 20 HP", effect={"hp": 20})

# Swords
WOODEN_SWORD = Item("Wooden Sword", "A practice sword", equippable=True, slot="weapon", bonus={"strength": 2})
COPPER_SWORD = Item("Copper Sword", "A common sword", equippable=True, slot="weapon", bonus={"strength": 4})
IRON_SWORD = Item("Iron Sword", "A uncommon sword", equippable=True, slot="weapon", bonus={"strength": 8})
MITHRIL_SWORD = Item("Mithril Sword", "A rare sword", equippable=True, slot="weapon", bonus={"strength": 12})
OBSIDIAN_SWORD = Item("Obsidian Sword", "A epic sword", equippable=True, slot="weapon", bonus={"strength": 16})
METEORITE_SWORD = Item("Meteorite Sword", "A legendary sword", equippable=True, slot="weapon", bonus={"strength": 20})

# Armors
RAGS_ARMOR = Item("Rags armor", "A practice armor", equippable=True, slot="armor", bonus={"constitution": 1})
LEATHER_ARMOR = Item("Leather armor", "A common armor", equippable=True, slot="armor", bonus={"constitution": 2})
IRON_ARMOR = Item("Iron-Plated chainmail", "A uncommon armor", equippable=True, slot="armor", bonus={"constitution": 3})
ELVEN_ARMOR = Item("Elvenleaf weave armor", "A rare armor", equippable=True, slot="armor", bonus={"constitution": 4})
DRAKESCALE_ARMOR = Item("Drakescale armor", "A epic armor", equippable=True, slot="armor", bonus={"constitution": 5})
METEORITE_ARMOR =  Item("Meteorite armor", "A legendary armor", equippable=True, slot="armor", bonus={"constitution": 6})




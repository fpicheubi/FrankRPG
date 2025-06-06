"""
equipment.py

This module defines the equipment system for the game, including weapons, armor, and other gear
that can be equipped by the player or enemies. It manages equipment stats, effects, and how
equipment modifies character attributes.

Classes:
- Equipment: Base class for all equippable items.
- Weapon: Subclass representing weapons with attack bonuses or special effects.
- Armor: Subclass representing armor with defense bonuses or resistances.

Functions:
- equip_item(character, item): Equips an item to the appropriate slot and updates stats.
- unequip_item(character, slot): Removes an item from a slot and reverts stat changes.
- get_equipped_items(character): Returns a list or dictionary of currently equipped items.

Dependencies:
- character: For modifying player stats based on equipment.
- items: For shared item properties or inheritance.
- utils: (Optional) For formatting or validation helpers.

This module is used by the combat system, inventory management, and character customization.

Author: Francois Piche
Date: 2025-06-06
"""
#Standard libraries imports
#Third party libraries imports
#Local application imports


class Equipment:
    def __init__(self, name, slot, bonus):
        self.name = name
        self.slot = slot  # e.g., "weapon", "armor"
        self.bonus = bonus  # e.g., {"strength": +5}

    def equip(self, character):
        # Equip the item
        character.equipment[self.slot] = self

        # Apply stat bonuses
        for stat, value in self.bonus.items():
            if hasattr(character, stat):
                setattr(character, stat, getattr(character, stat) + value)

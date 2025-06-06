"""
items.py

This module defines all general items in the game, including consumables, quest items,
and base item functionality. It provides item classes, effects, and inventory interactions.

Classes:
- Item: Base class for all items with common properties (name, description, value).
- Consumable: Subclass for items that can be used (e.g., potions, scrolls).
- QuestItem: Subclass for items related to quests or story progression.

Functions:
- use_item(character, item): Applies the item's effect to the character.
- get_item_description(item): Returns a formatted string describing the item.

Dependencies:
- character: For applying item effects to the player.
- game_state: For updating inventory or triggering events.
- utils: (Optional) For formatting or helper functions.

This module is used by inventory systems, combat (for consumables), and quest logic.

Author: Francois Piche
Date: 2025-06-06
"""
#Standard libraries imports
#Third party libraries imports
#Local application imports


class Item:
    def __init__(self, name, description, effect):
        self.name = name
        self.description = description
        self.effect = effect  # e.g., {"hp": +20}

    def use(self, target):
        # Apply effect to target (e.g., character)
        pass

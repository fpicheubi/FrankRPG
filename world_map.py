"""
world_map.py

This module defines the structure and data for the game world, including map boundaries,
points of interest (POIs), and terrain features. It is designed to make world creation
and iteration simple and flexible.

Key Responsibilities:
- Define world boundaries and coordinate system.
- Store and manage points of interest (e.g., towns, dungeons, landmarks).
- Mark unpassable or special terrain types (e.g., water, mountains).
- Provide utility functions for querying world layout and terrain.

Data Structures:
- WORLD_BOUNDS: Tuple defining the size of the world grid.
- POINTS_OF_INTEREST: Dictionary mapping names to coordinates and metadata.
- TERRAIN_MAP: Optional grid or dictionary defining terrain types and passability.

Functions:
- is_passable(x, y): Returns whether a tile is walkable.
- get_poi_at(x, y): Returns the point of interest at a given coordinate, if any.
- generate_world(): (Optional) Creates or loads the world layout.

This module is used by navigation, UI rendering, and game logic to interact with the world.

Author: Francois Piche
Date: 2025-06-06
"""
#Standard libraries imports
#Third party libraries imports
#Local application imports


''' Define the playable area of the map, 4K resolution monitor required! '''
WORLD_BOUNDS = {
    'x_min': 0,
    'x_max': 132, # The map is 132 columns large
    'y_min': 0,
    'y_max': 69 # The map is 69 rows high
}

''' Define points of interest '''
POINTS_OF_INTEREST = {
    (21, 13): {'name': 'City', 'symbol': 'C'},
    (3, 20): {'name': 'Camp', 'symbol': 'c'},
    (20, 20): {'name': 'Merchant', 'symbol': 'M'},
    (30, 30): {'name': 'Fountain', 'symbol': 'F'},
}

def get_poi_at(x, y):
    ''' Returns the name of a point of interest at a given coordinate: '''
    return POINTS_OF_INTEREST.get((x, y), None)

def get_coordinates_of_poi(poi_name):
    ''' Returns the coordinates of a given point of interest: '''
    for coords, name in POINTS_OF_INTEREST.items():
        if name == poi_name:
            return coords
    return None

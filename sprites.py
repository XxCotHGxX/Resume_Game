# sprites.py - Contains functions to create SNES-style sprites for the game

import pygame
import os
from config import *

# Asset paths
PLAYER_SPRITE_SHEET = os.path.join('static', 'Boss', 'Boss', 'Boss.png')
OBJECTS_SPRITE_SHEET = os.path.join('static', 'gfx', 'gfx', 'objects.png')
NPC_SPRITE_SHEET = os.path.join('static', '24x32 lying down.png')
OVERWORLD_SPRITE_SHEET = os.path.join('static', 'gfx', 'gfx', 'Overworld.png')

# --- Lazy loading and caching for sprite sheets ---
_player_sprite_sheet = None
def get_player_sprite_sheet():
    global _player_sprite_sheet
    if _player_sprite_sheet is None:
        _player_sprite_sheet = pygame.image.load(PLAYER_SPRITE_SHEET).convert_alpha()
    return _player_sprite_sheet

_objects_sprite_sheet = None
def get_objects_sprite_sheet():
    global _objects_sprite_sheet
    if _objects_sprite_sheet is None:
        _objects_sprite_sheet = pygame.image.load(OBJECTS_SPRITE_SHEET).convert_alpha()
    return _objects_sprite_sheet

_npc_sprite_sheet = None
def get_npc_sprite_sheet():
    global _npc_sprite_sheet
    if _npc_sprite_sheet is None:
        _npc_sprite_sheet = pygame.image.load(NPC_SPRITE_SHEET).convert_alpha()
    return _npc_sprite_sheet

_overworld_sprite_sheet = None
def get_overworld_sprite_sheet():
    global _overworld_sprite_sheet
    if _overworld_sprite_sheet is None:
        _overworld_sprite_sheet = pygame.image.load(OVERWORLD_SPRITE_SHEET).convert_alpha()
    return _overworld_sprite_sheet

# --- Player Sprite Sheet Slicing ---
# Assume Boss.png is a grid: 4 rows (down, left, right, up), N columns (animation frames)
PLAYER_FRAME_WIDTH = 32  # Adjust if needed
PLAYER_FRAME_HEIGHT = 32  # Adjust if needed
PLAYER_DIRECTIONS = ['down', 'right', 'left', 'up']
PLAYER_FRAMES_PER_DIRECTION = 3  # Adjust if needed

def get_player_frame(direction: str, frame: int) -> pygame.Surface:
    """Return the correct player frame for direction and animation frame index."""
    sheet = get_player_sprite_sheet()
    if direction not in PLAYER_DIRECTIONS:
        direction = 'down'
    dir_idx = PLAYER_DIRECTIONS.index(direction)
    frame = frame % PLAYER_FRAMES_PER_DIRECTION
    rect = pygame.Rect(
        frame * PLAYER_FRAME_WIDTH,
        dir_idx * PLAYER_FRAME_HEIGHT,
        PLAYER_FRAME_WIDTH,
        PLAYER_FRAME_HEIGHT
    )
    return sheet.subsurface(rect).copy()

# --- Object/Environment Sprite Slicing ---
def get_object_sprite(x, y, w, h) -> pygame.Surface:
    """Extract a sprite from the objects.png sheet at (x, y) with size (w, h)."""
    sheet = get_objects_sprite_sheet()
    rect = pygame.Rect(x, y, w, h)
    return sheet.subsurface(rect).copy()

# Example: Define some common object sprites (coordinates must be set by inspecting objects.png)
# These coordinates are EXAMPLES. Adjust them to match your actual objects.png layout.
def get_chest_sprite():
    return get_object_sprite(32, 16, 16, 16)

def get_bush_sprite():
    return get_object_sprite(0, 120, 24, 24)

def get_rock_sprite():
    return get_object_sprite(64, 32, 16, 16)

# You can add more as needed, e.g. HEART_SPRITE, TREE_SPRITE, etc.

# --- NPC Sprite Sheet Slicing ---
NPC_FRAME_WIDTH = 24
NPC_FRAME_HEIGHT = 32
NPC_COLUMNS = 8
NPC_ROWS = 6
NPC_TOTAL = NPC_COLUMNS * NPC_ROWS  # 48

def get_npc_sprite(index: int) -> pygame.Surface:
    sheet = get_npc_sprite_sheet()
    if index < 0 or index >= NPC_TOTAL:
        index = 0
    col = index % NPC_COLUMNS
    row = index // NPC_COLUMNS
    rect = pygame.Rect(
        col * NPC_FRAME_WIDTH,
        row * NPC_FRAME_HEIGHT,
        NPC_FRAME_WIDTH,
        NPC_FRAME_HEIGHT
    )
    return sheet.subsurface(rect).copy()

# --- House Sprite from Overworld.png ---
def get_house_sprite():
    # Example: top-left house, adjust coordinates/size as needed
    sheet = get_overworld_sprite_sheet()
    rect = pygame.Rect(0, 0, 48, 48)  # (x, y, w, h) - adjust if house is larger/smaller
    return sheet.subsurface(rect).copy()

# --- Usage in Game ---
# For player: call get_player_frame(direction, frame) to get the correct image
# For objects: use CHEST_SPRITE, BUSH_SPRITE, etc. when creating GameObject instances
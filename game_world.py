# game_world.py - Creates and manages the game world

from config import SCREEN_WIDTH, SCREEN_HEIGHT, GREEN
from game_objects import GameArea, GameObject
from sprites import get_chest_sprite, get_bush_sprite, get_rock_sprite, get_npc_sprite, get_house_sprite
import random


# Create game world
def create_game_world():
    main_area = GameArea("Main Area", GREEN)

    # Add bushes and rocks around the edges for borders
    for i in range(0, SCREEN_WIDTH, 32):
        bush_top = GameObject(i, 0, 16, 16, get_bush_sprite(), "Bush")
        bush_bottom = GameObject(i, SCREEN_HEIGHT - 16, 16, 16, get_bush_sprite(), "Bush")
        main_area.add_object(bush_top)
        main_area.add_object(bush_bottom)
    for i in range(0, SCREEN_HEIGHT, 32):
        bush_left = GameObject(0, i, 16, 16, get_bush_sprite(), "Bush")
        bush_right = GameObject(SCREEN_WIDTH - 16, i, 16, 16, get_bush_sprite(), "Bush")
        main_area.add_object(bush_left)
        main_area.add_object(bush_right)

    # Add some rocks for variety
    for i in range(3):
        rock1 = GameObject(100 + i * 200, 100, 16, 16, get_rock_sprite(), "Rock")
        rock2 = GameObject(100 + i * 200, SCREEN_HEIGHT - 120, 16, 16, get_rock_sprite(), "Rock")
        main_area.add_object(rock1)
        main_area.add_object(rock2)

    # Add chests for About Me and Contact
    about_chest = GameObject(150, 300, 16, 16, get_chest_sprite(), "About Me Chest", "A treasure chest containing personal information.")
    main_area.add_object(about_chest)
    contact_chest = GameObject(450, 400, 16, 16, get_chest_sprite(), "Contact Information", "How to get in touch.")
    main_area.add_object(contact_chest)

    # Add NPCs using get_npc_sprite (random non-naked characters)
    used_indices = set()
    def get_unique_npc_index():
        idx = random.randint(0, 7)
        while idx in used_indices:
            idx = random.randint(0, 7)
        used_indices.add(idx)
        return idx
    skills_npc = GameObject(200, 200, 24, 32, get_npc_sprite(get_unique_npc_index()), "Skills Master", "I've heard you have impressive skills. Let me see them!")
    main_area.add_object(skills_npc)
    experience_npc = GameObject(400, 150, 24, 32, get_npc_sprite(get_unique_npc_index()), "Experience Sage", "Your work history tells an interesting story!")
    main_area.add_object(experience_npc)
    education_npc = GameObject(300, 350, 24, 32, get_npc_sprite(get_unique_npc_index()), "Knowledge Keeper", "Education is the foundation of growth.")
    main_area.add_object(education_npc)
    projects_npc = GameObject(500, 300, 24, 32, get_npc_sprite(get_unique_npc_index()), "Project Master", "Show me what you've built!")
    main_area.add_object(projects_npc)

    # House using the house sprite from Overworld.png
    house = GameObject(SCREEN_WIDTH - 200, 80, 48, 48, get_house_sprite(), "House", "Your home, where you've developed many of your projects.")
    main_area.add_object(house)

    return main_area
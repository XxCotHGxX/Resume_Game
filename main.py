# main.py - SNES-Style Interactive Resume Game

import pygame
import asyncio
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import game modules
from config import *
from player import Player
from game_world import create_game_world
from ui_systems import DialogSystem, MenuSystem, ResumeDisplay
from resume_data import RESUME_DATA

# Game state variables
game_running = True
in_main_menu = True
screen = None
clock = None
player = None
game_world = None
dialog_system = None
menu_system = None
resume_display = None
GAME_SURFACE = None
IS_FULLSCREEN = False


def initialize_game():
    """Initialize game systems and create game objects"""
    global screen, clock, player, game_world, dialog_system, menu_system, resume_display, GAME_SURFACE

    try:
        # Initialize Pygame
        logger.info("Starting game initialization...")
        if not pygame.get_init():
            pygame.init()

        # Initialize fonts and test
        success = initialize_fonts()
        if not success:
            raise RuntimeError("Font initialization failed")

        # Screen setup
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Interactive Resume - SNES Style")

        # Game clock
        clock = pygame.time.Clock()

        # Create game objects
        player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        game_world = create_game_world()
        dialog_system = DialogSystem()
        menu_system = MenuSystem()
        resume_display = ResumeDisplay()

        GAME_SURFACE = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        logger.info("Game initialization completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        return False


def handle_object_interaction(obj):
    """Handle interactions with game objects"""
    try:
        if obj.name == "Skills Master":
            resume_display.show_section("Skills", RESUME_DATA["SKILLS"])
        elif obj.name == "Experience Sage":
            resume_display.show_section("Experience", RESUME_DATA["EXPERIENCE"])
        elif obj.name == "Knowledge Keeper":
            resume_display.show_section("Education", RESUME_DATA["EDUCATION"])
        elif obj.name == "Project Master":
            resume_display.show_section("Projects", RESUME_DATA["PROJECTS"])
        elif obj.name == "About Me Chest":
            resume_display.show_section("About Me", None)
        elif obj.name == "Contact Information":
            resume_display.show_section("Contact", RESUME_DATA["CONTACT"])
        else:
            dialog_system.show_dialog(obj.name, obj.interaction_text)
    except Exception as e:
        logger.error(f"Error in object interaction: {str(e)}")


def handle_menu_selection(option):
    """Handle menu selection options"""
    global in_main_menu, game_running
    try:
        if in_main_menu:
            if option == "Start Game":
                in_main_menu = False
                dialog_system.show_dialog(
                    "Welcome",
                    f"Welcome to {RESUME_DATA['PLAYER_NAME']}'s interactive resume! "
                    "Walk around using WASD or arrow keys. "
                    "Interact with characters and objects using E or SPACE to learn more."
                )
            elif option == "About":
                dialog_system.show_dialog(
                    "About This Game",
                    "This interactive resume was created with Pygame to showcase my skills "
                    "and experience in a creative way. It features SNES-style graphics "
                    "inspired by games like The Legend of Zelda."
                )
            elif option == "Exit":
                game_running = False
        else:
            menu_system.close()
    except Exception as e:
        logger.error(f"Error in menu selection: {str(e)}")


def handle_menu_navigation(event):
    """Handle menu navigation inputs"""
    try:
        if event.key == pygame.K_UP:
            menu_system.move_selection(-1)
        elif event.key == pygame.K_DOWN:
            menu_system.move_selection(1)
        elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
            menu_system.select_current_option()
        elif event.key == pygame.K_ESCAPE:
            menu_system.close()
    except Exception as e:
        logger.error(f"Error in menu navigation: {str(e)}")


async def handle_keydown_event(event):
    """Handle keyboard input events"""
    global in_main_menu
    try:
        if dialog_system.active and event.key == pygame.K_SPACE:
            dialog_system.next_page()
        elif menu_system.active:
            handle_menu_navigation(event)
        elif resume_display.active and event.key == pygame.K_ESCAPE:
            resume_display.close()
        elif not in_main_menu and (event.key == pygame.K_e or event.key == pygame.K_SPACE):
            interaction_target = player.get_interaction_target(game_world.objects)
            if interaction_target:
                handle_object_interaction(interaction_target)
        elif not in_main_menu and event.key == pygame.K_ESCAPE:
            menu_system.show_menu("Paused", ["Resume", "Controls", "Exit"], handle_menu_selection)
        elif event.key == pygame.K_F11:
            toggle_fullscreen()
    except Exception as e:
        logger.error(f"Error handling keydown event: {str(e)}")


def render_game():
    """Handle game rendering"""
    try:
        target_surface = GAME_SURFACE if GAME_SURFACE is not None else screen
        if not in_main_menu:
            game_world.render(target_surface)
            player.render(target_surface)
        else:
            target_surface.fill(BLUE)
            title_text = create_pixel_text("Interactive Resume Game", large_font, YELLOW)
            target_surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

            subtitle_text = create_pixel_text(f"By {RESUME_DATA['PLAYER_NAME']}", medium_font, WHITE)
            target_surface.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 150))

        dialog_system.render(target_surface)
        menu_system.render(target_surface)
        resume_display.render(target_surface)
        # Scale to window
        window_size = screen.get_size()
        scaled_surface = pygame.transform.scale(target_surface, window_size)
        screen.blit(scaled_surface, (0, 0))

    except Exception as e:
        logger.error(f"Error in render_game: {str(e)}")


def toggle_fullscreen():
    global screen, IS_FULLSCREEN
    IS_FULLSCREEN = not IS_FULLSCREEN
    if IS_FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


async def main():
    """Main game loop"""
    global game_running, in_main_menu

    try:
        # Show initial menu
        menu_system.show_menu("Interactive Resume", ["Start Game", "About", "Exit"], handle_menu_selection)

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    await handle_keydown_event(event)

            if not (dialog_system.active or menu_system.active or
                    resume_display.active or in_main_menu):
                keys = pygame.key.get_pressed()
                player.update(keys, game_world.objects)

            render_game()
            pygame.display.flip()
            clock.tick(FPS)
            await asyncio.sleep(0)  # Required for browser deployment

    except Exception as e:
        logger.error(f"Error in main game loop: {str(e)}")
    finally:
        pygame.quit()
        return 0


if __name__ == "__main__":
    try:
        if initialize_game():
            asyncio.run(main())
        else:
            logger.error("Game initialization failed")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)
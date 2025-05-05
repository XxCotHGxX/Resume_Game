# config.py - Game configuration and constants

import pygame
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Screen dimensions
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (46, 139, 87)
BLUE = (25, 25, 112)
BROWN = (139, 69, 19)
YELLOW = (255, 223, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (173, 216, 230)

# Game settings
FPS = 60

# Font variables
small_font = None
medium_font = None
large_font = None


def get_font(size):
    """Helper function to get a font with multiple fallback options"""
    try:
        # First try: Look for specific fonts in order of preference
        for font_name in ['courier', 'arial', 'helvetica']:
            font_path = pygame.font.match_font(font_name)
            if font_path and os.path.exists(font_path):
                logger.info(f"Using font: {font_name} from {font_path}")
                return pygame.font.Font(font_path, size)

        # Second try: Use default system font
        default_font = pygame.font.get_default_font()
        if default_font:
            logger.info(f"Using default system font: {default_font}")
            return pygame.font.Font(default_font, size)

        # Last resort: Use SysFont
        logger.info("Falling back to SysFont")
        return pygame.font.SysFont(None, size)

    except Exception as e:
        logger.error(f"Error creating font of size {size}: {str(e)}")
        return pygame.font.SysFont(None, size)


def initialize_fonts():
    """Initialize fonts with multiple fallback options"""
    global small_font, medium_font, large_font
    logger.info("Initializing fonts...")

    # Ensure pygame is initialized
    if not pygame.get_init():
        logger.warning("Pygame not initialized, initializing now...")
        pygame.init()

    # Initialize font system specifically
    if not pygame.font.get_init():
        logger.warning("Font system not initialized, initializing now...")
        pygame.font.init()

    try:
        # Set up fonts with specific sizes
        small_font = get_font(16)
        medium_font = get_font(24)
        large_font = get_font(32)

        # Test each font
        for font, size in [(small_font, "small"), (medium_font, "medium"), (large_font, "large")]:
            test_surface = font.render("Test", True, WHITE)
            if test_surface is None:
                raise RuntimeError(f"{size} font failed rendering test")

        logger.info("All fonts initialized and tested successfully")
        return True

    except Exception as e:
        logger.error(f"Font initialization error: {str(e)}")
        # Set up emergency fallback fonts
        small_font = pygame.font.SysFont(None, 16)
        medium_font = pygame.font.SysFont(None, 24)
        large_font = pygame.font.SysFont(None, 32)
        logger.info("Using fallback system fonts")
        return True


def create_pixel_text(text, font, color):
    """Create a pixel art style text surface with fallback handling"""
    try:
        if font is None:
            logger.warning("Font is None, using fallback system font")
            font = pygame.font.SysFont(None, 32)

        text_surface = font.render(text, True, color)
        if text_surface is None:
            raise ValueError("Text surface is None after rendering")

        return text_surface

    except Exception as e:
        logger.error(f"Error in create_pixel_text: {str(e)}")
        emergency_font = pygame.font.SysFont(None, 32)
        return emergency_font.render(text, True, color)
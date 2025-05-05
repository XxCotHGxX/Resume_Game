# ui_systems.py - UI elements like dialog boxes, menus, and resume display

import pygame
from config import *
from sprites import get_player_frame  # Only import what is needed
from resume_data import RESUME_DATA

# Dialog box drawing function (moved from sprites.py)
def create_dialog_box(width, height):
    dialog_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    # Background
    pygame.draw.rect(dialog_surface, (0, 0, 128, 220), (0, 0, width, height))
    # Border
    pygame.draw.rect(dialog_surface, (255, 255, 255), (0, 0, width, height), 4)
    # Decorative corners
    pygame.draw.rect(dialog_surface, (255, 200, 0), (0, 0, 12, 12))
    pygame.draw.rect(dialog_surface, (255, 200, 0), (width - 12, 0, 12, 12))
    pygame.draw.rect(dialog_surface, (255, 200, 0), (0, height - 12, 12, 12))
    pygame.draw.rect(dialog_surface, (255, 200, 0), (width - 12, height - 12, 12, 12))
    return dialog_surface

# Dialog system
class DialogSystem:
    def __init__(self):
        self.active = False
        self.current_text = ""
        self.current_title = ""
        self.text_chunks = []
        self.dialog_box = create_dialog_box(SCREEN_WIDTH - 80, 150)
        self.dialog_box_rect = pygame.Rect(40, SCREEN_HEIGHT - 190, SCREEN_WIDTH - 80, 150)
        self.current_page = 0
        self.total_pages = 0

    def show_dialog(self, title, text):
        self.active = True
        self.current_title = title

        # Split text into pages
        self.text_chunks = []
        words = text.split()
        current_chunk = ""

        for word in words:
            test_chunk = current_chunk + " " + word if current_chunk else word
            if len(test_chunk) <= 250:  # Rough limit for text in dialog box
                current_chunk = test_chunk
            else:
                self.text_chunks.append(current_chunk)
                current_chunk = word

        if current_chunk:
            self.text_chunks.append(current_chunk)

        self.current_page = 0
        self.total_pages = len(self.text_chunks)
        self.current_text = self.text_chunks[0] if self.text_chunks else ""

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.current_text = self.text_chunks[self.current_page]
        else:
            self.active = False

    def render(self, screen):
        if not self.active:
            return

        # Draw dialog box
        screen.blit(self.dialog_box, (40, SCREEN_HEIGHT - 190))

        # Draw title
        title_text = create_pixel_text(self.current_title, medium_font, WHITE)
        screen.blit(title_text, (60, SCREEN_HEIGHT - 180))

        # Draw content text with word wrapping
        y_offset = SCREEN_HEIGHT - 150
        words = self.current_text.split()
        line = ""
        line_spacing = 24

        for word in words:
            test_line = line + word + " "
            text_width = small_font.size(test_line)[0]

            if text_width < SCREEN_WIDTH - 120:
                line = test_line
            else:
                text_surface = create_pixel_text(line, small_font, WHITE)
                screen.blit(text_surface, (60, y_offset))
                y_offset += line_spacing
                line = word + " "

        if line:
            text_surface = create_pixel_text(line, small_font, WHITE)
            screen.blit(text_surface, (60, y_offset))

        # Draw page indicator if multiple pages
        if self.total_pages > 1:
            page_text = create_pixel_text(f"Page {self.current_page + 1}/{self.total_pages}", small_font, WHITE)
            screen.blit(page_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 60))

        # Draw continue prompt
        continue_text = create_pixel_text("Press SPACE to continue", small_font, YELLOW)
        screen.blit(continue_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 60))


# Menu system
class MenuSystem:
    def __init__(self):
        self.active = False
        self.menu_name = ""
        self.options = []
        self.selected_index = 0
        self.callback = None

    def show_menu(self, name, options, callback=None):
        if not options:
            logger.warning("Empty options list provided to show_menu. Using default option.")
            options = ["No Options Available"]
        self.active = True
        self.menu_name = name
        self.options = options
        self.selected_index = 0
        self.callback = callback

    def move_selection(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.options)

    def select_current_option(self):
        if self.callback and 0 <= self.selected_index < len(self.options):
            self.callback(self.options[self.selected_index])

    def close(self):
        self.active = False

    def render(self, screen):
        if not self.active:
            return

        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # Draw title
        title_text = create_pixel_text(self.menu_name, large_font, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Draw options
        option_spacing = 40
        start_y = 150

        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_index else WHITE
            option_text = create_pixel_text(option, medium_font, color)

            # Draw selection indicator for current option
            if i == self.selected_index:
                pygame.draw.rect(screen, YELLOW,
                                 (SCREEN_WIDTH // 2 - option_text.get_width() // 2 - 15,
                                  start_y + i * option_spacing - 5,
                                  option_text.get_width() + 30,
                                  option_text.get_height() + 10), 3)

            screen.blit(option_text,
                        (SCREEN_WIDTH // 2 - option_text.get_width() // 2,
                         start_y + i * option_spacing))

        # Draw navigation instructions
        nav_text = create_pixel_text("↑/↓: Navigate   SPACE: Select   ESC: Back", small_font, WHITE)
        screen.blit(nav_text, (SCREEN_WIDTH // 2 - nav_text.get_width() // 2, SCREEN_HEIGHT - 50))


# Resume content display
class ResumeDisplay:
    def __init__(self):
        self.active = False
        self.current_section = None
        self.current_data = None

    def show_section(self, section, data):
        self.active = True
        self.current_section = section
        self.current_data = data

    def close(self):
        self.active = False

    def render(self, screen):
        if not self.active:
            return

        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 128, 200))
        screen.blit(overlay, (0, 0))

        # Draw section title
        title_text = create_pixel_text(self.current_section, large_font, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 30))

        # Draw content based on section type
        if self.current_section == "Skills":
            if self.current_data and isinstance(self.current_data, list):
                self.render_skills(screen)
            else:
                self.render_error(screen, "Skills data is missing or invalid.")
        elif self.current_section == "Experience":
            if self.current_data and isinstance(self.current_data, list):
                self.render_experience(screen)
            else:
                self.render_error(screen, "Experience data is missing or invalid.")
        elif self.current_section == "Education":
            if self.current_data and isinstance(self.current_data, list):
                self.render_education(screen)
            else:
                self.render_error(screen, "Education data is missing or invalid.")
        elif self.current_section == "Projects":
            if self.current_data and isinstance(self.current_data, list):
                self.render_projects(screen)
            else:
                self.render_error(screen, "Projects data is missing or invalid.")
        elif self.current_section == "Contact":
            if self.current_data and isinstance(self.current_data, dict):
                self.render_contact(screen)
            else:
                self.render_error(screen, "Contact data is missing or invalid.")
        elif self.current_section == "About Me":
            self.render_about(screen)

        # Draw navigation instructions
        nav_text = create_pixel_text("ESC: Back", small_font, WHITE)
        screen.blit(nav_text, (SCREEN_WIDTH - nav_text.get_width() - 20, SCREEN_HEIGHT - 40))

    def render_skills(self, screen):
        y_offset = 100
        max_bar_width = 250

        for skill in self.current_data:
            skill_name = create_pixel_text(f"{skill['name']}", medium_font, WHITE)
            screen.blit(skill_name, (150, y_offset))

            # Draw skill level bar
            bar_width = int(max_bar_width * skill['level'] / 100)
            pygame.draw.rect(screen, DARK_GRAY, (300, y_offset + 5, max_bar_width, 20))
            pygame.draw.rect(screen, YELLOW, (300, y_offset + 5, bar_width, 20))

            # Draw percentage
            level_text = create_pixel_text(f"{skill['level']}%", small_font, WHITE)
            screen.blit(level_text, (300 + max_bar_width + 10, y_offset + 5))

            y_offset += 40

    def render_experience(self, screen):
        y_offset = 100

        for job in self.current_data:
            # Title and company
            title_text = create_pixel_text(f"{job['title']} at {job['company']}", medium_font, WHITE)
            screen.blit(title_text, (80, y_offset))

            # Duration
            duration_text = create_pixel_text(job['duration'], small_font, YELLOW)
            screen.blit(duration_text, (80, y_offset + 30))

            # Description
            desc_text = create_pixel_text(job['description'], small_font, WHITE)
            screen.blit(desc_text, (80, y_offset + 55))

            # Divider
            pygame.draw.line(screen, GRAY, (80, y_offset + 85), (SCREEN_WIDTH - 80, y_offset + 85), 2)

            y_offset += 100

    def render_education(self, screen):
        y_offset = 100

        for edu in self.current_data:
            # Degree
            degree_text = create_pixel_text(edu['degree'], medium_font, WHITE)
            screen.blit(degree_text, (80, y_offset))

            # School and year
            school_text = create_pixel_text(f"{edu['school']} - {edu['year']}", small_font, YELLOW)
            screen.blit(school_text, (80, y_offset + 30))

            # Details
            details_text = create_pixel_text(edu['details'], small_font, WHITE)
            screen.blit(details_text, (80, y_offset + 55))

            # Divider
            pygame.draw.line(screen, GRAY, (80, y_offset + 85), (SCREEN_WIDTH - 80, y_offset + 85), 2)

            y_offset += 100

    def render_projects(self, screen):
        y_offset = 100

        for project in self.current_data:
            # Project name
            name_text = create_pixel_text(project['name'], medium_font, WHITE)
            screen.blit(name_text, (80, y_offset))

            # Technologies
            tech_text = create_pixel_text(f"Technologies: {project['tech']}", small_font, YELLOW)
            screen.blit(tech_text, (80, y_offset + 30))

            # Description
            desc_text = create_pixel_text(project['description'], small_font, WHITE)
            screen.blit(desc_text, (80, y_offset + 55))

            # Divider
            pygame.draw.line(screen, GRAY, (80, y_offset + 85), (SCREEN_WIDTH - 80, y_offset + 85), 2)

            y_offset += 100

    def render_contact(self, screen):
        y_offset = 120
        spacing = 50

        for key, value in self.current_data.items():
            # Format the key for display
            display_key = key.capitalize()

            # Draw key-value pair
            key_text = create_pixel_text(f"{display_key}:", medium_font, YELLOW)
            screen.blit(key_text, (150, y_offset))

            value_text = create_pixel_text(value, medium_font, WHITE)
            screen.blit(value_text, (300, y_offset))

            y_offset += spacing

    def render_about(self, screen):
        player_name = RESUME_DATA["PLAYER_NAME"]
        player_title = RESUME_DATA["PLAYER_TITLE"]
        personal_summary = RESUME_DATA["PERSONAL_SUMMARY"]

        title_text = create_pixel_text(player_name, large_font, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        role_text = create_pixel_text(player_title, medium_font, YELLOW)
        screen.blit(role_text, (SCREEN_WIDTH // 2 - role_text.get_width() // 2, 150))

        # Split summary into lines for display
        words = personal_summary.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            if small_font.size(test_line)[0] < SCREEN_WIDTH - 160:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        y_offset = 200
        for line in lines:
            line_text = create_pixel_text(line, small_font, WHITE)
            screen.blit(line_text, (SCREEN_WIDTH // 2 - line_text.get_width() // 2, y_offset))
            y_offset += 30

        # Display player sprite larger
        scaled_player = pygame.transform.scale(get_player_frame(0), (128, 128))
        screen.blit(scaled_player, (SCREEN_WIDTH // 2 - 64, 300))

    def render_error(self, screen, message):
        error_text = create_pixel_text(message, medium_font, YELLOW)
        screen.blit(error_text, (SCREEN_WIDTH // 2 - error_text.get_width() // 2, 100))
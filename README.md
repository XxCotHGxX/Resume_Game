# SNES-Style Interactive Resume Game

This project is a Super Nintendo-style game that serves as an interactive resume, inspired by games like The Legend of Zelda: A Link to the Past. It uses Pygame and can be deployed to the web using Pygbag.

## Overview

This game allows you to showcase your skills, experience, and education in a creative and engaging way. Visitors to your website can explore a small game world and interact with characters and objects to learn more about your professional background.

## Features

- SNES-style pixel art graphics
- Interactive game world to explore
- NPCs and objects that provide information about your skills, experience, education, and projects
- Dialog system with paged text
- Menu system for navigation
- Responsive controls (keyboard)
- Web-deployable using Pygbag

## File Structure

- `main.py` - Main entry point for the game
- `config.py` - Game configuration and constants
- `resume_data.py` - Your personal resume information
- `sprites.py` - Functions to create game sprites
- `player.py` - Player character class
- `game_objects.py` - Game world object classes
- `game_world.py` - Game world creation and management
- `ui_systems.py` - UI elements like dialog boxes, menus, and resume display

## Getting Started

1. Update `resume_data.py` with your personal information, including:
   - Name and title
   - Skills
   - Work experience
   - Education
   - Projects
   - Contact information

2. Install dependencies:
   ```
   pip install pygame
   pip install pygbag  # For web deployment
   ```

3. Run the game locally:
   ```
   python main.py
   ```

4. Deploy to the web:
   ```
   python -m pygbag path_to_folder_containing_main_py
   ```
   
   After running this command, Pygbag will start a local server with your game. It will also create a `build/web` directory that contains all the files needed for web deployment.

5. Upload the contents of the `build/web` directory to your web hosting service or GitHub Pages to make your game accessible online.

## Controls

- **Arrow keys** or **WASD**: Move the player character
- **E** or **Space**: Interact with objects/characters
- **Space**: Continue dialog
- **Escape**: Open menu or go back
- **Up/Down arrows**: Navigate menus
- **Space** or **Enter**: Select menu option

## Customization

- Modify the sprites in `sprites.py` to change the game's appearance
- Add more objects or NPCs to `game_world.py`
- Extend the game with new areas or game mechanics

## Web Deployment Tips

- Keep file sizes small for faster loading on the web
- Test your game in different browsers and on mobile devices
- Include clear instructions for users who may not be familiar with games

## Credits

This interactive resume game was created with Pygame and uses Pygbag for web deployment. It's designed to showcase your professional skills in a creative way.

## License

This project is released under the MIT License.

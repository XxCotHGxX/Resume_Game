# player.py - Player character class

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT
from sprites import get_player_frame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.speed = 3
        self.direction = 'down'  # down, left, right, up
        self.anim_frame = 0
        self.anim_timer = 0
        self.anim_speed = 8  # Lower is faster
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, keys, objects):
        new_x, new_y = self.x, self.y
        moved = False
        prev_direction = self.direction

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= self.speed
            self.direction = 'left'
            moved = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += self.speed
            self.direction = 'right'
            moved = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= self.speed
            self.direction = 'up'
            moved = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += self.speed
            self.direction = 'down'
            moved = True

        # Check if new position would result in collision
        temp_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        collision = False
        for obj in objects:
            if obj.rect.colliderect(temp_rect):
                collision = True
                break
        if not collision:
            self.x, self.y = new_x, new_y
            self.rect.x, self.rect.y = new_x, new_y

        # Keep player within screen bounds
        self.x = max(0, min(SCREEN_WIDTH - self.width, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - self.height, self.y))
        self.rect.x, self.rect.y = self.x, self.y

        # Animation logic
        if moved:
            self.anim_timer += 1
            if self.anim_timer >= self.anim_speed:
                self.anim_frame = (self.anim_frame + 1) % 3  # 3 frames per direction
                self.anim_timer = 0
        else:
            self.anim_frame = 1  # Idle frame (usually the middle one)

    def render(self, screen):
        frame = get_player_frame(self.direction, self.anim_frame)
        screen.blit(frame, (self.x, self.y))

    def get_interaction_target(self, objects):
        # Check for objects in front of the player
        interaction_range = 20
        dx, dy = 0, 0
        if self.direction == 'up':
            dy = -interaction_range
        elif self.direction == 'down':
            dy = interaction_range
        elif self.direction == 'left':
            dx = -interaction_range
        elif self.direction == 'right':
            dx = interaction_range
        interaction_rect = pygame.Rect(
            self.x + dx - interaction_range // 2,
            self.y + dy - interaction_range // 2,
            self.width + interaction_range,
            self.height + interaction_range
        )
        for obj in objects:
            if interaction_rect.colliderect(obj.rect):
                return obj
        return None
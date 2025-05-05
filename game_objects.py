# game_objects.py - Classes for game world and objects

import pygame


# Game objects
class GameObject:
    def __init__(self, x, y, width, height, sprite=None, name="Object", interaction_text=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprite = sprite
        self.name = name
        self.interaction_text = interaction_text
        self.rect = pygame.Rect(x, y, width, height)

    def render(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height))

    def contains_point(self, x, y):
        return self.rect.collidepoint(x, y)

    def interact(self):
        return self.interaction_text


# Define game areas/scenes
class GameArea:
    def __init__(self, name, background_color, objects=None):
        self.name = name
        self.background_color = background_color
        self.objects = objects if objects else []

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self, screen):
        screen.fill(self.background_color)
        for obj in self.objects:
            obj.render(screen)
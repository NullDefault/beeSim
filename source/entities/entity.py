"""
Class Name: Entity
Class Purpose: Super class for all Entities, holds data common to all game entities
Notes:
"""

#  IMPORTS
import pygame
from source.entities import sprite_bank


class Entity(pygame.sprite.Sprite):

#  FUNCTIONS

    def __init__(self, location, base_sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_bank.retrieve(base_sprite)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

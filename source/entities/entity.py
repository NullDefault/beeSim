"""
Class Name: Entity
Class Purpose: Super class for all Entities, holds data common to all game entities
Notes:
"""

from pygame.sprite import DirtySprite

from source.entities import sprite_bank


class Entity(DirtySprite):

    def __init__(self, location, base_sprite):
        DirtySprite.__init__(self)
        try:
            self.image = sprite_bank.retrieve(base_sprite)
        except KeyError:
            self.image = base_sprite
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

import pygame
from source import beeHiveData


class Bee(pygame.sprite.Sprite):

    queenHive = beeHiveData.BeeHive

    def __init__(self, location, queen):
        queenHive = queen
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/beeSprite.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


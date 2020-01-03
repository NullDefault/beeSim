import pygame
import random


class Flower(pygame.sprite.DirtySprite):

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        random_type = random.randint(0, 5)
        self.image = pygame.image.load("assets/flower_sprites/flower_sprites"+str(random_type)+".png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.pollen = 100

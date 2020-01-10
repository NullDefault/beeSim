import pygame
from random import randint


class Flower(pygame.sprite.DirtySprite):

    def __init__(self, location, growth_stage=None):
        pygame.sprite.Sprite.__init__(self)
        if growth_stage is None:
            growth_stage = randint(0, 5)
        else:
            growth_stage = growth_stage
        self.image = pygame.image.load("assets/flower_sprites/flower_sprites"+str(growth_stage)+".png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

        self.occupied = False
        self.pollen = 100

        self.neighbors = None

    def set_neighbors(self, neighbors_list):
        self.neighbors = neighbors_list

    def begin_harvest(self):
        self.occupied = True

    def finish_harvest(self):
        self.occupied = False
        pollen_gain_rate = 10
        pollen_taken = self.pollen - pollen_gain_rate  # pollen_gain_rate is eventually going to have a formula
        self.pollen = self.pollen - pollen_taken

        return pollen_taken

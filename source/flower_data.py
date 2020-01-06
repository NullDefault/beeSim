import pygame
import random


class Flower(pygame.sprite.DirtySprite):

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        random_type = random.randint(0, 5)
        self.image = pygame.image.load("assets/flower_sprites/flower_sprites"+str(random_type)+".png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

        self.occupied = False
        self.pollen = 100

    def begin_harvest(self):
        self.occupied = True

    def finish_harvest(self):
        self.occupied = False
        pollen_gain_rate = 10
        pollen_taken = self.pollen - pollen_gain_rate  # pollen_gain_rate is eventually going to have a formula
        self.pollen = self.pollen - pollen_taken

        return pollen_taken

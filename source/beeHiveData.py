import pygame
import random


class BeeHive(pygame.sprite.DirtySprite):

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/beeHive_sprites/beeHive_red.png")
        self.dirty = 0
        self.rect = self.image.get_rect()
        self.known_flowers = []
        self.rect.left, self.rect.top = location

    def remember_flower(self, flower):
        self.known_flowers.append(flower)

    def has_orders(self):
        if len(self.known_flowers) == 0:
            return False
        else:
            return True

    def get_order(self):
        random_index = random.randint(0, len(self.known_flowers)-1)
        flower_ordered = self.known_flowers[random_index]
        return flower_ordered.rect.left + 8, flower_ordered.rect.top + 8




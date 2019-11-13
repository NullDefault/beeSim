import pygame
import math
import random


class Bee(pygame.sprite.Sprite):

    hungry = False
    queen_hive = None

    def __init__(self, location, queen):
        self.queen_hive = queen
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/beeSprite.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def move(self):
        self.look_for_nectar(.1)  # TODO - implement gather / return cycle

    def look_for_nectar(self, angle):
        random_x_offset = random.randint(-3, 3)
        random_y_offset = random.randint(-3, 3)

        ox = self.queen_hive.position[0]
        oy = self.queen_hive.position[1]

        px, py = self.rect.left, self.rect.top

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

        self.rect.left = qx + random_x_offset
        self.rect.top = qy + random_y_offset




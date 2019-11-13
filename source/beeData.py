import pygame
import math
import random


class Bee(pygame.sprite.Sprite):

    left_sprite = pygame.image.load("assets/beeSprite_left.png")
    right_sprite = pygame.image.load("assets/beeSprite_right.png")
    up_sprite = pygame.image.load("assets/beeSprite_up.png")
    down_sprite = pygame.image.load("assets/beeSprite_down.png")

    turn_timer = 0
    hungry = False
    queen_hive = None

    def __init__(self, location, queen):
        self.queen_hive = queen
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/beeSprite_down.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def move(self):
        self.look_for_nectar(0.036)  # TODO - implement gather / return cycle

    def look_for_nectar(self, angle):

        random_x_offset = random.randint(-2, 2)
        random_y_offset = random.randint(-2, 2)

        ox = self.queen_hive.position[0] + 33 # 33 is half the hive sprite
        oy = self.queen_hive.position[1] + 33

        px, py = self.rect.left, self.rect.top

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

        self.update_sprite(px, py, qx, qy)

        self.rect.left = qx + random_x_offset
        self.rect.top = qy + random_y_offset

    def update_sprite(self, origin_x, origin_y, end_x, end_y):

        x_distance = end_x - origin_x
        y_distance = end_y - origin_y
        if abs(x_distance) > abs(y_distance):
            if x_distance < -0:
                self.image = self.left_sprite
            else:
                self.image = self.right_sprite
        else:
            if y_distance < -0:
                self.image = self.up_sprite
            else:
                self.image = self.down_sprite



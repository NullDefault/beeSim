import pygame
import math
import random
from fysom import *


class Bee(pygame.sprite.Sprite):
########################################################################################################################
# Class Fields

    left_sprite = pygame.image.load("assets/beeSprite_left.png")
    right_sprite = pygame.image.load("assets/beeSprite_right.png")
    up_sprite = pygame.image.load("assets/beeSprite_up.png")
    down_sprite = pygame.image.load("assets/beeSprite_down.png")

    wiggle = 1
    speed = 4
    roam_percentages = (0.64, 0.36)

################################################################## ######################################################

    def __init__(self, location, queen, type):

        self.queen_hive = queen
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/beeSprite_down.png")
        self.target_destination = None

        # await orders (flowers available > go to flower) | (no flowers available > await orders)
        # go to flower  (arrived at flower > harvest pollen)
        # harvest pollen (flower is out of pollen > look nearby) | (full of pollen > head to hive)
        # look nearby   (flower found > harvest pollen) | (no flower found > head to hive)
        # head to hive  (arrived at hive > offload)
        # offload   (flowers available > go to flower) | (no flowers available > await orders)
        if type == "worker":
            self.bee_states = Fysom({
                'initial': 'await orders',
                'events': [
                    {'name': 'flowers available', 'src': 'await orders', 'dst': 'go to flower'},
                    {'name': 'no flowers available', 'src': 'await orders', 'dst': 'await orders'},
                    {'name': 'arrived at flower', 'src': 'go to flower', 'dst': 'harvest pollen'},
                    {'name': 'flower is out of pollen', 'src': 'harvest pollen', 'dst': 'look nearby'},
                    {'name': 'full of pollen', 'src': 'harvest pollen', 'dst': 'head to hive'},
                    {'name': 'flower found', 'src': 'look nearby', 'dst': 'harvest pollen'},
                    {'name': 'no flower found', 'src': 'look nearby', 'dst': 'head to hive'},
                    {'name': 'arrived at hive', 'src': 'head to hive', 'dst': 'offload'},
                    {'name': 'flowers available', 'src': 'offload', 'dst': 'go to flower'},
                    {'name': 'no flowers available', 'src': 'offload', 'dst': 'await orders'},
                ]
            })
        # look for flowers (found flower > head to hive) | (no flower found > head to hive)
        # dance (dance complete > look for flowers)
        # head to hive (arrived at hive > dance)
        else:
            self.bee_states = Fysom({
                'initial': 'look for flowers',
                'events': [
                    {'name': 'found flower', 'src': 'look for flowers', 'dst': 'head to hive'},
                    {'name': 'no flower found', 'src': 'look for flowers', 'dst': 'head to hive'},
                    {'name': 'arrive at hive', 'src': 'head to hive', 'dst': 'dance'},
                    {'name': 'dance complete', 'src': 'dance', 'dst': 'look for flowers'}
                ]
            })
        self.current_nectar = 0
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.random_spin_affinity = random.randint(0, 1)
########################################################################################################################

    def move(self):
        if self.bee_states.current == "await orders":
            self.head_towards((self.queen_hive.rect.left + 33, self.queen_hive.rect.top + 52))

########################################################################################################################

    def head_towards(self, target_destination):

        x_distance = target_destination[0] - (self.rect.left + 5)
        y_distance = target_destination[1] - (self.rect.top + 4)

        dx = 0
        dy = 0

        movement_points_to_spend = self.speed

        while True:
            if movement_points_to_spend == 0:
                break
            coin_flip = random.randint(0, 1)
            if coin_flip == 0:
                dx = dx + 1
            else:
                dy = dy + 1

            movement_points_to_spend = movement_points_to_spend - 1

        if x_distance < 0:
            dx = -dx
        if y_distance < 0:
            dy = -dy

        if -4 < x_distance < 4:
            dx = 0
        if -4 < y_distance < 4:
            dy = 0

        random_x_offset = random.randint(-self.wiggle, self.wiggle)
        random_y_offset = random.randint(-self.wiggle, self.wiggle)
        self.rect.top = self.rect.top + dy + random_x_offset
        self.rect.left = self.rect.left + dx + random_y_offset
























    def orbit_hive(self, angle):

        random_x_offset = random.randint(-2, 2)
        random_y_offset = random.randint(-2, 2)

        ox = self.queen_hive.position[0] + 33
        oy = self.queen_hive.position[1] + 52

        px, py = self.rect.left, self.rect.top

        if self.random_spin_affinity == 0:
            qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
            qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        else:
            qx = ox + math.cos(-angle) * (px - ox) - math.sin(-angle) * (py - oy)
            qy = oy + math.sin(-angle) * (px - ox) + math.cos(-angle) * (py - oy)

        self.update_sprite(px, py, qx, qy)

        self.rect.left = qx + random_x_offset
        self.rect.top = qy + random_y_offset
########################################################################################################################

    def update_sprite(self, origin_x, origin_y, end_x, end_y):

        x_distance = end_x - origin_x
        y_distance = end_y - origin_y

        if abs(x_distance) > abs(y_distance):
            if x_distance < 0:
                self.image = self.left_sprite
            else:
                self.image = self.right_sprite
        else:
            if y_distance < 0:
                self.image = self.up_sprite
            else:
                self.image = self.down_sprite



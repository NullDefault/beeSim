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

    hungry = False
    queen_hive = None

    speed = 5

    roam_percentages = (0.64, 0.36)
    target_destination = ()
    random_spin_affinity = 0

# The field below is a finite state machine which decides the bees behavior at the moment
# the progression is roam > (find flower) > gather > (full of pollen) > head home > (arrived at hive) > offload > roam
#                                                  > (still hungry) > roam
    bee_states = Fysom({'initial': 'roam',
                        'events': [
                            {'name': 'found flower', 'src': 'roam', 'dst': 'gather'},
                            {'name': 'full of pollen', 'src': 'gather', 'dst': 'head home'},
                            {'name': 'still hungry', 'src': 'gather', 'dst': 'roam'},
                            {'name': 'arrived at hive', 'src': 'head home', 'dst': 'offload'},
                            {'name': 'done offloading', 'src': 'offload', 'dst': 'roam'},
                        ]})
########################################################################################################################

    def __init__(self, location, queen):
        self.queen_hive = queen
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/beeSprite_down.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.random_spin_affinity = random.randint(0, 1)
########################################################################################################################

    def move(self):
        if self.bee_states.current == 'roam':
                self.orbit_hive(0.036)
########################################################################################################################

    def head_towards(self):
        self_x = self.rect.left
        self_y = self.rect.top

        goal_x = self.target_destination[0]
        goal_y = self.target_destination[1]

        total_x_distance = goal_x - self_x
        total_y_distance = goal_y - self_y

        if total_x_distance == 0 or total_y_distance == 0:
            print(str(self.target_destination))
        else:
            x_delta = self.speed / total_x_distance
            y_delta = self.speed / total_y_distance

            self.rect.left = self_x + x_delta
            self.rect.top = self_y + y_delta

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



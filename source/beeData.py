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

    search_radius = 300
    wiggle = 1
    speed = 4
    roam_percentages = (0.64, 0.36)

########################################################################################################################

    def __init__(self, location, queen, type):

        self.queen_hive = queen
        self.queen_hive_x = queen.rect.left + 33
        self.queen_hive_y = queen.rect.top + 52
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
        # look for flowers (begin search > looking for flowers)
        # looking for flowers (found flower > head to hive) | (no flower found > head to hive)
        # dance (dance complete > look for flowers)
        # head to hive (arrived at hive > dance)
        else:
            self.bee_states = Fysom({
                'initial': 'look for flowers',
                'events': [
                    {'name': 'begin search', 'src': 'look for flowers', 'dst': 'looking for flowers'},
                    {'name': 'found flower', 'src': 'looking for flowers', 'dst': 'head to hive'},
                    {'name': 'no flower found', 'src': 'looking for flowers', 'dst': 'head to hive'},
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
        self.target_destination = self.update_target(self.bee_states.current)
        self.head_towards()
        self.update_sprite()

########################################################################################################################

    def update_target(self, origin_state):
        return {
            'await orders': self.go_to_hive(),
            'go to flower': (),  # TODO: Pick a random flower from the known_flowers array and return its location
            'harvest pollen': (),  # TODO: Sit on top of the flower and collect its pollen
            'look nearby': (),  # TODO: Search the nearby location for more flowers
            'head to hive': self.go_to_hive(),
            'offload': self.go_to_hive(),
            'look for flowers': self.search_for_flowers(),  # TODO: Search for flowers
            'looking for flowers': self.target_destination,
            'dance': (),  # TODO: Do a cute lil dance
        }[origin_state]

    def go_to_hive(self):
        return self.queen_hive_x, self.queen_hive_y

    def search_for_flowers(self):

        if self.bee_states.current == 'look for flowers':

            self.bee_states.trigger("begin search")

            r = self.search_radius * math.sqrt(random.random())
            theta = random.random() * 2 * math.pi

            if random.randint(0, 1) == 0:
                random_x_coordinate = self.queen_hive_x + (r * math.cos(theta))
            else:
                random_x_coordinate = self.queen_hive_x - (r * math.cos(theta))
            if random.randint(0, 1) == 1:
                random_y_coordinate = self.queen_hive_y + (r * math.sin(theta))
            else:
                random_y_coordinate = self.queen_hive_y - (r * math.sin(theta))

            return random_x_coordinate, random_y_coordinate

        elif self.bee_states.current == 'looking for flowers':

            x_distance = abs(self.target_destination[0] - (self.rect.left + 5))
            y_distance = abs(self.target_destination[1] - (self.rect.top + 4))

            if x_distance < 10 or y_distance < 10:
                self.bee_states.trigger('no flower found')
                self.bee_states.trigger('arrive at hive')
                self.bee_states.trigger('dance complete')

        # go to random point within the search range
        # search the adjacent area
        # if flower found > report to hive
        # if no flower found > go back to hive

    def head_towards(self):

        x_distance = self.target_destination[0] - (self.rect.left + 5)
        y_distance = self.target_destination[1] - (self.rect.top + 4)

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

        ox = self.queen_hive_x
        oy = self.queen_hive_y

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

    def update_sprite(self):

        x_distance = self.target_destination[0] - self.rect.left
        y_distance = self.target_destination[1] - self.rect.top

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



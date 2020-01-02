import pygame
import math
import random
from source.beeData import Bee
from random import randint
from fysom import *


class WorkerBee(Bee):

    def __init__(self, location, queen):
        self.max_nectar_capacity = 100
        self.current_nectar = 0
        self.random_spin_affinity = randint(0, 1)
        self.bee_states = Fysom({
            # await orders > harvest > offload >...
            'initial': 'await orders',
            'events': [
                {'name': 'go to flower', 'src': 'await orders', 'dst': 'harvest'},
                {'name': 'harvest complete', 'src': 'harvest', 'dst': 'offload'},
                {'name': 'offload complete', 'src': 'offload', 'dst': 'await orders'}
            ]
        })
        Bee.__init__(self, location, queen)

    def deliver_nectar_load(self):
        if pygame.sprite.collide_rect(self, self.queen_hive):

            self.queen_hive.gain_nectar(self.current_nectar)
            self.current_nectar = 0

            self.bee_states.trigger('offload complete')
            return self.queen_hive_x, self.queen_hive_y
        else:
            return self.target_destination

    def orbit_hive(self):

        angle = 0.36  # Magic Number - tune for speed of orbit

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

        shipBack = (qx + random_x_offset, qy + random_y_offset)
        return shipBack

    def harvest_flower(self):
        if self.current_nectar < self.max_nectar_capacity:
            if self.target_destination[0] - 10 <= self.rect.left <= self.target_destination[0] + 10 and \
                    self.target_destination[1] - 10 <= self.rect.top <= self.target_destination[1] + 10:
                self.current_nectar = self.current_nectar + 10
                return self.target_destination
            else:
                return self.target_destination
        else:
            self.bee_states.trigger('harvest complete')
            return self.queen_hive_x, self.queen_hive_y

    def check_available_orders(self):
        if self.queen_hive.has_orders():
            self.bee_states.trigger('go to flower')
            return self.queen_hive.get_order()
        else:
            return self.orbit_hive()
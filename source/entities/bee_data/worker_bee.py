"""
Class Name: Worker Bee
Class Purpose: Bee subclass which harvests flowers and does other work
Notes:
"""

# IMPORTS
from math import cos, sin
from pygame import image, sprite
from random import randint
from source.entities.bee_data.bee import Bee
from source.entities.bee_data.castes import worker_fysom

# CLASS BODY


class WorkerBee(Bee):

    #  FUNCTIONS

    def __init__(self, location, queen):

        self.max_nectar_capacity = 1  # Max nectar the worker can carry
        self.current_nectar = 0  # Current nectar on bee-hand

        self.target_flower = None  # Variables used in the harvesting process
        self.harvesting_pollen = False
        self.begin_harvest_time = 0
        self.harvesting_duration = randint(2000, 4000)

        self.offloading = False  # Variables used in the offloading process
        self.begin_offload_time = 0
        self.offloading_duration = randint(2000, 5000)

        self.random_spin_affinity = randint(0, 1)  # Which way the bee will randomly orbit the hive

        self.bee_states = worker_fysom()  # Assigns the behavioral finite state machine

        Bee.__init__(self, location, queen)

    def move(self):
        self.target_destination = self.update_target(self.bee_states.current)
        self.head_towards()
        self.update_sprite()

    def deliver_nectar_load(self):
        if self.queen_hive.center[0] - 10 <= self.rect.left <= self.queen_hive.center[0] + 10 and \
           self.queen_hive.center[1] - 6 <= self.rect.top <= self.queen_hive.center[1] + 6:
            self.queen_hive.gain_nectar(self.current_nectar)
            self.current_nectar = 0

            self.bee_states.trigger('begin offload')
            return self.queen_hive.center
        else:
            return self.queen_hive.center

    def offload(self):
        if not self.offloading:
            self.offloading = True
            self.begin_offload_time = self.queen_hive.last_tick
        else:
            current_time = self.queen_hive.last_tick
            if current_time >= self.begin_offload_time + self.offloading_duration:
                self.offloading = False
                self.begin_offload_time = 0
                self.bee_states.trigger('offload complete')

        return self.queen_hive.center

    def orbit_hive(self):  # Spin around a hive

        angle = 0.36  # Magic Number - tune for speed of orbit

        random_x_offset = randint(-2, 2)
        random_y_offset = randint(-2, 2)

        ox = self.queen_hive_x
        oy = self.queen_hive_y

        px, py = self.rect.left, self.rect.top

        if self.random_spin_affinity == 0:
            qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
            qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
        else:
            qx = ox + cos(-angle) * (px - ox) - sin(-angle) * (py - oy)
            qy = oy + sin(-angle) * (px - ox) + cos(-angle) * (py - oy)

        ship_back = (qx + random_x_offset, qy + random_y_offset)
        return ship_back

    def harvest_flower(self):
        if self.current_nectar < self.max_nectar_capacity:
            if sprite.collide_rect(self, self.target_flower):
                self.harvest_nectar_from(self.target_flower)
                self.wiggle = 0
                return self.target_flower.rect.left + 9, self.target_flower.rect.top + 6
            else:
                return self.target_flower.rect.left + 9, self.target_flower.rect.top + 6
        else:
            self.wiggle = 1
            self.bee_states.trigger('harvest complete')
            return self.queen_hive_x, self.queen_hive_y

    def harvest_nectar_from(self, flower):
        if not self.harvesting_pollen:
            self.harvesting_pollen = True
            flower.begin_harvest()
            self.begin_harvest_time = self.queen_hive.last_tick
        else:
            current_time = self.queen_hive.last_tick
            if current_time >= self.begin_harvest_time + self.harvesting_duration:
                self.harvesting_pollen = False
                self.current_nectar = self.current_nectar + flower.finish_harvest()

    def check_available_orders(self):
        if self.queen_hive.has_orders():
            self.target_flower = self.queen_hive.get_order()
            self.bee_states.trigger('go to flower')
            return self.target_flower.rect.left, self.target_flower.rect.top
        else:
            return self.orbit_hive()

"""
Class Name: Worker Bee
Class Purpose: Bee subclass which harvests flowers and does other work
Notes:
"""

# IMPORTS
from math import cos, sin
from random import randint
from pygame import sprite, Vector2

from source.entities.bee_data.bee import Bee
from source.entities.bee_data.bee_components.castes import worker_fysom


# CLASS BODY


class WorkerBee(Bee):

    #  FUNCTIONS

    def __init__(self, location, queen):

        Bee.__init__(self, location, queen)

        self.max_nectar_capacity = 10  # Max nectar the worker can carry
        self.current_nectar = 0

        self.spin_affinity = randint(0, 1)  # Decides if the bee will orbit the hive clock or counter-clock wise

        self.target_flower = None  # Variables used in the harvesting process
        self.harvesting_pollen = False
        self.begin_harvest_time = 0

        self.offloading = False  # Variables used in the offloading process
        self.begin_offload_time = 0

        self.state_machine = worker_fysom()  # Assigns the behavioral finite state machine

    def update(self):
        """
        Runs once per frame
        :return: void
        """
        self.target_destination = self.update_target()
        if not self.harvesting_pollen and not self.offloading:
            self.head_towards()
        self.update_sprite()

    def update_target(self):
        if self.state == 'await orders':
            return self.check_available_orders()
        elif self.state == 'harvest':
            return self.harvest_flower()
        elif self.state == 'offload':
            return self.offload()
        elif self.state == 'head back':
            return self.deliver_nectar_load()

    def deliver_nectar_load(self):
        """
        Makes the worker go back to his hive ot drop off nectar
        :return: Center of its hive
        """
        if self.location.distance_to(self.queen_hive.center) < self.rect.width / 2:
            self.queen_hive.gain_nectar(self.current_nectar)
            self.current_nectar = 0

            if self.target_flower.pollen > 0:
                self.queen_hive.flowers_getting_harvested.remove(self.target_flower)
                self.queen_hive.remember_flower(self.target_flower)
            else:
                self.queen_hive.flowers_getting_harvested.remove(self.target_flower)
                self.target_flower.stop_inspection(self.queen_hive)

            self.state_machine.trigger('begin offload')
            self.rect.left = self.queen_hive.center.x + randint(-1, 1)
            self.rect.top = self.queen_hive.center.y + randint(-1, 1)
            return self.queen_hive.center
        else:
            return self.queen_hive.center

    def offload(self):
        """
        Offloads nectar
        :return: Center of the hive
        """
        if not self.offloading:
            self.offloading = True
            self.begin_offload_time = self.queen_hive.last_tick
        else:
            current_time = self.queen_hive.last_tick
            if current_time >= self.begin_offload_time + randint(2000, 5000):
                self.offloading = False
                self.begin_offload_time = 0
                self.state_machine.trigger('offload complete')

        return self.queen_hive.center

    def orbit_hive(self):
        """
        Spin around the hive
        :return: Next location on the orbit trajectory
        """
        angle = 0.4  # Magic Number - tune for speed of orbit

        random_x_offset = randint(-2, 2)
        random_y_offset = randint(-2, 2)

        ox, oy = self.hive_location.x, self.hive_location.y - 54
        px, py = self.rect.left + 9, self.rect.top + 9  # 9 is half the sprite size

        if self.spin_affinity == 0:
            qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy)
            qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy)
        else:
            qx = ox + cos(-angle) * (px - ox) - sin(-angle) * (py - oy)
            qy = oy + sin(-angle) * (px - ox) + cos(-angle) * (py - oy)

        next_orbit_point = Vector2(qx + random_x_offset, qy + random_y_offset)
        return next_orbit_point

    def harvest_flower(self):
        """
        Harvest nectar
        :return: If harvesting isn't done yet, the location of the flower. Otherwise, go to the hive.
        """
        if self.current_nectar < self.max_nectar_capacity:
            if sprite.collide_rect(self, self.target_flower):
                self.start_harvesting_from(self.target_flower)
            if self.target_flower.pollen <= 0:
                self.state_machine.trigger('harvest complete')
            return Vector2(self.target_flower.rect.left + randint(0, self.target_flower.rect.width),
                           self.target_flower.rect.top + randint(0, self.target_flower.rect.height))
        else:
            self.target_flower.busy = False
            self.state_machine.trigger('harvest complete')
            return Vector2(self.hive_location.x, self.hive_location.y)

    def start_harvesting_from(self, flower):
        """
        Starts the harvesting process
        :param flower:
        :return: void
        """
        if not self.harvesting_pollen:
            self.rect.left = flower.rect.left + self.target_flower.rect.width/3 + randint(-2, 2)
            self.rect.top = flower.rect.top + self.target_flower.rect.height/3 + randint(-2, 2)
            self.harvesting_pollen = True
            self.begin_harvest_time = self.queen_hive.last_tick
        else:
            current_time = self.queen_hive.last_tick
            if current_time >= self.begin_harvest_time + randint(2000, 4000):
                self.harvesting_pollen = False
                self.current_nectar = self.current_nectar + \
                                      flower.transfer_pollen(self.max_nectar_capacity, self.current_nectar)

    def check_available_orders(self):
        """
        :return: If an order is received, the order location. Otherwise, orbit the hive.
        """
        if self.queen_hive.has_orders:
            self.target_flower = self.queen_hive.get_order()
            self.state_machine.trigger('go to flower')
            return Vector2(self.target_flower.rect.left + self.target_flower.rect.width/2,
                           self.target_flower.rect.top + self.target_flower.rect.height/2)
        else:
            return self.orbit_hive()

    def handle_collisions(self, flowers):
        if self.state == 'go to flower':
            if sprite.collide_rect(self, self.target_flower):
                    self.state_machine.trigger('arrived at flower')

    def collide_with_flower(self, flower):
        pass

    def validate_collision(self):
        pass


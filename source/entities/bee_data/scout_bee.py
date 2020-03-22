"""
Class Name: Scout Bee
Class Purpose: Bee subclass which searches for flowers and other points of interest
Notes:
"""

# IMPORTS
from math import sqrt, pi, cos, sin
from random import randint, random

from pygame import Vector2

from source.entities.bee_data.bee import Bee
from source.entities.bee_data.bee_components.castes import scout_fysom
from source.entities.bee_data.bee_components.stomach import Stomach


# CLASS BODY


class ScoutBee(Bee):

    # FUNCTIONS

    def __init__(self, location, queen):

        self.scouting_complete = True  # Vars used in the scouting process
        self.remembered_flower = None

        self.state_machine = scout_fysom()  # Assigns the behavior finite state machine
        self.stomach = Stomach()

        Bee.__init__(self, location, queen)

    def update(self):
        self.target_destination = self.update_target()
        self.head_towards()
        self.update_sprite()

    def update_target(self):
        if self.state == 'report':
            return self.report_back_to_hive()
        elif self.state == 'scout':
            return self.search_for_flowers()
        else:
            return self.report_back_to_hive()

    def remember_flower(self, flower):
        self.remembered_flower = flower

    def forget_flower(self):
        self.remembered_flower = None

    def search_for_flowers(self):
        if self.scouting_complete:
            return self.random_walk_scout()
        else:
            if self.location.distance_to(self.target_destination) < 5:  # [5] could perhaps be a variable (eyesight)
                self.scouting_complete = True  # or maybe its based on flower smelliness?

            return self.target_destination

    def random_walk_scout(self):

        new_x = self.location.x + randint(-50, 50)
        new_y = self.location.y + randint(-40, 40)

        destination = Vector2(new_x, new_y)
        if self.queen_hive.rect.inflate(10, 10).collidepoint(new_x, new_y):
            return self.random_walk_scout()
        else:
            self.use_energy(self.location.distance_to(destination))

            self.scouting_complete = False
            return Vector2(destination)

    def use_energy(self, distance):
        hungry = self.stomach.use_energy_for_turn(distance)
        if hungry:
            self.state_machine.trigger("stomach empty")

    def report_back_to_hive(self):
        if self.location.distance_to(self.queen_hive.center) < self.rect.width / 2:
            self.scouting_complete = True
            if self.remembered_flower is not None:
                self.queen_hive.remember_flower(self.remembered_flower)
                self.forget_flower()
            self.stomach.eat(self.queen_hive)
            self.state_machine.trigger('dance complete')

        return Vector2(self.hive_location.x, self.hive_location.y)

    def collide_with_flower(self, flower):
        if flower not in self.queen_hive.known_flowers:
            self.remember_flower(flower)
            self.state_machine.trigger('found flower')

    def validate_collision(self):
        if self.state == 'scout':
            return True
        else:
            return False

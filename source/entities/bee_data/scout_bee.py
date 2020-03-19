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


# CLASS BODY


class ScoutBee(Bee):

    # FUNCTIONS

    def __init__(self, location, queen):

        self.scouting_complete = True  # Vars used in the scouting process
        self.remembered_flower = None

        self.bee_states = scout_fysom()  # Assigns the behavior finite state machine

        Bee.__init__(self, location, queen)

    def move(self):
        self.target_destination = self.update_target(self.bee_states.current)
        self.head_towards()
        self.update_sprite()

    def remember_flower(self, flower):
        self.remembered_flower = flower

    def forget_flower(self):
        self.remembered_flower = None

    def search_for_flowers(self):

        if self.scouting_complete:
            return self.begin_new_scouting_mission()
        else:
            if self.location.distance_to(self.target_destination) < 5:  # [5] could perhaps be a variable (eyesight)
                self.scouting_complete = True  # or maybe its based on flower smelliness?

            return self.target_destination

    def begin_new_scouting_mission(self):  # TODO: Rework into a random walk approach

        r = randint(0, 400) * sqrt(random())
        theta = random() * 2 * pi
        if randint(0, 1) == 0:
            random_x_coordinate = self.hive_location.x + (r * cos(theta))
        else:
            random_x_coordinate = self.hive_location.x - (r * cos(theta))
        if randint(0, 1) == 1:
            random_y_coordinate = self.hive_location.y + (r * sin(theta))
        else:
            random_y_coordinate = self.hive_location.y - (r * sin(theta))

        self.scouting_complete = False
        return Vector2(random_x_coordinate, random_y_coordinate)

    def report_back_to_hive(self):
        if self.location.distance_to(self.queen_hive.center) < 5:
            self.scouting_complete = True
            self.queen_hive.remember_flower(self.remembered_flower)
            self.forget_flower()

            self.bee_states.trigger('dance complete')

        return Vector2(self.hive_location.x, self.hive_location.y)

"""
Class Name: Scout Bee
Class Purpose: Bee subclass which searches for flowers and other points of interest
Notes:
"""

# IMPORTS
from math import sqrt, pi, cos, sin
from random import randint, random
from pygame.sprite import collide_rect
from source.entities.bee_data.bee import Bee
from source.entities.bee_data.castes import scout_fysom

# CLASS BODY


class ScoutBee(Bee):

    # FUNCTIONS

    def __init__(self, location, queen):
        self.search_radius = 300  # How far the scout will search for new flower patches

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
            if abs(self.target_destination[0] - self.rect.left) < 20:
                self.scouting_complete = True

            return self.target_destination

    def begin_new_scouting_mission(self):

        r = self.search_radius * sqrt(random())
        theta = random() * 2 * pi
        if randint(0, 1) == 0:
            random_x_coordinate = self.queen_hive_x + (r * cos(theta))
        else:
            random_x_coordinate = self.queen_hive_x - (r * cos(theta))
        if randint(0, 1) == 1:
            random_y_coordinate = self.queen_hive_y + (r * sin(theta))
        else:
            random_y_coordinate = self.queen_hive_y - (r * sin(theta))

        self.scouting_complete = False
        return random_x_coordinate, random_y_coordinate

    def report_back_to_hive(self):
        if collide_rect(self, self.queen_hive):
            self.scouting_complete = True
            self.queen_hive.remember_flower(self.remembered_flower)
            self.forget_flower()

            self.bee_states.trigger('dance complete')
            return self.queen_hive_x, self.queen_hive_y
        else:
            return self.queen_hive_x, self.queen_hive_y



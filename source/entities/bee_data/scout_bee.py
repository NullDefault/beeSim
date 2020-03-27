"""
Class Name: Scout Bee
Class Purpose: Bee subclass which searches for flowers and other points of interest
Notes:
"""

# IMPORTS
from random import randint
from pygame import Vector2
from math import floor, atan2, pi

from source.entities.bee_data.bee import Bee
from source.entities.bee_data.bee_components.castes import scout_fysom
from source.entities.bee_data.bee_components.stomach import Stomach


def map_to_range(orientation):
    """
    Maps the angle orientation in degrees to range [-180, 180)
    :param orientation:
    :return: the degree mapped onto the range
    """
    return orientation - 360 * floor((orientation + 180) * (1 / 360))


def vector_to_degrees(vector):
    """
    Returns the angle from X+ axis to the given vector
    :param vector:
    :return: angle from the X+ axis
    """
    return atan2(-vector[1], vector[0]) * (180/pi)


class ScoutBee(Bee):

    # FUNCTIONS

    def __init__(self, location, queen):
        Bee.__init__(self, location, queen)

        self.scouting_complete = True  # Vars used in the scouting process
        self.remembered_flower = None
        self.sight_range = self.rect.height * 2
        self.state_machine = scout_fysom()  # Assigns the behavior finite state machine
        self.stomach = Stomach()

    def update(self):
        """
        This function runs once every frame
        :return: void
        """
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
        """
        Saves the flower in the scouts memory
        :param flower:
        :return:
        """
        self.remembered_flower = flower

    def forget_flower(self):
        """
        Forgets the currently remembered flower
        :return:
        """
        self.remembered_flower = None

    def search_for_flowers(self):
        """
        Makes the scout scout (ha ha)
        :return: If no mission is currently happening, returns a new random walk destination. Otherwise keeps going to
        to whatever the current scouting destination is.
        """
        if self.scouting_complete:
            return self.random_walk_scout()
        else:
            if self.location.distance_to(self.target_destination) < 5:  # [5] could perhaps be a variable (eyesight)
                self.scouting_complete = True  # or maybe its based on flower smelliness?

            return self.target_destination

    def random_walk_scout(self):
        """
        :return: Next destination using random walk rules
        """

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
        """
        Uses the energy needed for movement
        :param distance:
        :return: void
        """
        hungry = self.stomach.use_energy_for_turn(distance)
        if hungry:
            self.state_machine.trigger("stomach empty")

    def report_back_to_hive(self):
        """
        Goes towards the hive
        :return: The destination of the queen hive
        """
        if self.location.distance_to(self.queen_hive.center) < self.rect.width / 2:
            self.scouting_complete = True
            if self.remembered_flower is not None:
                self.queen_hive.remember_flower(self.remembered_flower)
                self.forget_flower()
            self.stomach.eat(self.queen_hive)
            self.state_machine.trigger('dance complete')

        return Vector2(self.hive_location.x, self.hive_location.y)

    def handle_collisions(self, flowers):
        if self.state == 'scout':
            for f in flowers:
                distance_vector = f.center_loc - self.location
                dist = distance_vector.length()

                if dist < self.sight_range:  # 16 should be how far the bee can see
                    dist_orientation = vector_to_degrees(distance_vector)

                    bee_angle = 270 - atan2(self.target_destination.y - self.location.y,
                                            self.target_destination.x - self.location.x) * 180 / pi

                    angular_distance = dist_orientation - bee_angle
                    angular_distance = map_to_range(angular_distance)

                    if abs(angular_distance) < 150:
                        self.collide_with_flower(f)
                        break

    def collide_with_flower(self, flower):
        if flower not in self.queen_hive.known_flowers:
            self.remember_flower(flower)
            self.state_machine.trigger('found flower')

    def validate_collision(self):
        if self.state == 'scout':
            return True
        else:
            return False

"""
Class Name: Flower
Class Purpose: Holds data common to all flowers
Notes:
"""

#  IMPORTS
from source.entities.entity import Entity
from pygame import Vector2


# CLASS BODY


class Flower(Entity):

    # FUNCTIONS

    def __init__(self, location):
        self.busy = False  # Used by hives to designate orders
        self.pollen = 10  # How much pollen the flowers starts with
        self.neighbors = None  # Used for growth

        Entity.__init__(self, location, 'flower')

    @property
    def center_loc(self):
        return Vector2(self.rect.left + self.rect.width / 2, self.rect.top + self.rect.height / 2)

    def set_neighbors(self, neighbors_list):
        self.neighbors = neighbors_list

    def finish_harvest(self, limit, current):
        wanted = limit - current
        if wanted <= self.pollen:
            pollen_taken = wanted
            self.pollen = self.pollen - pollen_taken
        else:
            pollen_taken = self.pollen
            self.pollen = 0

        return pollen_taken

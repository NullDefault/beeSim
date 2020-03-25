"""
Class Name: Flower
Class Purpose: Holds data common to all flowers
Notes:
"""

#  IMPORTS
from source.entities.entity import Entity
from pygame import Vector2
from statistics import NormalDist


# CLASS BODY

random_gen = NormalDist(0.5, 0.15)

class Flower(Entity):

    # FUNCTIONS

    def __init__(self, location):
        self.busy = False  # Used by hives to designate orders
        self.pollen = 10  # How much pollen the flowers starts with
        self.neighbors = None  # Used for growth

        random_color = self.choose_color()

        Entity.__init__(self, location, 'flower'+"_"+str(random_color))

    @property
    def center_loc(self):
        return Vector2(self.rect.left + self.rect.width / 2, self.rect.top + self.rect.height / 2)

    def choose_color(self):
        roll = random_gen.samples(1)[0]
        if 0.4 <= roll <= 0.6:
            return 0
        elif 0.3 < roll < 0.4:
            return 1
        elif 0.6 < roll < 0.7:
            return 3
        elif roll < 0.1 or roll > 0.9:
            return 2
        else:
            return 4

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

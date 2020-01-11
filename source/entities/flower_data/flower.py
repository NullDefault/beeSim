"""
Class Name: Flower
Class Purpose: Holds data common to all flowers
Notes:
"""

#  IMPORTS
from source.entities.entity import Entity
from random import randint

# CLASS BODY


class Flower(Entity):

    # FUNCTIONS

    def __init__(self, location, growth_stage=None):

        if growth_stage is None:
            # if not explicitly specified, the flower will spawn with in a random stage of its growth
            growth_stage = randint(0, 5)
        else:
            growth_stage = growth_stage
        self.occupied = False  # For bee business
        self.pollen = 100  # How much pollen the flowers starts with
        self.neighbors = None  # Used for growth

        Entity.__init__(self, location, 'flower_'+str(growth_stage))

    def set_neighbors(self, neighbors_list):
        self.neighbors = neighbors_list

    def begin_harvest(self):
        self.occupied = True

    def finish_harvest(self):
        self.occupied = False
        pollen_taken = 1  # TODO: Replace this with a formula of some kind
        self.pollen = self.pollen - pollen_taken

        return pollen_taken

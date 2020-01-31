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

    def __init__(self, location):

        temp_growth_tick = randint(0, 50)

        self.busy = False  # Used by hives to designate orders
        self.pollen = 10  # How much pollen the flowers starts with
        self.neighbors = None  # Used for growth
        self.growth_phase = (temp_growth_tick // 10)
        self.growth_tick = temp_growth_tick + randint(0, 50)  # having 2 rolls helps us pull the avg value to the middle
        Entity.__init__(self, location, 'flower_'+str(self.growth_phase))

    def set_neighbors(self, neighbors_list):
        self.neighbors = neighbors_list

    def finish_harvest(self):
        pollen_taken = 1
        self.pollen = self.pollen - pollen_taken

        return pollen_taken

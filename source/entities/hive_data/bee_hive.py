"""
Class Name: Bee Hive
Class Purpose: Holds data and functions relevant for bee hives
Notes:
"""

from random import randint

#  IMPORTS
from pygame import Vector2, Surface, SRCALPHA, surfarray

from source.entities.entity import Entity
from source.entities.honey_bar import HoneyBar
from source.entities.sprite_bank import sprite_bank

# CLASS BODY

team_color_dict = {
    'red': [204, 0, 0],
    'green': [0, 255, 10],
    'blue': [0, 153, 255],
    'purple': [153, 0, 153],
    'yellow': [255, 255, 0]
}


class BeeHive(Entity):

    #  FUNCTIONS

    def __init__(self, location, team):

        self.highlighted = False  # Used in inspection mode

        self.current_nectar = 50  # How much nectar the hive has stored
        self.max_nectar = 100  # Maximum honey the hive can store

        self.bee_buy_cost = 50

        self.last_tick = 0  # Time since last tick check

        self.known_flowers = []  # Flowers the scouts have discovered
        self.flowers_getting_harvested = []  # Flowers currently being harvested by workers

        self.workers = []  # Hive workers
        self.scouts = []  # Hive scouts

        Entity.__init__(self, location, 'hive')
        self.scaled_rect = self.rect

        self.honey_bar = HoneyBar(self)

        self.team = team
        self.phenotype = (randint(0, 11), randint(0, 5), randint(0, 5), randint(0, 5))
        self.init_team_data()

        self.center = Vector2(self.rect.left + 34, self.rect.top + 54)  # Location of hive entrance

    @property
    def has_orders(self):
        """
        :return: If there's an available order, return True. Otherwise False.
        """
        for flower in self.known_flowers:
            if not flower.busy:
                return True
        return False

    @property
    def flowers(self):
        return self.known_flowers + self.flowers_getting_harvested

    @property
    def number_of_bees(self):
        """
        :return: How many bees are assigned to this hive
        """
        # 0: workers, 1: scouts
        return len(self.workers), len(self.scouts)

    def init_team_data(self):
        """
        Puts the appropriate hat on top of the hive. (It makes its color match its team)
        :return: void
        """
        temp = self.image
        self.image = Surface(self.rect.size, SRCALPHA)
        self.image.blit(sprite_bank[self.team + '_hat'], (20, 5))
        self.image.blit(temp, (0, 0))

    def recolor_crosshair(self, entity):
        """
        Changes the color of the entity crosshair to that of the hive
        :param entity:
        :return: void
        """
        new_crosshair = entity.crosshair.image.copy()
        arr = surfarray.pixels3d(new_crosshair)
        color = team_color_dict[self.team]

        arr[:, :, 0] = color[0]
        arr[:, :, 1] = color[1]
        arr[:, :, 2] = color[2]
        entity.crosshair.image = new_crosshair

        entity.highlighted = self.highlighted

    def add_bee(self, bee, caste):
        self.recolor_crosshair(bee)
        self.workers.append(bee) if caste == 'worker' else self.scouts.append(bee)

    def buy_bee(self):
        self.current_nectar -= self.bee_buy_cost

    def gain_nectar(self, nectar_amount):
        """
        :param nectar_amount:
        :return: Adds n nectar to the hive, unless its overfilled already.
        """
        if self.current_nectar < self.max_nectar:
            self.current_nectar = self.current_nectar + nectar_amount
        else:
            self.current_nectar = self.max_nectar

    def give_food(self, hunger):
        """
        :param hunger:
        :return: Feeds the bee that amount of food
        """
        if self.current_nectar < hunger:
            temp = self.current_nectar
            self.current_nectar = 0
            return temp
        else:
            self.current_nectar = self.current_nectar - hunger
            return hunger

    def remember_flower(self, flower):
        """
        :param flower:
        :return: Adds the flower to the list of known flowers
        """
        if self.highlighted:
            flower.highlighted = True
            flower.get_inspected(self)
        self.known_flowers.append(flower)

    def get_order(self):
        """
        :return: Returns a flower for harvesting process
        """
        flower = self.known_flowers.pop()
        self.flowers_getting_harvested.append(flower)
        flower.busy = True
        return flower

    def highlight(self):
        """
        Turns bee highlighting on or off depending on what state it was in earlier
        :return: void
        """
        if not self.highlighted:
            self.highlighted = True

            for bee in self.workers:
                bee.highlighted = True
            for bee in self.scouts:
                bee.highlighted = True
            for flower in self.flowers:
                self.recolor_crosshair(flower)
                flower.get_inspected(self)
        else:
            self.highlighted = False

            for bee in self.workers:
                bee.highlighted = False
            for bee in self.scouts:
                bee.highlighted = False
            for flower in self.flowers:
                flower.stop_inspection(self)

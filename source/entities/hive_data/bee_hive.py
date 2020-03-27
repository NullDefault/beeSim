"""
Class Name: Bee Hive
Class Purpose: Holds data and functions relevant for bee hives
Notes:
"""

#  IMPORTS
from pygame import Vector2

from source.UI.bee_counters import Counter
from source.UI.honey_bar import HoneyBar
from source.entities.entity import Entity


# CLASS BODY


class BeeHive(Entity):

    #  FUNCTIONS

    def __init__(self, location):

        self.highlighted = False  # Used in inspection mode

        self.current_nectar = 10  # How much nectar the hive has stored
        self.max_nectar = 100  # Maximum honey the hive can store

        self.last_tick = 0  # Time since last tick check

        self.known_flowers = []  # Flowers the scouts have discovered

        self.available_orders = []  # Flowers the workers can be ordered to pursue

        self.workers = []  # Hive workers

        self.scouts = []  # Hive scouts

        Entity.__init__(self, location, 'hive')

        self.worker_counter = Counter(self, "worker_counter")
        self.scout_counter = Counter(self, "scout_counter")
        self.honey_bar = HoneyBar(self)
        self.center = Vector2(self.rect.left + 34, self.rect.top + 54)  # Location of hive entrance

    @property
    def has_orders(self):
        """
        :return: If there's an available order, return True. Otherwise False.
        """
        self.update_order_queue()
        if len(self.available_orders) != 0:
            return True
        else:
            return False

    @property
    def number_of_bees(self):
        """
        :return: How many bees are assigned to this hive
        """
        # 0: workers, 1: scouts
        return len(self.workers), len(self.scouts)

    def add_worker_bee(self, bee):
        """
        :param bee:
        :return: Adds the worker bee to the hive
        """
        self.workers.append(bee)

    def add_scout_bee(self, bee):
        """
        :param bee:
        :return: Adds the scout bee to the hive
        """
        self.scouts.append(bee)

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
        self.known_flowers.append(flower)
        self.available_orders.append(flower)

    def forget_flower(self, flower):
        """
        :param flower:
        :return: Removes the flower from the list of known flowers
        """
        self.known_flowers.remove(flower)
        self.available_orders.remove(flower)

    def update_order_queue(self):
        """
        Updates the order queue
        :return: void
        """
        available_orders = []
        for flower in self.known_flowers:
            if flower.pollen != 0 and not flower.busy:
                available_orders.append(flower)

        self.available_orders = available_orders

    def get_order(self):
        """
        :return: Returns a flower for harvesting process
        """
        flower = self.available_orders.pop()
        flower.busy = True
        return flower

    def highlight_bees(self):
        """
        Turns bee highlighting on or off depending on what state it was in earlier
        :return: void
        """
        if not self.highlighted:
            for bee in self.workers:
                bee.highlighted = True
                self.highlighted = True
            for bee in self.scouts:
                bee.highlighted = True
                self.highlighted = True
        else:
            for bee in self.workers:
                bee.highlighted = False
                self.highlighted = False
            for bee in self.scouts:
                bee.highlighted = False
                self.highlighted = False

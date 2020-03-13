"""
Class Name: Bee Hive
Class Purpose: Holds data and functions relevant for bee hives
Notes:
"""

#  IMPORTS
from source.entities.entity import Entity
from source.UI.honey_bar import HoneyBar
from source.UI.bee_counters import WorkerCounter, ScoutCounter
# CLASS BODY
from source.logic_and_algorithms.vector import Vector


class BeeHive(Entity):

    #  FUNCTIONS

    def __init__(self, location):

        self.highlighted = False  # Used in inspection mode

        self.current_honey = 10  # How much nectar the hive has stored
        self.max_honey = 100    # Maximum honey the hive can store

        self.last_tick = 0  # Time since last tick check

        self.known_flowers = []  # Flowers the scouts have discovered

        self.available_orders = []  # Flowers the workers can be ordered to pursue

        self.workers = []  # Hive workers

        self.scouts = []  # Hive scouts

        Entity.__init__(self, location, 'hive')

        self.worker_counter = WorkerCounter(self)
        self.scout_counter = ScoutCounter(self)
        self.honey_bar = HoneyBar(self)
        self.center = Vector(self.rect.left + 38, self.rect.top + 56)  # Location of hive entrance

    def add_worker_bee(self, bee):
        self.workers.append(bee)

    def add_scout_bee(self, bee):
        self.scouts.append(bee)

    def get_bees(self):
        # 0: workers, 1: scouts
        return len(self.workers), len(self.scouts)

    def get_nectar(self):
        return self.current_honey

    def gain_nectar(self, nectar_amount):
        if self.current_honey < self.max_honey:
            self.current_honey = self.current_honey + nectar_amount
        else:
            self.current_honey = self.max_honey

    def remember_flower(self, flower):
        self.known_flowers.append(flower)
        self.available_orders.append(flower)

    def update_order_queue(self):
        available_orders = []
        for flower in self.known_flowers:
            if flower.pollen != 0 and not flower.busy:
                available_orders.append(flower)

        self.available_orders = available_orders

    def has_orders(self):
        self.update_order_queue()
        if len(self.available_orders) is not 0:
            return True
        else:
            return False

    def get_order(self):
        flower = self.available_orders.pop()
        flower.busy = True
        return flower

    def highlight_bees(self):
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



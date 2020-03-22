"""
Class Name: Stomach
Class Purpose: Component that takes care of bee's nutritional needs. Encapsulates all info necessary for bees to eat and
starve when appropriate. It's their stomach but like programmed.
Notes:
"""


class Stomach:
    def __init__(self):
        self.max_capacity = 10
        self.current_food = 10
        self.energy_expenditure = 0.01

    def use_energy_for_turn(self, distance):
        self.current_food = self.current_food - (self.energy_expenditure * distance)
        if self.current_food <= 0:
            self.current_food = 0
            return True

    def eat(self, hive):
        needed_food = self.max_capacity - self.current_food
        gained_food = hive.give_food(needed_food)
        self.current_food = gained_food

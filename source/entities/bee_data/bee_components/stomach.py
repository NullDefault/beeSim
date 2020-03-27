"""
Class Name: Stomach
Class Purpose: Component that takes care of bee's nutritional needs. Encapsulates all info necessary for bees to eat and
starve when appropriate. It's their stomach but like programmed.
Notes:
"""


class Stomach:
    def __init__(self):
        self.max_capacity = 5  # How Much Food the Stomach Can Fit
        self.current_food = 5  # How Much Food It Currently Has
        self.energy_expenditure = 0.005  # Used in energy calculations

    def use_energy_for_turn(self, distance):
        """
        This function calculates how much food the bee uses after traversing some distance
        :param distance: The length of the vector to the next destination
        :return: Returns True if the bee is out of food (Scouts return to their hive when hungry for example)
        """
        self.current_food = self.current_food - (self.energy_expenditure * distance)
        if self.current_food <= 0:
            self.current_food = 0
            return True

    def eat(self, hive):
        """
        Takes food from the given hive and puts it into the Bee's stomach
        :param hive: The hive the food is being taken from. Almost always will be the Queen Hive.
        :return: Void
        """

        needed_food = self.max_capacity - self.current_food
        gained_food = hive.give_food(needed_food)
        self.current_food = gained_food

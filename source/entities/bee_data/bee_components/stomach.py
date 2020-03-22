"""
Class Name: Stomach
Class Purpose: Component that takes care of bee's nutritional needs. Encapsulates all info necessary for bees to eat and
starve when appropriate. It's their stomach but like programmed.
Notes:
"""


class Stomach:
    def __init__(self):
        self.max_capacity = 10
        self.current_food = 1
        self.energy_expenditure = 0.01

    def use_energy_for_turn(self):
        self.current_food = self.current_food - self.energy_expenditure

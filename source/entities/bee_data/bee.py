"""
Class Name: Bee
Class Purpose: Super class for all Bee Entities, holds data and functions all bees share.
Notes: Castes.py is a dictionary of finite state machines for each individual bee subclass (i.e workers and scouts)
"""

# IMPORTS
from random import randint
from source.entities.entity import Entity
from source.entities import sprite_bank

# CLASS BODY


class Bee(Entity):
########################################################################################################################
    # DATA FIELDS
    wiggle = 1  # How much a bee 'wiggles' during movement, purely for aesthetic reasons
    speed = 4  # How many pixels a bee will traverse in a single turn
########################################################################################################################
    # FUNCTIONS

    def __init__(self, location, queen):

        self.queen_hive = queen  # This sets which hive the bee be(e)longs to
        self.queen_hive_x = queen.center[0]
        self.queen_hive_y = queen.center[1]
        self.highlighted = False  # Used for highlighting the bees during inspection mode
        self.target_destination = (self.queen_hive_x, self.queen_hive_y)  # Variable used for movement

        Entity.__init__(self, location, 'bee')  # Calls the Entity constructor

    def update_target(self, current_state):  # Note: The methods this function calls only exist in the bee subclasses
        # Worker Methods
        if current_state == 'await orders':
            return self.check_available_orders()
        elif current_state == 'harvest':
            return self.harvest_flower()
        elif current_state == 'offload':
            return self.offload()

        # Scout Methods
        elif current_state == 'report':
            return self.report_back_to_hive()
        elif current_state == 'scout':
            return self.search_for_flowers()
        elif current_state == 'head back':
            return self.deliver_nectar_load()

    def head_towards(self):  # Heads towards the current target destination for self.speed pixels distance

        x_distance = self.target_destination[0] - (self.rect.left + 5)
        y_distance = self.target_destination[1] - (self.rect.top + 4)

        dx = 0
        dy = 0

        movement_points_to_spend = self.speed

        while True:  # This loop basically picks randomly how much you move on the x and y axis towards the destination
            if movement_points_to_spend == 0:
                break
            coin_flip = randint(0, 1)
            if coin_flip == 0:
                dx = dx + 1
            else:
                dy = dy + 1

            movement_points_to_spend = movement_points_to_spend - 1

        if x_distance < 0:
            dx = -dx
        if y_distance < 0:
            dy = -dy

        if -4 < x_distance < 4:
            dx = 0
        if -4 < y_distance < 4:
            dy = 0

        #  This wiggles the bee
        random_x_offset = randint(-self.wiggle, self.wiggle)
        random_y_offset = randint(-self.wiggle, self.wiggle)

        self.rect.top = self.rect.top + dy + random_x_offset
        self.rect.left = self.rect.left + dx + random_y_offset

    def update_sprite(self):  # Updates the new sprite, calculating the orientation based on change in coordinates

        x_distance = self.target_destination[0] - self.rect.left
        y_distance = self.target_destination[1] - self.rect.top

        if abs(x_distance) > abs(y_distance):
            if x_distance < 0:
                if self.highlighted:
                    self.image = sprite_bank.retrieve("bee_left_selected_sprite")
                else:
                    self.image = sprite_bank.retrieve("bee_left_sprite")
            else:
                if self.highlighted:
                    self.image = sprite_bank.retrieve("bee_right_selected_sprite")
                else:
                    self.image = sprite_bank.retrieve("bee_right_sprite")
        else:
            if y_distance < 0:
                if self.highlighted:
                    self.image = sprite_bank.retrieve("bee_up_selected_sprite")
                else:
                    self.image = sprite_bank.retrieve("bee_up_sprite")
            else:
                if self.highlighted:
                    self.image = sprite_bank.retrieve("bee_down_selected_sprite")
                else:
                    self.image = sprite_bank.retrieve("bee_down_sprite")

    def validate_collision(self):  # Logic function for detecting collisions for bees of interest
        # Note: bee_states is assigned only in subclasses
        if self.bee_states.current == 'scout' or self.bee_states.current == 'go to flower':
            return True
        else:
            return False

    def collide_with_flower(self, flower):  # Another collision function
        # Scout logic
        if self.bee_states.current == 'scout':
            self.remember_flower(flower)
            self.bee_states.trigger('found flower')
        # Worker logic
        if self.bee_states.current == 'go to flower':
            self.bee_states.trigger('arrived at flower')

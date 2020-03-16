"""
Class Name: Bee
Class Purpose: Super class for all Bee Entities, holds data and functions all bees share.
Notes: Castes.py is a dictionary of finite state machines for each individual bee subclass (i.e workers and scouts)
"""

# IMPORTS
import math

from pygame import transform, Vector2
from random import randint
from source.entities import sprite_bank
from source.entities.bee_data.bee_components.stomach import Stomach
from source.entities.crosshair import Crosshair
from source.entities.entity import Entity
# CLASS BODY

animation_fps = 20


class Bee(Entity):
########################################################################################################################
    # FUNCTIONS

    def __init__(self, location, queen):

        self.queen_hive = queen  # This sets which hive the bee be(e)longs to
        self.highlighted = False  # Used for highlighting the bees during inspection mode
        self.target_destination = Vector2(queen.center.x, queen.center.y)  # Variable used for movement
        self.speed = 1.5
        self.wings_up = False
        self.animation_loop = randint(0, animation_fps)
        self.wings_up_sprite = sprite_bank.retrieve('bee_wings_up')
        self.wings_down_sprite = sprite_bank.retrieve('bee_wings_down')
        self.stomach = Stomach()

        Entity.__init__(self, location, 'bee_wings_down')  # Calls the Entity constructor
        self.crosshair = Crosshair(self)

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

    @property
    def location(self):
        return Vector2(self.rect.left + self.rect.width/2,
                       self.rect.top + self.rect.height/2)

    @property
    def hive_location(self):
        return self.queen_hive.center

    def head_towards(self):
        dest = self.target_destination - self.location
        if dest.length() != 0:
            dest.scale_to_length(self.speed)
        dest.normalize()
        self.rect.left = self.rect.left + dest.x
        self.rect.top = self.rect.top + dest.y

    def update_sprite(self):
        rotate = False
        if self.bee_states.current == 'offload':
            self.image = sprite_bank.retrieve("bee_hidden_sprite")
        elif self.bee_states.current == 'harvest' and self.harvesting_pollen:
            self.image = sprite_bank.retrieve("bee_harvest_sprite")
        else:

            if self.wings_up:
                self.image = self.wings_down_sprite
                self.wings_up = False
            else:
                self.image = self.wings_up_sprite
                self.wings_up = True

            if self.animation_loop == animation_fps:
                self.animation_loop = 0
            else:
                self.animation_loop = self.animation_loop + 1
            rotate = True

        if rotate:
            angle = 270 - math.atan2(self.target_destination.y - self.location.y,
                                     self.target_destination.x - self.location.x) * 180 / math.pi
            self.image = transform.rotate(self.image, angle)

        self.rect.width = self.image.get_rect().width
        self.rect.height = self.image.get_rect().height

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

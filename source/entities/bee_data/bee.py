"""
Class Name: Bee
Class Purpose: Super class for all Bee Entities, holds data and functions all bees share.
Notes: Castes.py is a dictionary of finite state machines for each individual bee subclass (i.e workers and scouts)
"""

# IMPORTS
import math
from abc import abstractmethod
from random import randint

from pygame import transform, Vector2

from source.entities import sprite_bank
from source.entities.bee_data.bee_components.bee_factory import make_bee_sprites
from source.entities.crosshair import Crosshair
from source.entities.entity import Entity

# CLASS BODY

animation_fps = 20  # How many frames will pass before the bee flaps its wings


class Bee(Entity):

    # FUNCTIONS

    def __init__(self, location, queen):

        self.queen_hive = queen  # This sets which hive the bee be(e)longs to

        # All Of These Variables Are Used in Rendering
        self.animation_loop = randint(0, animation_fps)  # These vars are used to make the bee flap its
        sprites = make_bee_sprites(self.queen_hive.phenotype)
        self.wings_up_sprite = sprites[0]
        self.wings_down_sprite = sprites[1]

        Entity.__init__(self, location, self.wings_up_sprite)  # Calls the Entity constructor

        self.wings_up = False

        self.highlighted = False  # Used for highlighting the bees during inspection mode

        self.target_destination = queen.center  # Variable used for movement
        self.speed = 1.5  # The max length a bee can move in a single frame

        self.crosshair = Crosshair(self, 'bee')

        self.location = Vector2(self.rect.left + self.rect.width / 2,
                                self.rect.top + self.rect.height / 2)

    @property
    def hive_location(self):
        """
        :return: The location of the hive (also the center, not the top left corner)
        """
        return self.queen_hive.center

    @abstractmethod
    def update_target(self):
        """
        Updates where the bee is going next according to the game rules
        :return: void
        """
        pass

    @abstractmethod
    def collide_with_flower(self, flower):
        """
        Registers a collision with a flower
        :param flower:
        :return: void
        """
        pass

    @abstractmethod
    def validate_collision(self):
        """
        Checks if this bee has to collide with a flower or not
        :return: True if a collision is to happen, False otherwise
        """
        pass

    def head_towards(self):
        """
        Moves the bee towards its destination
        :return: void
        """
        dest = self.target_destination - self.location
        if dest.length() != 0:
            dest.scale_to_length(self.speed)
            dest.normalize()
        self.rect.left += dest.x
        self.rect.top += dest.y

    def update_sprite(self):
        """
        Updates the sprite to face towards where the bee is going and flaps the wings if necessary
        :return: void
        """
        rotate = False
        state = self.state_machine.current
        if state == 'offload':
            self.image = sprite_bank.retrieve("bee_hidden_sprite")
        elif state == 'harvest' and self.harvesting_pollen:
            self.wings_up = False
            self.image = self.wings_down_sprite
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

        self.location = Vector2(self.rect.left + self.rect.width / 2,
                                self.rect.top + self.rect.height / 2)

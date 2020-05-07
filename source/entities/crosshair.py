"""
Class Name: Crosshair
Class Purpose: SUsed to highlight bees in inspection mode.
Notes:
"""

from source.entities.entity import Entity


class Crosshair(Entity):
    def __init__(self, entity, kind):
        self.owner = entity
        Entity.__init__(self, (entity.rect.left, entity.rect.top), 'crosshair_' + kind)  # Calls the Entity constructor

    def follow(self):
        """
        Follows the owner
        :return: void
        """
        self.rect.left = self.owner.location.x - 10
        self.rect.top = self.owner.location.y - 10

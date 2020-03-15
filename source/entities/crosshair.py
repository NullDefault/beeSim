"""
Class Name: Crosshair
Class Purpose: SUsed to highlight bees in inspection mode.
Notes:
"""

from source.entities.entity import Entity


class Crosshair(Entity):
    def __init__(self, bee):
        self.owner = bee
        Entity.__init__(self, (bee.location.x, bee.location.y), 'crosshair')  # Calls the Entity constructor

    def follow(self):
        self.rect.left = self.owner.location.x - 10
        self.rect.top = self.owner.location.y - 10

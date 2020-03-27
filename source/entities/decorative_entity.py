"""
Class Name: Decorative Plant
Class Purpose: Class for creating plants that have no special functionality
Notes:
"""

from source.entities.entity import Entity


class Decoration(Entity):

    # FUNCTIONS

    def __init__(self, location, kind):
        Entity.__init__(self, location, kind)

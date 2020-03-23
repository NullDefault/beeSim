"""
Class Name: Grass Patch
Class Purpose: It's Grass Patch
Notes:
"""
#  IMPORTS
from source.entities.entity import Entity


# CLASS BODY


class GrassPatch(Entity):

    # FUNCTIONS

    def __init__(self, location):
        Entity.__init__(self, location, 'grass_patch')

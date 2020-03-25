"""
Class Name: Decorative Plant
Class Purpose: Class for creating plants that have no special functionality
Notes:
"""
#  IMPORTS
from source.entities.entity import Entity

# CLASS BODY


class Decoration(Entity):

    # FUNCTIONS

    def __init__(self, location, kind):
        Entity.__init__(self, location, kind)

"""
Class Name: Background
Class Purpose: Renderable entity corresponding to the background (grass field)
Notes:
"""

from source.entities.entity import Entity


class Background(Entity):
    def __init__(self):
        Entity.__init__(self, (0, 0), 'grass_background')

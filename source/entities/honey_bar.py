"""
Class Name: Honey Bar
Class Purpose: UI elements used to display how much honey is in a particular hive
Notes:
"""
from pygame import draw, Surface, SRCALPHA

from source.entities.entity import Entity


class HoneyBar(Entity):
    def __init__(self, owner):
        self.owner = owner
        loc = self.owner.rect.left - 33, self.owner.rect.top + 70
        Entity.__init__(self, loc, 'honey_bar')
        self.base_sprite = self.image

    def update(self):
        """
        Renders the honey bar
        :return: void
        """

        percent_full = self.owner.current_nectar / self.owner.max_nectar

        if percent_full == 0:
            return 0

        bar_start = 14, 8

        bar_end = bar_start[0] + 109, bar_start[1]
        honey_end = bar_start[0] + int(109*percent_full), bar_start[1]
        surf = Surface((self.rect.width, self.rect.height), SRCALPHA)

        draw.line(surf, (255, 255, 255), bar_start, bar_end, 13)
        draw.line(surf, (230, 200, 0), bar_start, honey_end, 13)

        surf.blit(self.base_sprite, (0, 0))
        self.image = surf


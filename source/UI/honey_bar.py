"""
Class Name: Honey Bar
Class Purpose: UI elements used to display how much honey is in a particular hive
Notes:
"""

from pygame import draw

from source.entities.entity import Entity


class HoneyBar(Entity):
    def __init__(self, owner):
        self.owner = owner
        loc = self.owner.rect.left - 8, self.owner.rect.top - 18
        Entity.__init__(self, loc, 'honey_bar')

    def draw_honey(self):
        """
        Renders the honey bar
        :return: void
        """

        percent_full = self.owner.current_nectar / self.owner.max_nectar

        if percent_full == 0:
            return 0

        bar_start = 2, 65

        bar_end = bar_start[0], bar_start[1] - 60 * percent_full

        draw.line(self.image, (230, 200, 0), bar_start, bar_end, 4)
        draw.line(self.image, (255, 255, 255), (2, 4), bar_end, 4)

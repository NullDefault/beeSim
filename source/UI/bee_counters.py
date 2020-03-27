"""
Class Name: Bee Counters
Class Purpose: UI elements that display how many workers and scouts are in a hive
Notes:
"""

from pygame import Rect, font

from source.entities.entity import Entity

font.init()
gameFont = font.Font("source/assets/fonts/m5x7.ttf", 30)


class Counter(Entity):
    def __init__(self, owner, kind):
        self.owner = owner
        if kind == 'scout_counter':
            loc = self.owner.rect.left + 66, self.owner.rect.top - 16
            Entity.__init__(self, loc, 'scout_counter')
        elif kind == 'worker_counter':
            loc = self.owner.rect.left + 66, self.owner.rect.top + 22
            Entity.__init__(self, loc, 'worker_counter')
        self.kind = kind

    def render(self):
        if self.kind == 'scout_counter':
            self.image.fill((255, 255, 255), rect=Rect(self.rect.left + 3, self.rect.top + 3, 26, 26))
            text = gameFont.render(str(len(self.owner.scouts)), False, [0, 0, 0], None)
            self.image.blit(text, (4, 4))
        elif self.kind == 'worker_counter':
            self.image.fill((255, 255, 255), rect=Rect(self.rect.left + 3, self.rect.top + 3, 26, 26))
            text = gameFont.render(str(len(self.owner.workers)), False, [0, 0, 0], None)
            self.image.blit(text, (4, 4))

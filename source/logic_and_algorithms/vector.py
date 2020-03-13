"""
Class Name: Vector
Class Purpose: Represents a 2D vector with an x and y values
Notes:
"""

from math import sqrt

# CLASS BODY


class Vector:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y

    def add(self, v2):
        self.x = self.x + v2.x
        self.y = self.y + v2.y

    def sub(self, v2):
        self.x = self.x - v2.x
        self.y = self.y - v2.y

    def mult(self, n):
        self.x = self.x * n
        self.y = self.y * n

    def div(self, n):
        if n != 0:
            self.x = self.x / n
            self.y = self.y / n

    def norm(self):
        m = self.mag
        if m is not 0:
            self.div(m)

    @property
    def mag(self):  # magnitude
        return sqrt(self.x*self.x + self.y * self.y)

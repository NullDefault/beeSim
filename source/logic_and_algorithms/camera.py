"""
Class Name: Camera
Class Purpose: Holds data relevant to camera functions during the rendering process
Notes:
"""


class Camera:
    def __init__(self):
        self.location = [0, 0]  # Controls which part of the screen is being rendered
        self.size = (1600, 900)

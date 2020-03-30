from pygame import Surface, Vector2


def make_limits(map_size, frame_resolution):
    """
    :param map_size:
    :param frame_resolution:
    :return: The highest value the camera will be allowed to go
    """
    highest_x_val = map_size[0] - frame_resolution[0]
    highest_y_val = map_size[1] - frame_resolution[1]
    return highest_x_val, highest_y_val


class Camera:

    def __init__(self, frame_resolution, map_size):
        self.frame_resolution = frame_resolution
        self.render_surface = Surface(frame_resolution)
        self.limits = make_limits(map_size, frame_resolution)
        self.location = Vector2(0, 0)

    def render(self, entities):
        """
        :param entities:
        :return: returns the rendered frame
        """
        self.render_surface.fill((102, 200, 102))
        for entity in entities:
            if self.in_range(entity.rect.left, 'x') and self.in_range(entity.rect.top, 'y'):  # This makes sure we only
                self.render_surface.blit(entity.image,                                        # render entities that are
                                         (entity.rect.left - self.location[0],                # within the frame
                                          entity.rect.top - self.location[1]))
        return self.render_surface

    def move(self, destination):
        """
        Moves the camera
        :param destination:
        :return: void
        """
        self.location = self.location + destination

        if self.location.x < 0:
            self.location.x = 0
        if self.location.x > self.limits[0]:
            self.location.x = self.limits[0]
        if self.location.y < 0:
            self.location.y = 0
        if self.location.y > self.limits[1]:
            self.location.y = self.limits[1]

    def in_range(self, val, x_or_y):
        """
        Checks if the given value is inside of the frame or outside
        :param val: the given location
        :param x_or_y: if it is on the x or y axis
        :return: True if inside of the frame, False otherwise
        """
        if x_or_y is 'x':
            if self.location.x <= val <= self.location.x + self.frame_resolution[0]:
                return True
            else:
                return False
        elif x_or_y is 'y':
            if self.location.y <= val <= self.location.y + self.frame_resolution[1]:
                return True
            else:
                return False


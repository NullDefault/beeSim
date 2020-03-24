from pygame import Surface, Vector2


def make_limits(map_size, frame_resolution):
    highest_x_val = map_size[0] - frame_resolution[0]
    highest_y_val = map_size[1] - frame_resolution[1]
    return highest_x_val, highest_y_val


class Camera:
    def __init__(self, frame_resolution, map_size):
        self.render_surface = Surface(frame_resolution)
        self.limits = make_limits(map_size, frame_resolution)
        self.location = Vector2(map_size[0]/2, map_size[1]/2)

    def render(self, entities):
        self.render_surface.fill((102, 200, 102))
        for entity in entities:
            self.render_surface.blit(entity.image,
                                     (entity.rect.left - self.location[0],
                                      entity.rect.top - self.location[1]))
        return self.render_surface

    def move(self, destination):
        self.location = self.location + destination

        if self.location.x < 0:
            self.location.x = 0
        if self.location.x > self.limits[0]:
            self.location.x = self.limits[0]
        if self.location.y < 0:
            self.location.y = 0
        if self.location.y > self.limits[1]:
            self.location.y = self.limits[1]




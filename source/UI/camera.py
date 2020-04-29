from pygame import Surface, Vector2, draw, transform, Rect

from source.entities.hive_data.bee_hive import BeeHive, team_color_dict

background_green = (102, 200, 102)


class Camera:

    def __init__(self, native_resolution, map_size):
        self.native_resolution = native_resolution
        self.render_surface = Surface(native_resolution)
        self.map_size = map_size
        self.zoom_factor = 1
        self.location = Vector2(0, 0)

    def render(self, entities):
        """
        :param entities:
        :return: returns the rendered frame
        """
        # TODO: Don't render pixels that havent changed
        self.render_surface.fill(background_green)

        draw.rect(self.render_surface,
                  (0, 0, 0),
                  (0 - self.location.x,
                   0 - self.location.y,
                   self.map_size[0] * self.zoom_factor + 10,
                   self.map_size[1] * self.zoom_factor + 10),
                  3)

        for entity in entities:
            # TODO: Make only entities in frame render

            scaled_x = int(entity.rect.left * self.zoom_factor) - self.location[0]
            scaled_y = int(entity.rect.top * self.zoom_factor) - self.location[1]
            scaled_width = (int(entity.rect.width * self.zoom_factor))
            scaled_height = (int(entity.rect.height * self.zoom_factor))
            scaled_image = transform.scale(entity.image, (scaled_width, scaled_height))

            self.render_surface.blit(scaled_image, (scaled_x, scaled_y))
            if isinstance(entity, BeeHive):
                entity.scaled_rect = Rect(scaled_x + self.location[0],
                                      scaled_y + self.location[1],
                                      scaled_width, scaled_height)
                self.handle_hive_highways(entity)

        return self.render_surface

    def move(self, destination):
        """
        Moves the camera
        :param destination:
        :return: void
        """
        # TODO: fix the camera going out of borders
        self.location = self.location + destination

    def handle_zoom(self):
        self.render_surface = Surface((int(self.native_resolution[0] * self.zoom_factor),
                                       int(self.native_resolution[1] * self.zoom_factor)))
        self.render_surface = transform.scale(self.render_surface, self.native_resolution)

    def zoom_out(self):
        if self.zoom_factor > .3:
            self.zoom_factor = round(self.zoom_factor - .10, 2)
            self.location *= .10
            self.handle_zoom()

    def zoom_in(self):
        if self.zoom_factor < 2:
            self.zoom_factor = round(self.zoom_factor + .10, 2)
            self.location *= .10
            self.handle_zoom()

    def handle_hive_highways(self, hive):
        """
        Draws lines from the hive to its flowers
        :param hive:
        :return:
        """
        if hive.highlighted:
            for flower in hive.flowers:
                hive_loc = (int(hive.center[0] * self.zoom_factor),
                            int(hive.center[1] * self.zoom_factor))
                flower_loc = (int(flower.center_loc[0] * self.zoom_factor),
                              int(flower.center_loc[1] * self.zoom_factor))

                draw.line(self.render_surface,
                          team_color_dict[hive.team],
                          hive_loc - self.location,
                          flower_loc - self.location,
                          1)

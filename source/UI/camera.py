from pygame import Surface, Vector2, draw, transform, Rect, sprite

from source.entities.hive_data.bee_hive import BeeHive, team_color_dict

grass_color = (102, 200, 102)
water_color = (51, 153, 255)


class Camera:

    def __init__(self, native_resolution, map_size):
        self.native_resolution = native_resolution
        self.render_surface = Surface(native_resolution)
        self.map_size = map_size
        self.frame_sprites = sprite.RenderUpdates()
        self.zoom_factor = 1
        self.location = Vector2(0, 0)

    def make_frame_sprites(self, entities):
        frame_sprites = sprite.RenderUpdates()

        for entity in entities:
            scaled_x = int(entity.rect.left * self.zoom_factor) - self.location[0]
            scaled_y = int(entity.rect.top * self.zoom_factor) - self.location[1]
            if 0 <= scaled_x <= self.native_resolution[0] and 0 <= scaled_y <= self.native_resolution[1]:

                scaled_width = (int(entity.rect.width * self.zoom_factor))
                scaled_height = (int(entity.rect.height * self.zoom_factor))
                scaled_image = transform.scale(entity.image, (scaled_width, scaled_height))

                temp_sprite = sprite.DirtySprite()
                temp_sprite.image = scaled_image
                temp_sprite.rect = temp_sprite.image.get_rect()
                temp_sprite.rect.left, temp_sprite.rect.top = scaled_x, scaled_y

                if isinstance(entity, BeeHive):
                    entity.scaled_rect = Rect(scaled_x + self.location[0],
                                              scaled_y + self.location[1],
                                              scaled_width, scaled_height)
                    self.handle_hive_highways(entity)

                frame_sprites.add(temp_sprite)

        self.frame_sprites = frame_sprites

    def paint_background(self):
        self.render_surface.fill(water_color)
        circle_center = (
            int((self.map_size*self.zoom_factor / 2) - self.location[0]),
            int((self.map_size*self.zoom_factor / 2) - self.location[1])
        )

        draw.circle(self.render_surface,
                    grass_color,
                    circle_center,
                    int(self.map_size * self.zoom_factor))

    def render(self, entities):
        """
        :param entities:
        :return: returns the rendered frame
        """
        self.paint_background()
        self.make_frame_sprites(entities)
        self.frame_sprites.draw(self.render_surface)

    def move(self, destination):
        """
        Moves the camera
        :param destination:
        :return: void
        """
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

from pygame import Vector2, draw, transform, Rect, sprite

from source.entities.hive_data.bee_hive import BeeHive, team_color_dict

grass_color = (102, 200, 102)
water_color = (51, 153, 255)


class Camera:

    def __init__(self, native_resolution, map_size):
        self.native_resolution = native_resolution
        self.map_size = map_size
        self.frame_sprites = sprite.RenderUpdates()
        self.zoom_factor = 1
        self.location = Vector2(0, 0)

    def make_frame_sprites(self, entities, surface):
        """
        Makes scaled sprites ready to be rendered
        :param entities:
        :param surface:
        :return:
        """
        frame_sprites = sprite.RenderUpdates()

        for entity in entities:
            scaled_loc = self.scale_location((entity.rect.left, entity.rect.top))
            if 0 <= scaled_loc[0]+entity.rect.height <= self.native_resolution[0] \
                    and 0 <= scaled_loc[1] <= self.native_resolution[1]:

                scaled_width = (int(entity.rect.width * self.zoom_factor))
                scaled_height = (int(entity.rect.height * self.zoom_factor))
                scaled_image = transform.scale(entity.image, (scaled_width, scaled_height))

                temp_sprite = sprite.DirtySprite()
                temp_sprite.image = scaled_image
                temp_sprite.rect = temp_sprite.image.get_rect()
                temp_sprite.rect.left, temp_sprite.rect.top = scaled_loc

                if isinstance(entity, BeeHive):
                    entity.scaled_rect = Rect(scaled_loc[0] + self.location[0],
                                              scaled_loc[1] + self.location[1],
                                              scaled_width, scaled_height)
                    self.handle_hive_highways(entity, surface)

                frame_sprites.add(temp_sprite)

        self.frame_sprites = frame_sprites

    def paint_background(self, surface):
        """
        Paints the water and island backgrounds
        :param surface:
        :return:
        """
        circle_center = (
            int((self.map_size*self.zoom_factor / 2) - self.location[0]),
            int((self.map_size*self.zoom_factor / 2) - self.location[1])
        )

        radius = int(self.map_size * self.zoom_factor)

        surface.fill(water_color)

        draw.circle(surface,
                    grass_color,
                    circle_center,
                    radius)

    def render(self, entities, surface):
        """
        :param surface:
        :param entities:
        :return: returns the rendered frame
        """
        self.paint_background(surface)
        self.make_frame_sprites(entities, surface)
        self.frame_sprites.draw(surface)

    def scale_location(self, pos):
        """
        Scales given location to its in game coordinate
        :param pos:
        :return:
        """
        scaled_x = int(pos[0] * self.zoom_factor) - self.location[0]
        scaled_y = int(pos[1] * self.zoom_factor) - self.location[1]
        return scaled_x, scaled_y

    def move(self, destination):
        """
        Moves the camera
        :param destination:
        :return: void
        """
        self.location = self.location + destination

    def zoom_out(self):
        if self.zoom_factor > .3:
            self.zoom_factor = round(self.zoom_factor - .10, 2)

    def zoom_in(self):
        if self.zoom_factor < 2:
            self.zoom_factor = round(self.zoom_factor + .10, 2)

    def handle_hive_highways(self, hive, surface):
        """
        Draws lines from the hive to its flowers
        :param surface:
        :param hive:
        :return:
        """
        if hive.highlighted:
            for flower in hive.flowers:
                hive_loc = self.scale_location(hive.center)
                flower_loc = self.scale_location(flower.center_loc)

                draw.line(surface,
                          team_color_dict[hive.team],
                          hive_loc,
                          flower_loc,
                          2)

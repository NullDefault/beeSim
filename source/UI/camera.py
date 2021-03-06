from pygame import Vector2, draw, transform, Rect

from source.entities.decorative_entity import Decoration
from source.entities.flower_data.flower import Flower
from source.entities.hive_data.bee_hive import BeeHive, team_color_dict

grass_color = (100, 200, 100)
water_color = (50, 150, 250)


class Camera:

    def __init__(self, native_resolution, map_size):
        self.native_resolution = native_resolution
        self.map_size = map_size
        self.orientation_changed = True
        self.scaled_sprites = {}
        self.zoom_factor = 1
        self.location = Vector2(0, 0)

    def in_frame(self, location, height):
        """
        Checks if a particular entity is visible in the camera frame
        :param location:
        :param height:
        :return:
        """
        return 0 <= location[0] <= self.native_resolution[0] and 0 <= location[1] + height <= self.native_resolution[1]

    def render_entities(self, entities, surface):
        """
        Renders entities on the provided surface
        :param entities:
        :param surface:
        :return:
        """

        def scale_entity(e):
            """
            Scales an entity according to the current zoom factor
            :param e:
            :return:
            """
            width = (int(e.rect.width * self.zoom_factor))
            height = (int(e.rect.height * self.zoom_factor))
            image = transform.scale(e.image, (width, height))
            return width, height, image

        def handle_hive_highlighting(e):
            if isinstance(e, BeeHive):
                e.scaled_rect = Rect(scaled_loc[0] + self.location[0],
                                     scaled_loc[1] + self.location[1],
                                     scaled_width, scaled_height)
                if e.highlighted:
                    self.handle_hive_highways(e, surface)

        if self.orientation_changed:
            """
            If the orientation has changed (camera moved or zoomed in/out) then we need to rescale the sprites that are
            now in the frame. If the orientation hasn't changed, we use the saved scaled sprites from the previous 
            iteration, which saves us some computing power.
            """
            self.scaled_sprites = {}

        for entity in entities:
            scaled_loc = self.scale_location((entity.rect.left, entity.rect.top))
            if self.in_frame(scaled_loc, entity.rect.height):
                if self.orientation_changed:
                    scaled_width, scaled_height, scaled_image = scale_entity(entity)
                    self.scaled_sprites[entity] = (scaled_image, (scaled_width, scaled_height))
                else:
                    if not isinstance(entity, Flower) and not isinstance(entity, Decoration):
                        scaled_width, scaled_height, scaled_image = scale_entity(entity)
                    else:
                        scaled_entity_data = self.scaled_sprites[entity]
                        scaled_width = scaled_entity_data[1][0]
                        scaled_height = scaled_entity_data[1][1]
                        scaled_image = scaled_entity_data[0]

                surface.blit(scaled_image, scaled_loc)

                handle_hive_highlighting(entity)

        if self.orientation_changed:
            self.orientation_changed = False

    def paint_background(self, surface):
        """
        Paints the water and island backgrounds
        :param surface:
        :return:
        """
        circle_center = (
            int((self.map_size * self.zoom_factor / 2) - self.location[0]),
            int((self.map_size * self.zoom_factor / 2) - self.location[1])
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
        self.render_entities(entities, surface)

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
        self.orientation_changed = True
        self.location = self.location + destination

    def zoom_out(self):
        self.orientation_changed = True
        if self.zoom_factor > .3:
            self.zoom_factor = round(self.zoom_factor - .10, 2)

    def zoom_in(self):
        self.orientation_changed = True
        if self.zoom_factor < 2:
            self.zoom_factor = round(self.zoom_factor + .10, 2)

    def handle_hive_highways(self, hive, surface):
        """
        Draws lines from the hive to its flowers
        :param surface:
        :param hive:
        :return:
        """
        for flower in hive.flowers:
            if not flower.alive():
                hive.flowers.remove(flower)
            else:
                hive_loc = self.scale_location(hive.center)
                flower_loc = self.scale_location(flower.center_loc)

                draw.line(surface,
                          team_color_dict[hive.team],
                          hive_loc,
                          flower_loc,
                          2)

"""
Class Name: Entity Master
Class Purpose: Handles logic behind entities
Notes:
"""

#  IMPORTS
from random import randint

from pygame.sprite import RenderUpdates, collide_circle_ratio, spritecollide, spritecollideany
from pygame.time import get_ticks
from pygame import Vector2

from source.entities.bee_data.scout_bee import ScoutBee
from source.entities.bee_data.worker_bee import WorkerBee
from source.logic_and_algorithms.random_generators import grow_plants
from source.logic_and_algorithms.spawn_strategies import get_hive_spawn_strategy, get_flower_spawn_strategy


# CLASS BODY


def merge_plant_sets(origin_dict, merging_dict):
    """
    :param origin_dict:
    :param merging_dict:
    :return: Merges the two dictionaries merged together, correcting for overlapping plants
    """

    for plant in merging_dict.values():
        collision = spritecollideany(plant, origin_dict.values())
        if collision:
            move_dir = Vector2(plant.rect.left, plant.rect.top) - Vector2(collision.rect.left, collision.rect.top)
            plant.rect.left = plant.rect.left + move_dir.x
            plant.rect.top = plant.rect.top + move_dir.y

    return {**origin_dict, **merging_dict}


class EntityMaster:
    # DATA FIELDS

    bee_ratio = 5

    # FUNCTIONS

    def __init__(self, initial_hives: int, default_bees_per_hive: int, play_area_dimensions: int(),
                 flower_spawn_strategy: str, hive_spawn_strategy: str):

        self.bees = RenderUpdates()
        self.hives = RenderUpdates()
        self.plants = RenderUpdates()
        self.flowers = RenderUpdates()
        self.ui_elements = RenderUpdates()
        self.crosshairs = RenderUpdates()

        self.flower_database = {}
        self.play_area = play_area_dimensions

        self.sim_paused = False

        self.grow_flora(play_area_dimensions)
        self.load_flower_data(get_flower_spawn_strategy(flower_spawn_strategy, play_area_dimensions))
        self.populate_hives(
            get_hive_spawn_strategy(hive_spawn_strategy, initial_hives, play_area_dimensions, self.flowers),
            default_bees_per_hive)
        self.clean_up_spawn()

    @property
    def bee_population(self):
        """
        :return: Total number of bees in the simulation
        """
        return len(self.bees)

    @property
    def flower_population(self):
        """
        :return: Total number of flowers in the simulation
        """
        return len(self.flowers)

    def get_valid_entities(self):
        """
        :return: Entities that need to be rendered next frame
        """
        self.update_game_state()

        valid_entities = RenderUpdates()
        valid_entities.add(self.plants)
        valid_entities.add(self.flowers)
        valid_entities.add(self.hives)
        valid_entities.add(self.bees)
        valid_entities.add(self.crosshairs)
        valid_entities.add(self.ui_elements)

        return valid_entities

    def update_game_state(self):
        """
        :return: void
        """
        for hive in self.hives:
            hive.last_tick = get_ticks()
            self.handle_hive_highlighting(hive)

        if not self.sim_paused:
            for bee in self.bees:  # If the sim is not paused, we update the states of the bees
                bee.update()
                self.update_bee_crosshair(bee)
                bee.handle_collisions(self.flowers)
        else:
            for bee in self.bees:  # If the sim is paused we only update the crosshairs
                self.update_bee_crosshair(bee)

        for flower in self.flowers:
            if flower.inspecting_hives.__len__() == 0:
                self.crosshairs.remove(flower.crosshair)
            else:
                self.crosshairs.add(flower.crosshair)
                flower.inspecting_hives[flower.inspecting_hives.__len__()-1].recolor_crosshair(flower)

    def update_bee_crosshair(self, bee):
        """
        Updates the state of the bee crosshair, adding it to the list of rendered entities if necessary
        :param bee:
        :return: void
        """
        if not bee.highlighted:
            bee.crosshair.kill()
        else:
            self.crosshairs.add(bee.crosshair)
            bee.crosshair.follow()

    def handle_hive_highlighting(self, hive):
        """
        Takes care of everything that has to do with hive highlighting, adding the needed ui elements if necessary
        :param hive:
        :return:
        """
        if not self.ui_elements.__contains__(hive.honey_bar) and hive.highlighted:
            self.ui_elements.add(hive.honey_bar)
            self.ui_elements.add(hive.scout_counter)
            self.ui_elements.add(hive.worker_counter)
        if hive.highlighted:
            hive.honey_bar.draw_honey()
            hive.scout_counter.render()
            hive.worker_counter.render()
        elif not hive.highlighted:
            self.ui_elements.remove(hive.honey_bar)
            self.ui_elements.remove(hive.scout_counter)
            self.ui_elements.remove(hive.worker_counter)

    def populate_hives(self, hives, bees_per_hive):
        """
        Populates the hives with bees
        :param hives:
        :param bees_per_hive:
        :return:
        """
        for hive in hives:
            self.hives.add(hive)
            self.spawn_initial_bees(hive, bees_per_hive)

    def spawn_initial_bees(self, hive, bees_per_hive):
        """
        Fills an individual hive with bees
        :param hive:
        :param bees_per_hive:
        :return:
        """
        scouts = int(bees_per_hive / self.bee_ratio)
        workers = bees_per_hive - scouts

        for j in range(workers):
            new_bee = \
                WorkerBee((hive.center.x + randint(-10, 10),
                           hive.center.y + randint(-10, 10)),
                          hive)
            self.crosshairs.add(new_bee.crosshair)
            hive.add_worker_bee(new_bee)
            self.bees.add(new_bee)

        for j in range(scouts):
            new_bee = \
                ScoutBee((hive.center.x + randint(-50, 50),
                          hive.center.y + randint(-50, 50)),
                         hive)
            self.crosshairs.add(new_bee.crosshair)
            hive.add_scout_bee(new_bee)
            self.bees.add(new_bee)

    def clean_up_spawn(self):
        """
        Removes flowers that are colliding with hives and adds UI elements to the hives
        :return:
        """
        for hive in self.hives:
            flowers = self.flowers
            spritecollide(hive, flowers, True, collide_circle_ratio(1.3))
            self.ui_elements.add(hive.honey_bar, hive.worker_counter, hive.scout_counter)

    def load_flower_data(self, data):
        """
        Loads the list of flowers
        :param data:
        :return:
        """
        self.flower_database = data
        self.flowers = RenderUpdates(list((data.values())))

    def grow_flora(self, play_area):
        """
        Grows the decorative plants
        :param play_area:
        :return: void
        """

        plant_db = grow_plants(play_area, num=randint(80, 90), plant_type="grass_patch", bias="center")

        plant_db = merge_plant_sets(plant_db,
                                         grow_plants(
                                             play_area, num=randint(40, 70), plant_type="grassy_plant", bias="edges"))
        plant_db = merge_plant_sets(plant_db,
                                         grow_plants(
                                             play_area, num=randint(0, 1), plant_type="pretty_log", bias="edges"))
        plant_db = merge_plant_sets(plant_db,
                                         grow_plants(
                                             play_area, num=randint(0, 2), plant_type="stump", bias="edges"))
        plant_db = merge_plant_sets(plant_db,
                                         grow_plants(
                                             play_area, num=randint(20, 40), plant_type="leaves", bias="edges"))
        plant_db = merge_plant_sets(plant_db,
                                         grow_plants(
                                             play_area, num=randint(10, 30), plant_type="bushy_grass", bias="edges"))

        self.plants = RenderUpdates(list(plant_db.values()))

    def get_hive_at(self, position):
        """
        :param position:
        :return: Hive at given location, None if there are none such.
        """
        for hive in self.hives:
            if hive.rect.collidepoint(position):
                return hive
        else:
            return None

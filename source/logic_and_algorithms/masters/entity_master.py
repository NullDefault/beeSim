"""
Class Name: Entity Master
Class Purpose: Handles logic behind entities
Notes:
"""

#  IMPORTS
from random import randint, random

from pygame import Vector2
from pygame.sprite import RenderUpdates, collide_circle_ratio, spritecollide, spritecollideany
from pygame.time import get_ticks

from source.entities.bee_data.scout_bee import ScoutBee
from source.entities.bee_data.worker_bee import WorkerBee
from source.logic_and_algorithms.random_generators import grow_plants
from source.logic_and_algorithms.spawn_strategies import get_hive_spawn_strategy, get_flower_spawn_strategy


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
                 flower_spawn_strategy: str, hive_spawn_strategy: str, flower_num: int):

        self.bees = RenderUpdates()
        self.hives = RenderUpdates()
        self.plants = RenderUpdates()
        self.flowers = RenderUpdates()
        self.ui_elements = RenderUpdates()

        self.flower_database = {}
        self.play_area = play_area_dimensions

        self.sim_paused = False

        self.grow_flora(play_area_dimensions)
        self.load_flower_data(get_flower_spawn_strategy(flower_spawn_strategy, play_area_dimensions, flower_num))
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

    def get_entities(self):
        """
        :return: Entities that need to be rendered next frame
        """
        self.update_game_state()

        return self.plants.sprites() + self.flowers.sprites() + \
               self.hives.sprites() + self.bees.sprites() + self.ui_elements.sprites()

    def update_game_state(self):
        """
        :return: void
        """
        for hive in self.hives:
            hive.last_tick = get_ticks()
            self.handle_hive_highlighting(hive)
            if hive.current_nectar == hive.max_nectar:
                self.hive_purchase_bee(hive)

        for flower in self.flowers:
            if flower.pollen == 0:
                flower.crosshair.kill()
                flower.kill()
                for hive in self.hives:
                    if flower in hive.flowers:
                        hive.flowers.remove(flower)
            else:
                if flower.inspecting_hives.__len__() == 0:
                    self.ui_elements.remove(flower.crosshair)
                else:
                    self.ui_elements.add(flower.crosshair)
                    flower.inspecting_hives[flower.inspecting_hives.__len__() - 1].recolor_crosshair(flower)

        if not self.sim_paused:
            for bee in self.bees:  # If the sim is not paused, we update the states of the bees
                bee.update()
                self.update_bee_crosshair(bee)
                bee.handle_collisions(self.flowers)

        else:
            for bee in self.bees:  # If the sim is paused we only update the crosshairs
                self.update_bee_crosshair(bee)

    def update_bee_crosshair(self, bee):
        """
        Updates the state of the bee crosshair, adding it to the list of rendered entities if necessary
        :param bee:
        :return: void
        """
        if not bee.highlighted:
            bee.crosshair.kill()
        else:
            self.ui_elements.add(bee.crosshair)
            bee.crosshair.follow()

    def handle_hive_highlighting(self, hive):
        """
        Takes care of everything that has to do with hive highlighting, adding the needed ui elements if necessary
        :param hive:
        :return:
        """
        if not hive.highlighted:
            hive.honey_bar.kill()
        else:
            self.ui_elements.add(hive.honey_bar)
            hive.honey_bar.update()

    def add_worker(self, hive):
        """
        Adds a worker bee to the given hive
        :param hive:
        :return:
        """
        new_bee = \
            WorkerBee((hive.center.x + randint(-10, 10),
                       hive.center.y + randint(-10, 10)),
                      hive)
        self.ui_elements.add(new_bee.crosshair)
        hive.add_worker_bee(new_bee)
        self.bees.add(new_bee)

    def add_scout(self, hive):
        """
        Adds a scout bee to the given hive
        :param hive:
        :return:
        """
        new_bee = \
            ScoutBee((hive.center.x + randint(-50, 50),
                      hive.center.y + randint(-50, 50)),
                     hive)
        self.ui_elements.add(new_bee.crosshair)
        hive.add_scout_bee(new_bee)
        self.bees.add(new_bee)

    def hive_purchase_bee(self, hive):
        """
        Provided hive purchases a bee using some of its honey
        :param hive:
        :return:
        """
        hive.buy_bee()
        bee_roll = random()
        if bee_roll >= 1 / self.bee_ratio:
            self.add_scout(hive)
        else:
            self.add_worker(hive)

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
            self.add_worker(hive)

        for j in range(scouts):
            self.add_scout(hive)

    def clean_up_spawn(self):
        """
        Removes flowers that are colliding with hives and adds UI elements to the hives
        :return:
        """
        for hive in self.hives:
            flowers = self.flowers
            spritecollide(hive, flowers, True, collide_circle_ratio(1))

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

        plant_db = grow_plants(play_area, num=randint(90, 150), plant_type="grass", bias="center")

        plant_db = merge_plant_sets(plant_db,
                                    grow_plants(
                                        play_area, num=randint(50, 75), plant_type="grassy_plant", bias="edges"))
        plant_db = merge_plant_sets(plant_db,
                                    grow_plants(
                                        play_area, num=randint(1, 2), plant_type="pretty_log", bias="edges"))
        plant_db = merge_plant_sets(plant_db,
                                    grow_plants(
                                        play_area, num=randint(0, 3), plant_type="stump", bias="edges"))
        plant_db = merge_plant_sets(plant_db,
                                    grow_plants(
                                        play_area, num=randint(25, 55), plant_type="leaves", bias="edges"))
        plant_db = merge_plant_sets(plant_db,
                                    grow_plants(
                                        play_area, num=randint(15, 25), plant_type="bushy_grass", bias="edges"))

        self.plants = RenderUpdates(list(plant_db.values()))

    def get_hive_at(self, position):
        """
        :param position:
        :return: Hive at given location, None if there are none such.
        """
        for hive in self.hives:
            if hive.scaled_rect.collidepoint(position):
                return hive
        else:
            return None

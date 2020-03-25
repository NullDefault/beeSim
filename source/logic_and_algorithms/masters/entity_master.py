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

        self.grow_flora(play_area_dimensions)
        self.load_flower_data(get_flower_spawn_strategy(flower_spawn_strategy, play_area_dimensions))
        self.populate_hives(
            get_hive_spawn_strategy(hive_spawn_strategy, initial_hives, play_area_dimensions, self.flowers),
            default_bees_per_hive)
        self.clean_up_spawn()

    @property
    def bee_population(self):  # Get number of bees on the board
        return len(self.bees)

    @property
    def flower_population(self):
        return len(self.flowers)

    def get_valid_entities(self):  # Returns entities to render next rendering step
        self.update_game_state()

        valid_entities = RenderUpdates()
        valid_entities.add(self.plants)
        valid_entities.add(self.flowers)
        valid_entities.add(self.hives)
        valid_entities.add(self.bees)
        valid_entities.add(self.crosshairs)
        valid_entities.add(self.ui_elements)

        return valid_entities

    def update_game_state(self):  # Updates the game state
        for hive in self.hives:
            hive.last_tick = get_ticks()

            if hive.highlighted and not self.ui_elements.__contains__(hive.honey_bar):
                self.ui_elements.add(hive.honey_bar)
                self.ui_elements.add(hive.scout_counter)
                self.ui_elements.add(hive.worker_counter)
            if hive.highlighted and self.ui_elements.__contains__(hive.honey_bar):
                hive.honey_bar.draw_honey()
                hive.scout_counter.render()
                hive.worker_counter.render()
            elif not hive.highlighted:
                self.ui_elements.remove(hive.honey_bar)
                self.ui_elements.remove(hive.scout_counter)
                self.ui_elements.remove(hive.worker_counter)

        for bee in self.bees:
            bee.update()
            if not bee.highlighted:
                bee.crosshair.kill()
            else:
                bee.crosshair.add(self.crosshairs)
                bee.crosshair.follow()
            bee.handle_collisions(self.flowers)

    def populate_hives(self, hives, bees_per_hive):  # Populates the new hives with bees
        for hive in hives:
            self.hives.add(hive)
            self.spawn_initial_bees(hive, bees_per_hive)

    def spawn_initial_bees(self, hive, bees_per_hive):  # Spawns initial bees for a given hive

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

    def clean_up_spawn(self):  # remove flowers under hives and add their ui elements to the ui_elements group
        for hive in self.hives:
            flowers = self.flowers
            spritecollide(hive, flowers, True, collide_circle_ratio(1.3))
            self.ui_elements.add(hive.honey_bar, hive.worker_counter, hive.scout_counter)

    def load_flower_data(self, data):  # Load updated flower data
        self.flower_database = data
        self.flowers = RenderUpdates(list((data.values())))

    def grow_flora(self, play_area):
        # Ideally we want the amount of plants to somehow relate to the size of the play area

        plant_db = grow_plants(play_area, num=randint(65, 80), plant_type="grass_patch", bias="center")

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

    def get_hive_at(self, position):  # Get hive at given location
        for hive in self.hives:
            if hive.rect.collidepoint(position):
                return hive
        else:
            return None

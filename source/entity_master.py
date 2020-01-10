from source.bees.scout_bee import ScoutBee
from source.bees.worker_bee import WorkerBee
from source.spawn_strategies import get_hive_spawn_strategy, get_flower_spawn_strategy
import pygame
from random import randint


class EntityMaster:

    scout_ratio = .2
    worker_ratio = .8

    bee_spawn_offset = (-50, 50)

    def __init__(self, initial_hives: int, default_bees_per_hive: int,
                 number_of_flower_zones: int, initial_growth_stages: int, play_area_dimensions: int(),
                 flower_spawn_strategy: str, hive_spawn_strategy: str):

        self.beeEntities = pygame.sprite.RenderUpdates()
        self.hiveEntities = pygame.sprite.RenderUpdates()
        self.flowerEntities = pygame.sprite.RenderUpdates()

        self.flowerDatabase = {}
        self.playArea = play_area_dimensions

        spawn_vars = {
            'flower_zones': number_of_flower_zones,
            'initial_growth_stages': initial_growth_stages
        }

        self.load_flower_data(get_flower_spawn_strategy(flower_spawn_strategy, spawn_vars, play_area_dimensions))
        self.populate_hives(
            get_hive_spawn_strategy(hive_spawn_strategy, initial_hives, play_area_dimensions, self.flowerEntities),
            default_bees_per_hive)

    def get_valid_entities(self):

        self.update_game_state()

        valid_entities = pygame.sprite.RenderUpdates()

        valid_entities.add(self.flowerEntities)
        valid_entities.add(self.hiveEntities)
        valid_entities.add(self.beeEntities)

        return valid_entities

    def update_game_state(self):
        for hive in self.hiveEntities:
            hive.last_tick = pygame.time.get_ticks()
        for bee in self.beeEntities:
            bee.move()

        bee_and_flower_collisions = pygame.sprite.groupcollide(self.beeEntities, self.flowerEntities, False, False)

        for bee_in_question in bee_and_flower_collisions:
            if bee_in_question.validate_collision():
                bee_in_question.collide_with_flower(bee_and_flower_collisions.get(bee_in_question)[0])

########################################################################################################################
# Functions That Spawn the Initial Game State

    def populate_hives(self, hives, bees_per_hive):
        for hive in hives:

            self.hiveEntities.add(hive)

            self.spawn_initial_bees(hive, bees_per_hive)

    def spawn_initial_bees(self, hive, bees_per_hive):

        workers = int(bees_per_hive * self.worker_ratio)
        scouts = int(bees_per_hive * self.scout_ratio)

        for j in range(workers):
            new_bee = \
                WorkerBee((hive.center[0] + randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1]),
                           hive.center[1] + randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1])),
                          hive)
            hive.add_worker_bee(new_bee)
            self.beeEntities.add(new_bee)

        for j in range(scouts):
            new_bee = \
                ScoutBee((hive.center[0] + randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1]),
                          hive.center[1] + randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1])),
                         hive)
            hive.add_scout_bee(new_bee)
            self.beeEntities.add(new_bee)

    def load_flower_data(self, data):
        self.flowerDatabase = data
        self.flowerEntities = data.values()

    def get_bee_population(self):
        return len(self.beeEntities)

    def get_hive_at(self, position):
        for hive in self.hiveEntities:
            if hive.rect.left <= position[0] <= hive.rect.left + 66 and \
                    hive.rect.top <= position[1] <= hive.rect.top + 66:
                return hive
        else:
            return None

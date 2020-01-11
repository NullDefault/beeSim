"""
Class Name: Entity Master
Class Purpose: Handles logic behind entities
Notes:
"""

#  IMPORTS
from pygame.sprite import RenderUpdates, groupcollide
from pygame.time import get_ticks
from random import randint
from source.entities.bee_data.scout_bee import ScoutBee
from source.entities.bee_data.worker_bee import WorkerBee
from source.logic_and_algorithms.spawn_strategies import get_hive_spawn_strategy, get_flower_spawn_strategy


# CLASS BODY


class EntityMaster:

    # DATA FIELDS

    scout_ratio = .2  # 1/5 of a hive are scouts
    worker_ratio = .8  # 4/5 of a hive are workers

    bee_spawn_offset = (-50, 50)

    # FUNCTIONS

    def __init__(self, initial_hives: int, default_bees_per_hive: int,
                 number_of_flower_zones: int, initial_growth_stages: int, play_area_dimensions: int(),
                 flower_spawn_strategy: str, hive_spawn_strategy: str):

        self.bee_entities = RenderUpdates()
        self.hive_entities = RenderUpdates()
        self.flower_entities = RenderUpdates()

        self.flower_database = {}
        self.play_area = play_area_dimensions

        spawn_vars = {
            'flower_zones': number_of_flower_zones,
            'initial_growth_stages': initial_growth_stages
        }

        self.load_flower_data(get_flower_spawn_strategy(flower_spawn_strategy, spawn_vars, play_area_dimensions))
        self.populate_hives(
            get_hive_spawn_strategy(hive_spawn_strategy, initial_hives, play_area_dimensions, self.flower_entities),
            default_bees_per_hive)

    def get_valid_entities(self):  # Returns entities to render next rendering step

        self.update_game_state()

        valid_entities = RenderUpdates()

        valid_entities.add(self.flower_entities)
        valid_entities.add(self.hive_entities)
        valid_entities.add(self.bee_entities)

        return valid_entities

    def update_game_state(self):  # Updates the game state
        for hive in self.hive_entities:
            hive.last_tick = get_ticks()
        for bee in self.bee_entities:
            bee.move()

        bee_and_flower_collisions = groupcollide(self.bee_entities, self.flower_entities, False, False)

        for bee_in_question in bee_and_flower_collisions:
            if bee_in_question.validate_collision():
                bee_in_question.collide_with_flower(bee_and_flower_collisions.get(bee_in_question)[0])

    def populate_hives(self, hives, bees_per_hive):  # Populates the new hives with bees
        for hive in hives:

            self.hive_entities.add(hive)

            self.spawn_initial_bees(hive, bees_per_hive)

    def spawn_initial_bees(self, hive, bees_per_hive):  # Spawns initial bees for a given hive

        workers = int(bees_per_hive * self.worker_ratio)
        scouts = int(bees_per_hive * self.scout_ratio)

        for j in range(workers):
            new_bee = \
                WorkerBee((hive.center[0] + randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1]),
                           hive.center[1] + randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1])),
                          hive)
            hive.add_worker_bee(new_bee)
            self.bee_entities.add(new_bee)

        for j in range(scouts):
            new_bee = \
                ScoutBee((hive.center[0] + randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1]),
                          hive.center[1] + randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1])),
                         hive)
            hive.add_scout_bee(new_bee)
            self.bee_entities.add(new_bee)

    def load_flower_data(self, data):  # Load updated flower data
        self.flower_database = data
        self.flower_entities = data.values()

    def get_bee_population(self):  # Get number of bees on the board
        return len(self.bee_entities)

    def get_hive_at(self, position):  # Get hive at given location
        for hive in self.hive_entities:
            if hive.rect.left <= position[0] <= hive.rect.left + 66 and \
                    hive.rect.top <= position[1] <= hive.rect.top + 66:
                return hive
        else:
            return None

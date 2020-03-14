"""
Class Name: Entity Master
Class Purpose: Handles logic behind entities
Notes:
"""

#  IMPORTS
from pygame.sprite import RenderUpdates, groupcollide, collide_circle_ratio, spritecollide
from source.entities.background import Background
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

    # FUNCTIONS

    def __init__(self, initial_hives: int, default_bees_per_hive: int,
                 number_of_flower_zones: int, initial_growth_stages: int, play_area_dimensions: int(),
                 flower_spawn_strategy: str, hive_spawn_strategy: str):

        self.background = Background()
        self.bee_entities = RenderUpdates()
        self.hive_entities = RenderUpdates()
        self.flower_entities = RenderUpdates()
        self.ui_elements = RenderUpdates()

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
        self.clean_up_spawn()

    def get_valid_entities(self):  # Returns entities to render next rendering step

        self.update_game_state()

        valid_entities = RenderUpdates(self.background)

        valid_entities.add(self.flower_entities)
        valid_entities.add(self.hive_entities)
        valid_entities.add(self.bee_entities)
        valid_entities.add(self.ui_elements)
        return valid_entities

    def update_game_state(self):  # Updates the game state
        for hive in self.hive_entities:
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

        for bee in self.bee_entities:
            bee.move()

        bee_and_flower_collisions = groupcollide(self.bee_entities, self.flower_entities, False, False)

        for bee_in_question in bee_and_flower_collisions:
            flower = bee_and_flower_collisions.get(bee_in_question)[0]
            if bee_in_question.validate_collision():
                if isinstance(bee_in_question, ScoutBee) and \
                        flower not in bee_in_question.queen_hive.known_flowers:
                    bee_in_question.collide_with_flower(flower)
                if isinstance(bee_in_question, WorkerBee):
                    bee_in_question.collide_with_flower(flower)

    def populate_hives(self, hives, bees_per_hive):  # Populates the new hives with bees
        for hive in hives:

            self.hive_entities.add(hive)

            self.spawn_initial_bees(hive, bees_per_hive)

    def spawn_initial_bees(self, hive, bees_per_hive):  # Spawns initial bees for a given hive

        workers = int(bees_per_hive * self.worker_ratio)
        scouts = int(bees_per_hive * self.scout_ratio)

        for j in range(workers):
            new_bee = \
                WorkerBee((hive.center.x + randint(-50, 50),
                           hive.center.y + randint(-50, 50)),
                           hive)
            hive.add_worker_bee(new_bee)
            self.bee_entities.add(new_bee)

        for j in range(scouts):
            new_bee = \
                ScoutBee((hive.center.x + randint(-50, 50),
                          hive.center.y + randint(-50, 50)),
                          hive)
            hive.add_scout_bee(new_bee)
            self.bee_entities.add(new_bee)

    def clean_up_spawn(self):   # remove flowers under hives and add their ui elements to the ui_elements group
        for hive in self.hive_entities:
            flowers = self.flower_entities
            spritecollide(hive, flowers, True, collide_circle_ratio(1.3))
            self.ui_elements.add(hive.honey_bar, hive.worker_counter, hive.scout_counter)

    def load_flower_data(self, data):  # Load updated flower data
        self.flower_database = data
        self.flower_entities = RenderUpdates(list((data.values())))

    def get_hive_at(self, position):  # Get hive at given location
        for hive in self.hive_entities:
            if hive.rect.collidepoint(position):
                return hive
        else:
            return None

    @property
    def bee_population(self):  # Get number of bees on the board
        return len(self.bee_entities)


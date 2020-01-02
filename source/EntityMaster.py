from source import beeHiveData
from source.scout_bee import ScoutBee
from source.worker_bee import WorkerBee
from source import flowerData
import pygame
import math
import random


class EntityMaster:
    test = False

    scout_ratio = .2
    worker_ratio = .8

    used_coordinates = []
    acceptable_hive_distance = 75
    bee_spawn_offset = (-50, 50)

    flowerLowRange = 6
    flowerHighRange = 10

    def __init__(self, initial_hives, default_bee_number, initial_flower_beds, screen_size):

        self.beeEntities = pygame.sprite.RenderUpdates()
        self.hiveEntities = pygame.sprite.RenderUpdates()
        self.flowerEntities = pygame.sprite.RenderUpdates()

        self.hive_spawn_range_x = (screen_size[0] * .1, screen_size[0] * .9)
        self.hive_spawn_range_y = (screen_size[1] * .2, screen_size[1] * .8)

        self.flower_spawn_range_x = (screen_size[0] * .05, screen_size[0] * .95)
        self.flower_spawn_range_y = (screen_size[1] * .1, screen_size[1] * .9)

        self.spawn_hives(initial_hives, default_bee_number)
        self.spawn_initial_flowers(initial_flower_beds)

    def get_renderable_entities(self):

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

    def spawn_hives(self, number_of_hives, bees_per_hive):

        for i in range(number_of_hives):
            done = False
            while not done:
                x_hive_coordinate = random.randint(self.hive_spawn_range_x[0], self.hive_spawn_range_x[1])
                y_hive_coordinate = random.randint(self.hive_spawn_range_y[0], self.hive_spawn_range_y[1])
                done = True
                for n in self.used_coordinates:
                    distance = abs(math.sqrt(pow(n[0] - x_hive_coordinate, 2) + pow(n[1] - y_hive_coordinate, 2)))
                    if distance < self.acceptable_hive_distance:
                        done = False

                self.used_coordinates.append((x_hive_coordinate, y_hive_coordinate))

            new_hive = beeHiveData.BeeHive((x_hive_coordinate, y_hive_coordinate))

            self.hiveEntities.add(new_hive)

            self.spawn_initial_bees(new_hive, bees_per_hive)

    def spawn_initial_bees(self, hive, bees_per_hive):

        workers = int(bees_per_hive * self.worker_ratio)
        scouts = int(bees_per_hive * self.scout_ratio)

        for j in range(workers):
            new_bee = \
                WorkerBee((hive.center[0] + random.randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1]),
                           hive.center[1] + random.randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1])),
                          hive)
            hive.add_worker_bee(new_bee)
            self.beeEntities.add(new_bee)

        for j in range(scouts):
            new_bee = \
                ScoutBee((hive.center[0] + random.randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1]),
                          hive.center[1] + random.randint(self.bee_spawn_offset[0], self.bee_spawn_offset[1])),
                         hive)
            hive.add_scout_bee(new_bee)
            self.beeEntities.add(new_bee)

    def spawn_initial_flowers(self, number_of_flower_beds):

        for k in range(number_of_flower_beds):
            bed_location = (random.randint(self.flower_spawn_range_x[0], self.flower_spawn_range_x[1]),
                            random.randint(self.flower_spawn_range_y[0], self.flower_spawn_range_y[1]))

            number_of_flowers = (random.randint(self.flowerLowRange, self.flowerHighRange))

            for l in range(number_of_flowers):
                r = 100 * math.sqrt(random.random())
                theta = random.random() * 42 * math.pi

                if random.randint(0, 1) == 0:
                    random_x_coordinate = bed_location[0] + (r * math.cos(theta))
                else:
                    random_x_coordinate = bed_location[0] - (r * math.cos(theta))
                if random.randint(0, 1) == 1:
                    random_y_coordinate = bed_location[1] + (r * math.sin(theta))
                else:
                    random_y_coordinate = bed_location[1] - (r * math.sin(theta))

                new_flower = flowerData.Flower((random_x_coordinate, random_y_coordinate))
                self.flowerEntities.add(new_flower)

    def get_bee_population(self):
        return len(self.beeEntities)

    def get_hive_at(self, position):
        for hive in self.hiveEntities:
            if hive.rect.left <= position[0] <= hive.rect.left + 66 and \
                    hive.rect.top <= position[1] <= hive.rect.top + 66:
                return hive
        else:
            return None

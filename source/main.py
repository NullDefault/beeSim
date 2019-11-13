import pygame
import sys
import random
import math
from source import meadow
from source import background
from source import beeHiveData
from source import flowerData
from source import beeData
########################################################################################################################
# Data Fields


_meadow = meadow.Meadow()  # Meadow Class is basically the "Board"
_background = background.Background((0, 0))  # This is just the background

_hives = pygame.sprite.RenderUpdates()
_hiveNumber = 8
used_coordinates = []
_hive_spawn_range = (60, 940)
acceptable_hive_distance = 75

_bees = pygame.sprite.RenderUpdates()
_beesPerHive = 10
_bee_spawn_offset = (-30, 30)


_flowers = pygame.sprite.RenderUpdates()
_initialFlowerBeds = 10
_flowers_per_bed = 10
_flower_spawn_range = (0, 1000)
_flower_bed_spawning_offset = (-30, 30)


########################################################################################################################


def spawn_hives(number_of_hives, bees_per_hive):
    for i in range(number_of_hives):

        done = False
        while not done:
            x_hive_coordinate = random.randint(_hive_spawn_range[0], _hive_spawn_range[1])
            y_hive_coordinate = random.randint(_hive_spawn_range[0], _hive_spawn_range[1])
            done = True
            for n in used_coordinates:
                distance = abs(math.sqrt(pow(n[0] - x_hive_coordinate, 2) + pow(n[1] - y_hive_coordinate, 2)))
                if distance < acceptable_hive_distance:
                    done = False

            used_coordinates.append((x_hive_coordinate, y_hive_coordinate))

        new_hive = beeHiveData.BeeHive((x_hive_coordinate, y_hive_coordinate))

        _hives.add(new_hive)

        for j in range(bees_per_hive):
            new_bee = beeData.Bee((x_hive_coordinate+random.randint(_bee_spawn_offset[0], _bee_spawn_offset[1]),
                                   y_hive_coordinate+random.randint(_bee_spawn_offset[0], _bee_spawn_offset[1])),
                                  new_hive)
            _bees.add(new_bee)
########################################################################################################################


def spawn_flowers(number_of_flowers):
    for i in range(number_of_flowers):
        flower_type = random.randint(1, 3)
        flower_bed_seed = (random.randint(_flower_spawn_range[0], _flower_spawn_range[1]),
                           random.randint(_flower_spawn_range[0], _flower_spawn_range[1]))
        for i in range(_flowers_per_bed):
            x_random = random.randint(_flower_bed_spawning_offset[0], _flower_bed_spawning_offset[1])
            y_random = random.randint(_flower_bed_spawning_offset[0], _flower_bed_spawning_offset[1])
            new_flower = flowerData.Flower((flower_bed_seed[0] + x_random, flower_bed_seed[1] + y_random)
                                           , flower_type)
            _flowers.add(new_flower)

########################################################################################################################


def main():
########################################################################################################################
# Init Screen

    screen = pygame.display.set_mode(_meadow._size)

########################################################################################################################
# Init Music
    pygame.mixer.init()
    pygame.mixer.music.load("assets/beeMusic.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0)

########################################################################################################################
# Spawn Hives
    spawn_hives(_hiveNumber, _beesPerHive)
########################################################################################################################
# Spawn Flowers
    spawn_flowers(_initialFlowerBeds)
########################################################################################################################
# Main Game Loop
    while True:
        screen.blit(_background.image, _background.rect)

        _hives.draw(screen)

        for flower in _flowers:
            screen.blit(flower.image, flower.rect)
        for bee in _bees:
            bee.move()
            screen.blit(bee.image, bee.rect)

        pygame.display.flip()
        pygame.time.delay(24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
########################################################################################################################


if __name__ == "__main__":
    main()

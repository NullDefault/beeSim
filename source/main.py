import pygame
import sys
import random
import math
from source import meadow
from source import gameBoard
from source import beeHiveData
from source import flowerData
from source import beeData
########################################################################################################################
# Data Fields


_meadow = meadow.Meadow()  # Meadow Class is basically the "Board"
_background = gameBoard.Background((0, 0))  # This is just the background

_hives = pygame.sprite.RenderUpdates()
_hiveNumber = 8
used_coordinates = []
_hive_spawn_range_x = (200, 1400)
_hive_spawn_range_y = (200, 600)
acceptable_hive_distance = 75

_bees = pygame.sprite.RenderUpdates()
_beesPerHive = 5
_bee_spawn_offset = (-30, 30)


_flowers = pygame.sprite.RenderUpdates()
_initialFlowerBeds = 80
_flowers_per_bed = 10
_flower_spawn_range_x = (100, 1500)
_flower_spawn_range_y = (50, 850)
_flower_bed_spawning_offset = (-30, 30)
_flower_type_number = 1

frame_delay = 0
tick_cycle = 100
tick_gain = 1

########################################################################################################################


def spawn_hives(number_of_hives, bees_per_hive):

    for i in range(number_of_hives):
        done = False
        while not done:
            x_hive_coordinate = random.randint(_hive_spawn_range_x[0], _hive_spawn_range_x[1])
            y_hive_coordinate = random.randint(_hive_spawn_range_y[0], _hive_spawn_range_y[1])
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
        flower_type = random.randint(1, _flower_type_number)
        flower_bed_seed = (random.randint(_flower_spawn_range_x[0], _flower_spawn_range_x[1]),
                           random.randint(_flower_spawn_range_y[0], _flower_spawn_range_y[1]))
        for j in range(_flowers_per_bed):
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
    current_tick = 0
    while True:
        screen.blit(_background.image, _background.rect)

        _hives.draw(screen)

        if current_tick == tick_cycle:
            current_tick = 0

        for flower in _flowers:
            flower.grow(current_tick)

        _flowers.draw(screen)

        for bee in _bees:
            bee.move()

        _bees.draw(screen)

        pygame.display.flip()
        pygame.time.delay(frame_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current_tick = current_tick + tick_gain
########################################################################################################################


if __name__ == "__main__":
    main()

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

_hives = []
_hiveNumber = 6
used_coordinates = []

_bees = []
_beesPerHive = 10
_flowers = []
_flowerNumber = 200


########################################################################################################################


def spawn_hives(number_of_hives, bees_per_hive):
    for i in range(number_of_hives):

        done = False
        while not done:
            x_hive_coordinate = random.randint(60, 940)
            y_hive_coordinate = random.randint(60, 940)
            done = True
            for n in used_coordinates:
                distance = abs(math.sqrt( pow(n[0] - x_hive_coordinate, 2) + pow(n[1] - y_hive_coordinate, 2)))
                if distance < 75:
                    done = False

            used_coordinates.append((x_hive_coordinate, y_hive_coordinate))

        new_hive = beeHiveData.BeeHive((x_hive_coordinate, y_hive_coordinate))

        _hives.append(new_hive)

        for j in range(bees_per_hive):
            new_bee = beeData.Bee((x_hive_coordinate+random.randint(-30, 30),
                                   y_hive_coordinate+random.randint(-30, 30)), new_hive)
            _bees.append(new_bee)
########################################################################################################################


def spawn_flowers(number_of_flowers):
    for i in range(number_of_flowers):
        new_flower = flowerData.Flower((random.randint(0, 1000), random.randint(0, 1000)), random.randint(1, 3))
        _flowers.append(new_flower)
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
    spawn_flowers(_flowerNumber)
########################################################################################################################
# Main Game Loop
    while True:
        screen.blit(_background.image, _background.rect)

        for beeHive in _hives:
            screen.blit(beeHive.image, beeHive.rect)
        for flower in _flowers:
            screen.blit(flower.image, flower.rect)
        for bee in _bees:
            bee.move()
            screen.blit(bee.image, bee.rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
########################################################################################################################


if __name__ == "__main__":
    main()

import pygame
import sys
import random
import math
from source import gameBoard
from source import beeHiveData
from source import beeData
########################################################################################################################
# Data Fields

screen_size = (1600, 900)
_background = gameBoard.Background((0, 0))  # This is just the background

_hives = pygame.sprite.RenderUpdates()
_hiveNumber = 1
used_coordinates = []
_hive_spawn_range_x = (200, 1400)
_hive_spawn_range_y = (200, 600)
acceptable_hive_distance = 75

_bees = pygame.sprite.RenderUpdates()
_beesPerHive = 10
_bee_spawn_offset = (-50, 50)


play_music = False
frame_delay = 14
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

        spawn_initial_bees(new_hive, bees_per_hive)


def spawn_initial_bees(hive, bees_per_hive):
    for j in range(bees_per_hive):
        new_bee = beeData.Bee((hive.rect.left + 33 + random.randint(_bee_spawn_offset[0], _bee_spawn_offset[1]),
                               hive.rect.top + 52 + random.randint(_bee_spawn_offset[0], _bee_spawn_offset[1])),
                              hive, 'scout')
        _bees.add(new_bee)

########################################################################################################################


def spawn_flowers(number_of_flowers):
    #TODO
    pass

########################################################################################################################


def main():
########################################################################################################################
# Init Screen

    screen = pygame.display.set_mode(screen_size)

########################################################################################################################
# Init Music
    if play_music:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/beeMusic.mp3")
        pygame.mixer.music.play(loops=-1, start=0.0)

########################################################################################################################
# Spawn Hives
    spawn_hives(_hiveNumber, _beesPerHive)
########################################################################################################################
# Spawn Flowers
    # TODO
########################################################################################################################
# Main Game Loop
    current_tick = 0
    while True:
        screen.blit(_background.image, _background.rect)

        _hives.draw(screen)

        if current_tick == tick_cycle:
            current_tick = 0

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

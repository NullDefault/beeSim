from random import *
import pygame


def generate_flower_spawn_points(number_of_field_partitions, growth_stages, hives, play_area_dimensions):
    # partition the playing field into halves until there is a region for every flower
    # if the number is odd, randomly pick right or left and partition that half an extra time
    # pick a central point within the region that will count as the "root" of the flower spawn
    # place the room pseudo-randomly, with increased chance for the middle area
    # grow the roots using Conway's rules
    # return all the x, y coordinates of the new flowers

    return area_partition(play_area_dimensions, number_of_field_partitions)


def area_partition(game_area, number_of_partitions):

    if number_of_partitions is 0:
        return ()

    cut_direction = flip_direction()
    rectangle = pygame.Rect(0, 0, game_area[0], game_area[1])
    rectangles = [rectangle]
    for i in range(number_of_partitions):
        rectangles = cut(rectangles, cut_direction)

    return rectangles


def flip_direction():
    if randint(0, 1) == 1:
        return 'horizontal'
    else:
        return 'vertical'


def cut(rectangles, cut_direction):
    if len(rectangles) == 1:  # Base Case

        old_rect = rectangles[0]

        if cut_direction == 'horizontal':
            top_half = \
                pygame.Rect(old_rect.left, old_rect.top, old_rect.width, old_rect.height / 2)
            bot_half = \
                pygame.Rect(old_rect.left, old_rect.top + old_rect.height / 2, old_rect.width, old_rect.height / 2)
            return top_half, bot_half
        else:
            left_half = \
                pygame.Rect(old_rect.left, old_rect.top, old_rect.width / 2, old_rect.height)
            right_half = \
                pygame.Rect(old_rect.left + old_rect.width / 2, old_rect.top, old_rect.width / 2, old_rect.height)
            return left_half, right_half

    else:  # Recursive Step
        mid_point = int(len(rectangles) / 2)
        left_cut = flip_direction()
        right_cut = flip_direction()

        return cut(rectangles[mid_point:], left_cut) + cut(rectangles[:mid_point], right_cut)

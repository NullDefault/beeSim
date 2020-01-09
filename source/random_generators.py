from random import *
import pygame

from source.flower_data import Flower


def generate_initial_flower_spawns(number_of_field_partitions, growth_stages, hives, play_area_dimensions):

    # TODO: Clean up this hacky mess and also make the flowers grow around hives

    root_locations = area_partition(play_area_dimensions, number_of_field_partitions)
    flower_database = {}

    for location_rect in root_locations:  # loads root flowers
        location = get_center_point(location_rect)
        new_f = Flower(location)
        flower_database[location] = new_f
    print(flower_database)
    flowers_to_add = {}

    for i in range(growth_stages):
        for flower in flower_database.values():
            # grow each flower, if no open spots are near a flower, grow an adjacent flower
            new_f = drop_seed(flower, flower_database.values())
            flowers_to_add[flower.rect.left, flower.rect.top] = new_f
        flower_database = {**flower_database, **flowers_to_add}

    clean_up_table = {}

    for f in flower_database.values():
        f_loc = f.rect.left, f.rect.top
        if not f_loc in clean_up_table:
            clean_up_table[f_loc] = f

    return clean_up_table


def drop_seed(flower, existing_flowers):
    drop_direction = find_valid_location(flower, existing_flowers)
    if not drop_direction[0]:
        return drop_seed(drop_direction[1], existing_flowers)

    return Flower(drop_direction[1])  # In the future this can be used to pass info between neighboring flowers


def find_valid_location(flower, existing_flowers):
    try_loc = roll_for_location(flower)

    for flower in existing_flowers:
        rect = flower.rect
        if rect.collidepoint(try_loc):
            return False, flower
    else:
        return True, try_loc


def roll_for_location(flower):
    r = randint(0, 7)

    left = flower.rect.x - flower.rect.width - 1
    right = flower.rect.x + flower.rect.width + 1
    up = flower.rect.y - flower.rect.height - 1
    down = flower.rect.y + flower.rect.height + 1

    same_x = flower.rect.left
    same_y = flower.rect.top

    if r == 0:  # UP LEFT
        dest_loc = left, up
    elif r == 1:  # UP
        dest_loc = same_x, up
    elif r == 2:  # UP RIGHT
        dest_loc = right, up
    elif r == 3:  # RIGHT
        dest_loc = right, same_y
    elif r == 4:  # LEFT
        dest_loc = left, same_y
    elif r == 5:  # DOWN LEFT
        dest_loc = left, down
    elif r == 6:  # DOWN
        dest_loc = same_x, down
    elif r == 7:  # DOWN RIGHT
        dest_loc = right, down

    return dest_loc


def get_center_point(rect):
    center_x = rect.x + rect.width / 2
    center_y = rect.y + rect.height / 2
    return center_x, center_y


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

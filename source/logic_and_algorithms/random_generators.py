"""
File Name: Random Generators
Class Purpose: Holds functions for procedurally generating a variety of game structures
Notes:
"""
#  IMPORTS
from statistics import NormalDist
from random import randint, uniform
from pygame import Rect
from source.entities.hive_data.bee_hive import BeeHive
from source.entities.flower_data.flower import Flower


# FUNCTIONS


def default_flower_spawning_strategy(number_of_field_partitions: int, growth_stages: int,  # Spawn initial flowers
                                     play_area_dimensions: int()):
    root_locations = area_partition(play_area_dimensions, number_of_field_partitions)  # partitions the field into
                                                                                       # halves n times
    flower_database = {}

    for location_rect in root_locations:  # loads root flowers
        location = get_center_point(location_rect)
        new_f = Flower(location)
        flower_database[location] = new_f
    flowers_to_add = {}

    for i in range(growth_stages):
        for flower in flower_database.values():
            # grow each flower, if no open spots are near a flower, grow an adjacent flower
            new_f = drop_seed(flower, flower_database.values())
            flowers_to_add[flower.rect.left, flower.rect.top] = new_f
        flower_database = {**flower_database, **flowers_to_add}

    # The code below cleans the generated flowers list of those with same coordinates
    clean_up_table = {}

    for f in flower_database.values():
        f_loc = f.rect.left, f.rect.top
        if f_loc not in clean_up_table:
            clean_up_table[f_loc] = f

    return clean_up_table


def drop_seed(flower, existing_flowers):  # Makes a flower spawn offspring adjacently
    drop_direction = find_valid_location(flower, existing_flowers)
    if not drop_direction[0]:
        return drop_seed(drop_direction[1], existing_flowers)

    return Flower(drop_direction[1])


def find_valid_location(flower, existing_flowers):  # Finds a valid location for the next flower
    try_loc = roll_for_location(flower)

    for flower in existing_flowers:
        rect = flower.rect
        if rect.collidepoint(try_loc):
            return False, flower
    else:
        return True, try_loc


def roll_for_location(flower):  # Rolls for one of a cells 8 neighbors
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
    else:  # DOWN RIGHT
        dest_loc = right, down

    return dest_loc


def get_center_point(rect):  # Returns the center of a rectangle
    center_x = rect.x + rect.width / 2
    center_y = rect.y + rect.height / 2
    return center_x, center_y


def area_partition(game_area, number_of_partitions):  # cuts a rectangle into halves n times
    if number_of_partitions == 0:
        return ()

    cut_direction = flip_direction()
    rectangle = Rect(0, 0, game_area[0], game_area[1])
    rectangles = [rectangle]
    for i in range(number_of_partitions):
        rectangles = cut(rectangles, cut_direction)

    return rectangles


def flip_direction():  # Utility method for partitioning
    if randint(0, 1) == 1:
        return 'horizontal'
    else:
        return 'vertical'


def cut(rectangles, cut_direction):  # Utility method for partitioning (Recursive!)
    if len(rectangles) == 1:  # Base Case

        old_rect = rectangles[0]

        if cut_direction == 'horizontal':
            top_half = \
                Rect(old_rect.left, old_rect.top, old_rect.width, old_rect.height / 2)
            bot_half = \
                Rect(old_rect.left, old_rect.top + old_rect.height / 2, old_rect.width, old_rect.height / 2)
            return top_half, bot_half
        else:
            left_half = \
                Rect(old_rect.left, old_rect.top, old_rect.width / 2, old_rect.height)
            right_half = \
                Rect(old_rect.left + old_rect.width / 2, old_rect.top, old_rect.width / 2, old_rect.height)
            return left_half, right_half

    else:  # Recursive Step
        mid_point = int(len(rectangles) / 2)
        left_cut = flip_direction()
        right_cut = flip_direction()

        return cut(rectangles[mid_point:], left_cut) + cut(rectangles[:mid_point], right_cut)


def find_valid_hive_spawns(hive_num, play_area, flowers):  # Finds valid locations for new hives
    new_hives = []
    for n in range(hive_num):
        new_hives.append(BeeHive(find_hive_loc(play_area, new_hives, flowers)))

    return new_hives


def find_hive_loc(play_area, existing_hives, flowers):  # Finds one hive location
    new_loc = randint(0, play_area[0] - 66), randint(0, play_area[1] - 66)

    for hive in existing_hives:
        if hive.rect.collidepoint(new_loc):
            return find_hive_loc(play_area, existing_hives, flowers)
    for flower in flowers:
        if flower.rect.collidepoint(new_loc):
            return find_hive_loc(play_area, existing_hives, flowers)
    else:
        return new_loc

# maps values from one range to another


def map_values(value, left_min, left_max, right_min, right_max):
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)


def normal_distr_flower_spawning_strategy(play_area):
    flower_num = 400  # This could be a parameter
    normal_distr = NormalDist(0.5, 0.15)
    flower_database = {}

    x_rolls = normal_distr.samples(flower_num)
    y_rolls = normal_distr.samples(flower_num)

    for i in range(flower_num):
        x_pos = map_values(x_rolls[i], 0, 1, 0, play_area[0])
        y_pos = map_values(y_rolls[i], 0, 1, 0, play_area[1])

        new_f = Flower((x_pos, y_pos))
        flower_database[(x_pos, y_pos)] = new_f

    clean_up_table = {}

    for f in flower_database.values():
        f_loc = f.rect.left, f.rect.top
        if f_loc not in clean_up_table:
            clean_up_table[f_loc] = f

    return clean_up_table

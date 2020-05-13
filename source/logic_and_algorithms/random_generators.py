"""
File Name: Random Generators
Class Purpose: Holds functions for procedurally generating a variety of game structures
Notes:
"""
from random import randint
from statistics import NormalDist

from pygame import Rect, Vector2

from source.entities.decorative_entity import Decoration
from source.entities.flower_data.flower import Flower
from source.entities.hive_data.bee_hive import BeeHive


# FUNCTIONS

def find_valid_hive_spawns(hive_num, play_area, flowers):
    """
    :param hive_num:
    :param play_area:
    :param flowers:
    :return: list of hives in valid locations
    """
    new_hives = []
    c_index = 0
    colors = ['blue', 'green', 'purple', 'red', 'yellow']

    for n in range(hive_num):

        if c_index != colors.__len__() - 1:
            c_index += 1
        else:
            c_index = 0

        new_hives.append(BeeHive(find_hive_loc(play_area, new_hives, flowers), colors[c_index]))

    return new_hives


def get_location_in_circle(distance_roll, play_area):
    distance = map_values(distance_roll, 0, 1, 0, play_area - 100)
    angle = randint(0, 360)

    center = play_area // 2, play_area // 2

    movement_vector = Vector2(center)
    movement_vector.rotate_ip(angle)
    movement_vector.scale_to_length(distance)

    location = Vector2(center) + movement_vector

    return location.x, location.y


def find_hive_loc(play_area, existing_hives, flowers):
    """
    :param play_area:
    :param existing_hives:
    :param flowers:
    :return: valid location for a hive
    """
    dist = 0.3
    new_loc = get_location_in_circle(dist, play_area)

    for hive in existing_hives:
        new_rect = Rect(new_loc[0], new_loc[1], 66, 66)
        if hive.rect.colliderect(new_rect):
            return find_hive_loc(play_area, existing_hives, flowers)
    else:
        return new_loc


def map_values(value, left_min, left_max, right_min, right_max):
    """
    :param value:
    :param left_min:
    :param left_max:
    :param right_min:
    :param right_max:
    :return: Maps the value from the left range onto the right range
    """
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = (value - left_min) / left_span

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)


def normal_distribution_flower_spawning_strategy(play_area, flower_num):
    """
    Returns a normal-distribution generated list of flowers
    :param play_area:
    :return: list of spawned flowers
    """
    normal_distribution = NormalDist(0.5, 0.15)
    flower_database = {}

    dist_rolls = normal_distribution.samples(flower_num)

    for i in range(flower_num):
        location = get_location_in_circle(dist_rolls[i], play_area)
        new_f = Flower(location)
        flower_database[location] = new_f

    clean_up_table = {}

    for f in flower_database.values():
        f_loc = f.rect.left, f.rect.top
        if f_loc not in clean_up_table:
            clean_up_table[f_loc] = f

    return clean_up_table


def inverse_probabilities(o_list):
    """
    :param o_list:
    :return: transforms the values from a normal distribution on range (0, 1) into its equivalents on an upside down one
    """
    transformed = []
    for value in o_list:
        if value < 0.5:
            transformed.append(0.5 - value)
        else:
            transformed.append(1.5 - value)
    return transformed


def grow_plants(play_area, num, plant_type, bias):
    """
    :param play_area:
    :param num:
    :param plant_type:
    :param bias:
    :return: a list of spawned plants of given type
    """
    normal_distribution = NormalDist(0.5, 0.15)

    plant_db = {}

    dist_rolls = normal_distribution.samples(num)

    if bias == 'edges':
        dist_rolls = inverse_probabilities(dist_rolls)

    for i in range(num):
        location = get_location_in_circle(dist_rolls[i], play_area)
        new_p = Decoration(location, plant_type)
        plant_db[location] = new_p

    clean_up_db = {}

    for p in plant_db.values():
        p_loc = p.rect.left, p.rect.top
        if p_loc not in clean_up_db:
            clean_up_db[p_loc] = p

    return clean_up_db

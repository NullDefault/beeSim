"""
File Name: Random Generators
Class Purpose: Holds functions for procedurally generating a variety of game structures
Notes:
"""
#  IMPORTS
from pygame import Rect
from statistics import NormalDist

from source.entities.hive_data.bee_hive import BeeHive
from source.entities.flower_data.flower import Flower
from source.entities.decorative_entity import Decoration


# FUNCTIONS

def find_valid_hive_spawns(hive_num, play_area, flowers):
    """
    :param hive_num:
    :param play_area:
    :param flowers:
    :return: list of hives in valid locations
    """
    new_hives = []
    for n in range(hive_num):
        new_hives.append(BeeHive(find_hive_loc(play_area, new_hives, flowers)))

    return new_hives


def find_hive_loc(play_area, existing_hives, flowers):
    """
    :param play_area:
    :param existing_hives:
    :param flowers:
    :return: valid location for a hive
    """
    normal_distribution = NormalDist(0.5, 0.15)

    new_loc = normal_distribution.samples(2)
    # 20 below is not a magic number, rather we just constrain the range a bit so we don't have things going off screen
    new_loc = map_values(new_loc[0], 0, 1, 20, play_area[0]-20), map_values(new_loc[1], 0, 1, 20, play_area[1]-20)

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


def normal_distribution_flower_spawning_strategy(play_area):
    """
    Returns a normal-distribution generated list of flowers
    :param play_area:
    :return: list of spawned flowers
    """
    flower_num = 200  # This could be a parameter
    normal_distribution = NormalDist(0.5, 0.15)
    flower_database = {}

    x_rolls = normal_distribution.samples(flower_num)
    y_rolls = normal_distribution.samples(flower_num)

    for i in range(flower_num):
        # 20 below is not a magic number,
        # rather we just constrain the range a bit so we don't have things going off screen
        x_pos = map_values(x_rolls[i], 0, 1, 20, play_area[0] - 20)
        y_pos = map_values(y_rolls[i], 0, 1, 20, play_area[1] - 20)

        new_f = Flower((x_pos, y_pos))
        flower_database[(x_pos, y_pos)] = new_f

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

    x_rolls = normal_distribution.samples(num)
    y_rolls = normal_distribution.samples(num)

    if bias == 'edges':
        x_rolls = inverse_probabilities(x_rolls)
        y_rolls = inverse_probabilities(y_rolls)

    for i in range(num):

        # 20 below is not a magic number,
        # rather we just constrain the range a bit so we don't have things going off screen
        x_pos = map_values(x_rolls[i], 0, 1, 20, play_area[0] - 20)
        y_pos = map_values(y_rolls[i], 0, 1, 20, play_area[1] - 20)

        new_p = Decoration((x_pos, y_pos), plant_type)
        plant_db[(x_pos, y_pos)] = new_p

    clean_up_db = {}

    for p in plant_db.values():
        p_loc = p.rect.left, p.rect.top
        if p_loc not in clean_up_db:
            clean_up_db[p_loc] = p

    return clean_up_db

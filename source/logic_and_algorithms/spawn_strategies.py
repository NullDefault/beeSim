"""
File Name: Spawn Strategies
Class Purpose: Dictionary for controlling which algorithm to use when spawning new entities
Notes:
"""

#  IMPORTS


from source.logic_and_algorithms.random_generators import find_valid_hive_spawns, \
    normal_distribution_flower_spawning_strategy


def get_flower_spawn_strategy(ss, play_area):
    if ss == 'normal_distribution':
        return normal_distribution_flower_spawning_strategy(
            play_area
        )


def get_hive_spawn_strategy(ss, hive_number, play_area, flowers):
    if ss == 'default':
        return find_valid_hive_spawns(
            hive_number,
            play_area,
            flowers
        )

"""
File Name: Spawn Strategies
Class Purpose: Dictionary for controlling which algorithm to use when spawning new entities
Notes:
"""

#  IMPORTS


from source.logic_and_algorithms.random_generators import default_flower_spawning_strategy, find_valid_hive_spawns


def get_flower_spawn_strategy(ss, spawn_vars, play_area):
    if ss == 'default':
        return default_flower_spawning_strategy(
            spawn_vars['flower_zones'],
            spawn_vars['initial_growth_stages'],
            play_area
        )


def get_hive_spawn_strategy(ss, hive_number, play_area, flowers):
    if ss == 'default':
        return find_valid_hive_spawns(
            hive_number,
            play_area,
            flowers
        )

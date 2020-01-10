from source.random_generators import generate_initial_flower_spawns, find_valid_hive_spawns


def get_flower_spawn_strategy(ss, spawn_vars, play_area):
    if ss == 'default':
        return generate_initial_flower_spawns(
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

import pickle
from os.path import join

from screeninfo import get_monitors

save_file_location = join("source", "assets", "save_data", "settings_save_data.pickle")


def load_settings_file():
    try:
        with open(save_file_location, 'rb') as f:
            settings = pickle.load(f)
            return settings
    except FileNotFoundError:
        print("No settings file found, initializing and saving new settings file")
        return Settings()


def get_resolution_below(monitor):
    return int(monitor.width * 0.8), int(monitor.height * 0.8)


default_data = {
    'map_size': 1000,
    'resolution': get_resolution_below(get_monitors()[0]),
    'initial_hives': 5,
    'initial_bees': 6,
    'flower_strat': 'normal distribution',
    'hive_strat': 'default',
    'flower_num': 600,
    'music': False
}


class Settings:

    def __init__(self, data=default_data):
        self.map_size = data['map_size']
        self.frame_resolution = data['resolution']
        self.frame_rate = 90
        self.initial_hives = data['initial_hives']
        self.initial_bees_per_hive = data['initial_bees']
        self.flower_spawn_strategy = data['flower_strat']
        self.hive_spawn_strategy = data['hive_strat']
        self.flower_num = data['flower_num']
        self.play_music = data['music']
        # Saves the file

        with open(save_file_location, 'wb') as f:
            pickle.dump(self, f)

"""
File Name: Sprite Bank
Class Purpose: Holds data on all the sprites for the sake of convenience and organization
Notes:
"""

from os.path import join

from pygame import image, display

screen = display.set_mode((1600, 900))


def load(path):
    return image.load(path).convert_alpha()


sprite_bank = {
    #  BEES
    'bee_hidden_sprite': load(
        join('source', 'assets', 'sprites', 'bee_sprites', 'bee_sprite_hidden.png')),

    # FLOWERS
    'flower_0': load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_0.png')),
    'flower_1': load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_1.png')),
    'flower_2': load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_2.png')),
    'flower_3': load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_3.png')),
    'flower_4': load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_4.png')),

    # DECORATIONS
    'grass1': load(join('source', 'assets', 'sprites', 'plant_sprites',
                        'decorative_plants', 'grass1.png')),
    'grass2': load(join('source', 'assets', 'sprites', 'plant_sprites',
                        'decorative_plants', 'grass2.png')),
    'grass3': load(join('source', 'assets', 'sprites', 'plant_sprites',
                        'decorative_plants', 'grass3.png')),
    'grassy_plant': load(join('source', 'assets', 'sprites', 'plant_sprites',
                              'decorative_plants', 'grassy_plant.png')),
    'bushy_grass': load(join('source', 'assets', 'sprites', 'plant_sprites',
                             'decorative_plants', 'bushy_grass.png')),
    'leaves': load(join('source', 'assets', 'sprites', 'plant_sprites',
                        'decorative_plants', 'leaves.png')),
    'pretty_log': load(join('source', 'assets', 'sprites', 'plant_sprites',
                            'decorative_plants', 'pretty_log.png')),
    'stump': load(join('source', 'assets', 'sprites', 'plant_sprites',
                       'decorative_plants', 'stump.png')),

    # HIVES
    'hive': load(join('source', 'assets', 'sprites', 'hive_sprites', 'hive.png')),

    # HIVE HATS
    'red_hat': load(join('source', 'assets', 'sprites', 'hive_sprites', 'red_hat.png')),
    'blue_hat': load(join('source', 'assets', 'sprites', 'hive_sprites', 'blue_hat.png')),
    'green_hat': load(join('source', 'assets', 'sprites', 'hive_sprites', 'green_hat.png')),
    'purple_hat': load(join('source', 'assets', 'sprites', 'hive_sprites', 'purple_hat.png')),
    'yellow_hat': load(join('source', 'assets', 'sprites', 'hive_sprites', 'yellow_hat.png')),

    # UI
    'game_icon': load(join('source', 'assets', 'ui_elements', 'game_icon.png')),
    'crosshair_bee': load(join('source', 'assets', 'ui_elements', 'crosshair_bee.png')),
    'crosshair_flower': load(join('source', 'assets', 'ui_elements', 'crosshair_flower.png')),
    'honey_bar': load(join('source', 'assets', 'ui_elements', 'honey_bar.png')),
    'main_menu_graphics': load(join('source', 'assets', 'menu_graphics.png')),
}


def retrieve(sprite: str):
    """
    :param sprite:
    :return: Returns the image for the requested sprite
    """
    return sprite_bank[sprite]

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


bee_path = 'source/assets/sprites/bee_sprites'
flower_path = 'source/assets/sprites/plant_sprites/flowers'
decoration_path = 'source/assets/sprites/plant_sprites/decorative_plants'
hive_path = 'source/assets/sprites/hive_sprites'
ui_path = 'source/assets/ui_elements'

sprite_bank = {
    #  BEES
    'bee_hidden_sprite': load(join(bee_path, 'bee_sprite_hidden.png')),

    # FLOWERS
    'flower_0': load(join(flower_path, 'flower_0.png')),
    'flower_1': load(join(flower_path, 'flower_1.png')),
    'flower_2': load(join(flower_path, 'flower_2.png')),
    'flower_3': load(join(flower_path, 'flower_3.png')),
    'flower_4': load(join(flower_path, 'flower_4.png')),

    # DECORATIONS
    'grass': load(join(decoration_path, 'grass_patch.png')),
    'grassy_plant': load(join(decoration_path, 'grassy_plant.png')),
    'bushy_grass': load(join(decoration_path, 'bushy_grass.png')),
    'leaves': load(join(decoration_path, 'leaves.png')),
    'pretty_log': load(join(decoration_path, 'pretty_log.png')),
    'stump': load(join(decoration_path, 'stump.png')),

    # HIVES
    'hive': load(join(hive_path, 'hive.png')),

    # HIVE HATS
    'red_hat': load(join(hive_path, 'red_hat.png')),
    'blue_hat': load(join(hive_path, 'blue_hat.png')),
    'green_hat': load(join(hive_path, 'green_hat.png')),
    'purple_hat': load(join(hive_path, 'purple_hat.png')),
    'yellow_hat': load(join(hive_path, 'yellow_hat.png')),

    # UI
    'game_icon': load(join(ui_path, 'game_icon.png')),
    'crosshair_bee': load(join(ui_path, 'crosshair_bee.png')),
    'crosshair_flower': load(join(ui_path, 'crosshair_flower.png')),
    'honey_bar': load(join(ui_path, 'honey_bar.png')),
    'main_menu_graphics': load(join(ui_path, 'menu_graphics.png')),
}


def retrieve(sprite: str):
    """
    :param sprite:
    :return: Returns the image for the requested sprite
    """
    return sprite_bank[sprite]

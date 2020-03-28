"""
File Name: Sprite Bank
Class Purpose: Holds data on all the sprites for the sake of convenience and organization
Notes:
"""

from os.path import join

from pygame import image

sprite_bank = {
    #  BEES
    'bee_wings_down': image.load(
        join('source', 'assets', 'sprites', 'bee_sprites', 'bee_sprite.png')),
    'bee_wings_up': image.load(
        join('source', 'assets', 'sprites', 'bee_sprites', 'bee_sprite2.png')),
    'bee_hidden_sprite': image.load(
        join('source', 'assets', 'sprites', 'bee_sprites', 'bee_sprite_hidden.png')),

    # FLOWERS
    'flower_0': image.load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_0.png')),
    'flower_1': image.load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_1.png')),
    'flower_2': image.load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_2.png')),
    'flower_3': image.load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_3.png')),
    'flower_4': image.load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower_4.png')),

    # DECORATIONS
    'grass_patch': image.load(join('source', 'assets', 'sprites', 'plant_sprites',
                                   'decorative_plants', 'grass_patch.png')),
    'grassy_plant': image.load(join('source', 'assets', 'sprites', 'plant_sprites',
                                    'decorative_plants', 'grassy_plant.png')),
    'bushy_grass': image.load(join('source', 'assets', 'sprites', 'plant_sprites',
                                    'decorative_plants', 'bushy_grass.png')),
    'leaves': image.load(join('source', 'assets', 'sprites', 'plant_sprites',
                                    'decorative_plants', 'leaves.png')),
    'pretty_log': image.load(join('source', 'assets', 'sprites', 'plant_sprites',
                                    'decorative_plants', 'pretty_log.png')),
    'stump': image.load(join('source', 'assets', 'sprites', 'plant_sprites',
                                    'decorative_plants', 'stump.png')),

    # HIVES
    'hive': image.load(join('source', 'assets', 'sprites', 'hive_sprites', 'bee_hive_yellow.png')),

    # UI
    'inspection_button': image.load(join('source', 'assets', 'ui_elements', 'inspection_button.png')),
    'game_icon': image.load(join('source', 'assets', 'ui_elements', 'game_icon.png')),

    'crosshair_bee': image.load(join('source', 'assets', 'ui_elements', 'crosshair_bee.png')),
    'crosshair_flower': image.load(join('source', 'assets', 'ui_elements', 'crosshair_flower.png')),

    'honey_bar': image.load(join('source', 'assets', 'ui_elements', 'honey_bar.png')),
    'honeycombs': image.load(join('source', 'assets', 'ui_elements', 'honeycombs.png')),
    'worker_counter': image.load(join('source', 'assets', 'ui_elements', 'worker_count.png')),
    'scout_counter': image.load(join('source', 'assets', 'ui_elements', 'scout_count.png')),
}


def retrieve(sprite: str):
    """
    :param sprite:
    :return: Returns the image for the requested sprite
    """
    return sprite_bank[sprite]

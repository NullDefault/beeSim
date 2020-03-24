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
    'flower': image.load(join('source', 'assets', 'sprites', 'plant_sprites', 'flowers', 'flower.png')),

    # PLANTS
    'grass_patch': image.load(join('source', 'assets', 'sprites', 'plant_sprites', 'grass_patch.png')),
    'grassy_plant': image.load(join('source', 'assets', 'sprites', 'plant_sprites', 'grassy_plant.png')),

    # HIVES
    'hive': image.load(join('source', 'assets', 'sprites', 'hive_sprites', 'bee_hive_yellow.png')),

    # UI
    'menu_image': image.load(join('source', 'assets', 'ui_elements', 'menu_background.png')),
    'inspection_menu': image.load(join('source', 'assets', 'ui_elements', 'inspection_menu.png')),
    'inspection_button': image.load(join('source', 'assets', 'ui_elements', 'inspection_button.png')),
    'game_icon': image.load(join('source', 'assets', 'ui_elements', 'game_icon.png')),
    'crosshair': image.load(join('source', 'assets', 'ui_elements', 'crosshair.png')),
    'honey_bar': image.load(join('source', 'assets', 'ui_elements', 'honey_bar.png')),
    'worker_counter': image.load(join('source', 'assets', 'ui_elements', 'worker_count.png')),
    'scout_counter': image.load(join('source', 'assets', 'ui_elements', 'scout_count.png')),
}


def retrieve(sprite: str):
    return sprite_bank[sprite]

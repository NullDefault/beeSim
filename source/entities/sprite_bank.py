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
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite.png')),
    'bee_wings_up': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite2.png')),
    'bee_hidden_sprite': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_hidden.png')),
    'bee_harvest_sprite': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_harvest.png')),

    # FLOWERS
    'flower_0': image.load(join('assets', 'sprites', 'flower_sprites', 'flower_0.png')),
    'flower_1': image.load(join('assets', 'sprites', 'flower_sprites', 'flower_1.png')),
    'flower_2': image.load(join('assets', 'sprites', 'flower_sprites', 'flower_2.png')),
    'flower_3': image.load(join('assets', 'sprites', 'flower_sprites', 'flower_3.png')),
    'flower_4': image.load(join('assets', 'sprites', 'flower_sprites', 'flower_4.png')),
    'flower_5': image.load(join('assets', 'sprites', 'flower_sprites', 'flower_5.png')),

    # HIVES
    'hive': image.load(join('assets', 'sprites', 'hive_sprites', 'bee_hive_yellow.png')),

    # UI
    'menu_image': image.load(join('assets', 'ui_elements', 'menu_background.png')),
    'inspection_menu': image.load(join('assets', 'ui_elements', 'inspection_menu.png')),
    'inspection_button': image.load(join('assets', 'ui_elements', 'inspection_button.png')),
    'game_icon': image.load(join('assets', 'ui_elements', 'game_icon.png')),
    'crosshair': image.load(join('assets', 'ui_elements', 'crosshair.png')),
    'honey_bar': image.load(join('assets', 'ui_elements', 'honey_bar.png')),
    'worker_counter': image.load(join('assets', 'ui_elements', 'worker_count.png')),
    'scout_counter': image.load(join('assets', 'ui_elements', 'scout_count.png')),
}


def retrieve(sprite: str):
    return sprite_bank[sprite]

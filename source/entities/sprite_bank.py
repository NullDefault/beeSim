"""
File Name: Sprite Bank
Class Purpose: Holds data on all the sprites for the sake of convenience and organization
Notes:
"""

from pygame import image
from os.path import join

sprite_bank = {
    #  BEES
    'bee': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_down.png')),
    'bee_left_sprite': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_left.png')),
    'bee_right_sprite': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_right.png')),
    'bee_up_sprite': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_up.png')),
    'bee_down_sprite': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_down.png')),

    'bee_left_sprite_highlighted': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_left_highlighted.png')),
    'bee_right_sprite_highlighted': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_right_highlighted.png')),
    'bee_up_sprite_highlighted': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_up_highlighted.png')),
    'bee_down_sprite_highlighted': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_down_highlighted.png')),

    'bee_hidden_sprite': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_hidden.png')),
    'bee_hidden_sprite_highlighted': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_hidden_highlighted.png')),

    'bee_harvest_sprite': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_harvest.png')),
    'bee_harvest_sprite_highlighted': image.load(
        join('assets', 'sprites', 'bee_sprites', 'bee_sprite_harvest_highlighted.png')),

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

    # MAP ELEMENTS
    'grass_background': image.load(join('assets', 'map_elements', 'grass_background.png')),
}


def retrieve(sprite: str):
    return sprite_bank[sprite]

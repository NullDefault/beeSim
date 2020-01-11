"""
File Name: Sprite Bank
Class Purpose: Holds data on all the sprites for the sake of convenience and organization
Notes:
"""

from pygame import image

sprite_bank = {
    #  BEES
    'bee': image.load("assets/sprites/bee_sprites/bee_sprite_down.png"),
    'bee_left_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_left.png"),
    'bee_right_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_right.png"),
    'bee_up_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_up.png"),
    'bee_down_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_down.png"),
    'bee_left_selected_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_left_selected.png"),
    'bee_right_selected_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_right_selected.png"),
    'bee_up_selected_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_up_selected.png"),
    'bee_down_selected_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_down_selected.png"),

    # FLOWERS
    'flower_0': image.load("assets/sprites/flower_sprites/flower_0.png"),
    'flower_1': image.load("assets/sprites/flower_sprites/flower_1.png"),
    'flower_2': image.load("assets/sprites/flower_sprites/flower_2.png"),
    'flower_3': image.load("assets/sprites/flower_sprites/flower_3.png"),
    'flower_4': image.load("assets/sprites/flower_sprites/flower_4.png"),
    'flower_5': image.load("assets/sprites/flower_sprites/flower_5.png"),

    # HIVES
    'hive': image.load("assets/sprites/hive_sprites/bee_hive_yellow.png")

}


def retrieve(sprite: str):
    return sprite_bank[sprite]

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

    'bee_left_sprite_highlighted': image.load("assets/sprites/bee_sprites/bee_sprite_left_selected.png"),
    'bee_right_sprite_highlighted': image.load("assets/sprites/bee_sprites/bee_sprite_right_selected.png"),
    'bee_up_sprite_highlighted': image.load("assets/sprites/bee_sprites/bee_sprite_up_selected.png"),
    'bee_down_sprite_highlighted': image.load("assets/sprites/bee_sprites/bee_sprite_down_selected.png"),

    'bee_hidden_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_hidden.png"),
    'bee_hidden_sprite_highlighted': image.load("assets/sprites/bee_sprites/bee_sprite_hidden_selected.png"),

    'bee_harvest_sprite': image.load("assets/sprites/bee_sprites/bee_sprite_harvest.png"),
    'bee_harvest_sprite_highlighted': image.load("assets/sprites/bee_sprites/bee_sprite_harvest_selected.png"),

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

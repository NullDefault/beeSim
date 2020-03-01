"""
Class Name: Main
Class Purpose: Entry point for the code, starts the engine up, all that jazz
Notes:
"""

#  IMPORTS
from pygame import time, display, Surface, mixer, transform, event

from source.UI.menus import menu_render
from source.entities import sprite_bank
from source.logic_and_algorithms.camera import Camera
from source.logic_and_algorithms.masters.entity_master import EntityMaster
from source.logic_and_algorithms.masters.event_master import EventMaster

# DATA FIELDS

screen_resolution = (1600, 900)
menu_location = (1200, 0)
camera = Camera()
play_area = (1600, 900)

entity_master = EntityMaster(initial_hives=2,                 # This variable decides what entities get spawned,
                             default_bees_per_hive=6,         # how many and on how big of a field. When i implement
                             number_of_flower_zones=3,        # saving and loading, this will be what loads and saves
                             initial_growth_stages=12,         # game states and data.
                             play_area_dimensions=play_area,
                             flower_spawn_strategy='default',
                             hive_spawn_strategy='default')

event_master = EventMaster(camera)

play_music = False

game_icon = sprite_bank.retrieve('game_icon')

game_clock = time.Clock()
game_frame_rate = 24


def main():
########################################################################################################################
# Init Screen
    screen = display.set_mode(screen_resolution)
    abstract_game_screen = Surface(play_area)
    display.set_icon(game_icon)
    display.set_caption("beeSim")
# Init Music
    if play_music:
        mixer.init()
        mixer.music.load("assets/sounds/bee_music.mp3")
        mixer.music.play(loops=-1, start=0.0)
# Init Game Vars
    menu_active = False
    inspection_target = None
########################################################################################################################
# Main Game Loop
    while True:

        game_clock.tick(game_frame_rate)

        entities_to_be_rendered = entity_master.get_valid_entities()

        camera_cropped_render = Surface(camera.size)
        camera_cropped_render.blit(abstract_game_screen, (0, 0),
                                   (camera.location[0], camera.location[1], camera.size[0], camera.size[1]))

        transform.scale(camera_cropped_render, screen_resolution, screen)
        updated_screen_rects = entities_to_be_rendered.draw(abstract_game_screen)

        if menu_active:
            screen.blit(menu_render(entity_master, game_clock, inspection_target), menu_location)

        display.update(updated_screen_rects)

        for e in event.get():
            inspection_target, menu_active = \
                event_master.handle_event(e, menu_active, entity_master, inspection_target)
########################################################################################################################


if __name__ == "__main__":
    main()

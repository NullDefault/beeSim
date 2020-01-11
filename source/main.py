"""
Class Name: Main
Class Purpose: Entry point for the code, starts the engine up, all that jazz
Notes:
"""

#  IMPORTS
from pygame import image, time, display, Surface, mixer, transform, event
from source.logic_and_algorithms.masters.entity_master import EntityMaster
from source.UI.menus import menu_render
from source.logic_and_algorithms.masters.event_master import EventMaster


# DATA FIELDS

screen_resolution = (1600, 900)
menu_location = (1200, 0)

play_area = (1600, 900)

background = image.load("assets/map_elements/grass_background.png")


entity_master = EntityMaster(initial_hives=1,                 # This variable decides what entities get spawned,
                             default_bees_per_hive=8,         # how many and on how big of a field. When i implement
                             number_of_flower_zones=4,        # saving and loading, this will be what loads and saves
                             initial_growth_stages=6,         # game states and data.
                             play_area_dimensions=play_area,
                             flower_spawn_strategy='default',
                             hive_spawn_strategy='default')

event_master = EventMaster()

play_music = False

game_icon = image.load("assets/ui_elements/game_icon.png")

game_clock = time.Clock()
game_frame_rate = 24


def main():
########################################################################################################################
# Init Screen
    screen = display.set_mode(screen_resolution)
    abstract_game_screen = Surface(play_area)
    camera_location = [0, 0]  # Controls which part of the screen is being rendered
    camera_size = (1600, 900)
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

        abstract_game_screen.blit(background, (0, 0))
        entities_to_be_rendered.draw(abstract_game_screen)  # TODO: only draw the visible ones

        camera_cropped_render = Surface(camera_size)
        camera_cropped_render.blit(abstract_game_screen, (0, 0),
                                   (camera_location[0], camera_location[1], camera_size[0], camera_size[1]))

        transform.scale(camera_cropped_render, screen_resolution, screen)

        if menu_active:
            screen.blit(menu_render(entity_master, game_clock, inspection_target), menu_location)

        display.flip()

        for e in event.get():
            inspection_target, menu_active, camera_location = \
                event_master.handle_event(e, menu_active, entity_master, inspection_target, camera_location)
########################################################################################################################


if __name__ == "__main__":
    main()

"""
Class Name: Main
Class Purpose: Entry point for the code, starts the engine up, all that jazz
Notes:
"""

#  IMPORTS
from pygame import time, display, mixer, event, QUIT

from source.UI.gui_master import GuiMaster
from source.entities import sprite_bank
from source.logic_and_algorithms.masters.entity_master import EntityMaster

# DATA FIELDS


screen_resolution = (1600, 900)
menu_location = (1200, 0)
play_area = screen_resolution
play_music = False
game_icon = sprite_bank.retrieve('game_icon')
game_clock = time.Clock()
game_frame_rate = 60


def main():

    # Init Screen
    screen = display.set_mode(screen_resolution)
    display.set_icon(game_icon)
    display.set_caption("beeSim")
    entity_master = EntityMaster(initial_hives=2,
                                 default_bees_per_hive=15,
                                 number_of_flower_zones=4,
                                 initial_growth_stages=15,
                                 play_area_dimensions=play_area,
                                 flower_spawn_strategy='normal_distribution',
                                 hive_spawn_strategy='default')
    gui_master = GuiMaster(screen_resolution, entity_master, game_clock)
    # Init Music
    if play_music:
        mixer.init()
        mixer.music.load("assets/sounds/bee_music.mp3")
        mixer.music.play(loops=-1, start=0.0)

    # Main Game Loop
    while True:
        time_delta = game_clock.tick(game_frame_rate) / 1000.0
        gui_master.update(time_delta)

        screen.fill((102, 200, 102))
        entity_master.get_valid_entities().draw(screen)
        gui_master.draw_ui(screen)
        display.update()

        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            gui_master.process_events(e)


if __name__ == "__main__":
    main()

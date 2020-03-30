"""
Class Name: Main
Class Purpose: Entry point for the code, starts the engine up, all that jazz
Notes:
"""

#  IMPORTS
from pygame import time, display, mixer, event, QUIT

from source.UI.camera import Camera
from source.UI.gui_master import GuiMaster
from source.entities import sprite_bank
from source.logic_and_algorithms.masters.entity_master import EntityMaster

# DATA FIELDS
map_size = (2200, 1100)

frame_resolution = (1600, 900)
menu_location = (1200, 0)

play_music = False
game_icon = sprite_bank.retrieve('game_icon')
game_clock = time.Clock()
game_frame_rate = 90


def main():

    # Init Screen
    screen = display.set_mode(frame_resolution)
    camera = Camera(frame_resolution, map_size)
    display.set_icon(game_icon)
    display.set_caption("beeSim")
    entity_master = EntityMaster(initial_hives=1,
                                 default_bees_per_hive=10,
                                 play_area_dimensions=map_size,
                                 flower_spawn_strategy='normal_distribution',
                                 hive_spawn_strategy='default')
    gui_master = GuiMaster(frame_resolution, entity_master, game_clock)
    # Init Music
    if play_music:
        mixer.init()
        mixer.music.load("source/assets/sounds/bee_music.mp3")
        mixer.music.play(loops=-1, start=0.0)

    # Main Game Loop
    while True:
        time_delta = game_clock.tick(game_frame_rate) / 1000.0
        gui_master.update(time_delta)

        frame_render = camera.render(entity_master.get_valid_entities())
        screen.blit(frame_render, (0, 0))
        gui_master.draw_ui(screen)
        display.update()

        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            gui_master.process_events(e, camera)


if __name__ == "__main__":
    main()

"""
Class Name: Game Loop
Class Purpose: Entry point for the code, starts the engine up, all that jazz
Notes:
"""

from os.path import join

#  IMPORTS
from pygame import display, mixer, event, QUIT

from source.UI.camera import Camera
from source.UI.gui_master import GuiMaster
from source.logic_and_algorithms.masters.entity_master import EntityMaster

# DATA FIELDS
menu_location = (1200, 0)


def simulation_loop(main_surface, game_clock, settings):
    frame_resolution = settings.frame_resolution
    game_frame_rate = settings.frame_rate
    camera = Camera(frame_resolution, settings.map_size)
    entity_master = EntityMaster(initial_hives=settings.initial_hives,
                                 default_bees_per_hive=settings.initial_bees_per_hive,
                                 play_area_dimensions=settings.map_size,
                                 flower_spawn_strategy=settings.flower_spawn_strat,
                                 hive_spawn_strategy=settings.hive_spawn_strat,
                                 flower_num=settings.flower_num)
    gui_master = GuiMaster(frame_resolution, entity_master, game_clock)
    # Init Music
    if settings.play_music:
        mixer.init()
        mixer.music.load(join('source', 'assets', 'sounds', 'bee_music.mp3'))
        mixer.music.play(loops=-1, start=0.0)

    # Main Game Loop
    while True:
        time_delta = game_clock.tick(game_frame_rate) / 1000.0
        gui_master.update(time_delta)
        camera.render(entity_master.get_entities(), main_surface)
        gui_master.draw_ui(main_surface)
        display.flip()

        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            output = gui_master.process_events(e, camera)

            if output == 0:
                mixer.quit()
                return output

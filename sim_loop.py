"""
Class Name: Game Loop
Class Purpose: Entry point for the code, starts the engine up, all that jazz
Notes:
"""

#  IMPORTS
from pygame import display, mixer, event, QUIT
from os.path import join
from source.UI.camera import Camera
from source.UI.gui_master import GuiMaster
from source.logic_and_algorithms.masters.entity_master import EntityMaster

# DATA FIELDS
map_size = 2000
menu_location = (1200, 0)
play_music = False


def simulation_loop(screen, frame_resolution, game_clock, game_frame_rate):
    camera = Camera(frame_resolution, map_size)
    entity_master = EntityMaster(initial_hives=5,
                                 default_bees_per_hive=6,
                                 play_area_dimensions=map_size,
                                 flower_spawn_strategy='normal_distribution',
                                 hive_spawn_strategy='default')
    gui_master = GuiMaster(frame_resolution, entity_master, game_clock)
    # Init Music
    if play_music:
        mixer.init()
        mixer.music.load(join('source', 'assets', 'sounds', 'bee_music.mp3'))
        mixer.music.play(loops=-1, start=0.0)

    # Main Game Loop
    while True:
        time_delta = game_clock.tick(game_frame_rate) / 1000.0
        gui_master.update(time_delta)
        camera.render(entity_master.get_valid_entities())
        screen.blit(camera.render_surface, (0, 0))
        gui_master.draw_ui(screen)
        display.update()

        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
            output = gui_master.process_events(e, camera)

            if output == 0:
                return output

import ast

from pygame import event, QUIT, Rect, display, USEREVENT, DOUBLEBUF
from pygame_gui import UIManager, elements

from settings_data import Settings
from source.UI.gui_master import main_theme


def settings_loop(screen, game_clock, settings):

    def update_settings():
        data = {
            'map_size': int(map_size_dropdown.selected_option),
            'resolution': ast.literal_eval(resolution_dropdown.selected_option),
            'initial_hives': int(bee_hive_dropdown.selected_option),
            'initial_bees': int(bees_dropdown.selected_option),
            'flower_strat': flower_spawn_strat_dropdown.selected_option,
            'hive_strat': hive_spawn_strat_dropdown.selected_option,
            'music': music_dropdown.selected_option == 'True'
        }
        new_settings = Settings(data)
        new_screen = display.set_mode(new_settings.frame_resolution, DOUBLEBUF)
        return 0, new_screen, new_settings

    frame_resolution = settings.frame_resolution
    game_frame_rate = settings.frame_rate

    gui_manager = UIManager(frame_resolution, main_theme)

    element_size = (150, 50)
    element_size_l = (250, 50)

    tooltip_size = (150, 25)
    tooltip_size_l = (250, 25)

    back_button = elements.UIButton(
        relative_rect=Rect((30, 30),
                           (50, 50)),
        text='',
        object_id="back_button",
        manager=gui_manager
    )

    save_settings_button = elements.UIButton(
        relative_rect=Rect((30, 100), (125, 50)),
        text="Save Settings",
        object_id="save_settings_button",
        manager=gui_manager
    )

    resolution_dropdown = elements.UIDropDownMenu(
        options_list=[
            '1920, 1080',
            '1536, 864',
            '1360, 768',
            '1280, 1024',
            '640, 360',
        ],
        starting_option=str(settings.frame_resolution)[1:len(str(settings.frame_resolution))-1],
        relative_rect=Rect((200, 100), element_size),
        manager=gui_manager
    )
    resolution_tooltip = elements.UILabel(
        relative_rect=Rect((200, 75), tooltip_size),
        text="Window Resolution",
        manager=gui_manager
    )

    map_size_dropdown = elements.UIDropDownMenu(
        options_list=[
            '2000',
            '1000',
            '500'
        ],
        starting_option=str(settings.map_size),
        relative_rect=Rect((200, 250), element_size),
        manager=gui_manager
    )
    map_size_tooltip = elements.UILabel(
        relative_rect=Rect((200, 225), tooltip_size),
        text="Map Size",
        manager=gui_manager
    )

    music_dropdown = elements.UIDropDownMenu(
        options_list=[
            "True", "False"
        ],
        starting_option=str(settings.play_music),
        relative_rect=Rect((200, 400), element_size),
        manager=gui_manager
    )
    music_tooltip = elements.UILabel(
        relative_rect=Rect((200, 375), tooltip_size),
        text="Play Music",
        manager=gui_manager
    )

    bee_hive_dropdown = elements.UIDropDownMenu(
        options_list=[
            '2', '5', '10', '12', '20'
        ],
        starting_option=str(settings.initial_hives),
        relative_rect=Rect((375, 100), element_size),
        manager=gui_manager
    )
    bee_hive_tooltip = elements.UILabel(
        relative_rect=Rect((375, 75), tooltip_size),
        text="Number of Hives",
        manager=gui_manager
    )

    bees_dropdown = elements.UIDropDownMenu(
        options_list=[
            '6', '8', '10', '12', '16', '20'
        ],
        starting_option=str(settings.initial_bees_per_hive),
        relative_rect=Rect((375, 250), element_size),
        manager=gui_manager
    )
    bees_tooltip = elements.UILabel(
        relative_rect=Rect((375, 225), tooltip_size),
        text="Initial Bees",
        manager=gui_manager
    )

    flower_spawn_strat_dropdown = elements.UIDropDownMenu(
        options_list=[
            'normal distribution'
        ],
        starting_option=settings.flower_spawn_strat,
        relative_rect=Rect((550, 100), element_size_l),
        manager=gui_manager
    )
    flower_spawn_strat_tooltip = elements.UILabel(
        relative_rect=Rect((550, 75), tooltip_size_l),
        text="Flower Spawn Strategy",
        manager=gui_manager
    )

    hive_spawn_strat_dropdown = elements.UIDropDownMenu(
        options_list=[
            'default'
        ],
        starting_option=settings.hive_spawn_strat,
        relative_rect=Rect((550, 250), element_size_l),
        manager=gui_manager
    )
    hive_spawn_strat_tooltip = elements.UILabel(
        relative_rect=Rect((550, 225), tooltip_size_l),
        text="Hive Spawn Strategy",
        manager=gui_manager
    )

    while True:
        screen.fill((219, 173, 92))
        time_delta = game_clock.tick(game_frame_rate) / 1000.0
        gui_manager.update(time_delta)
        gui_manager.draw_ui(screen)

        display.update()
        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()

            if e.type == USEREVENT:
                if e.user_type == 'ui_button_pressed':
                    if e.ui_element == back_button:
                        return 0, screen, settings  # Returns back to main menu
                    elif e.ui_element == save_settings_button:
                        return update_settings()

            gui_manager.process_events(e)

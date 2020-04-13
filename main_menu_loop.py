from pygame import event, QUIT, Rect, display, USEREVENT
from pygame_gui import UIManager, elements

from source.UI.gui_master import main_theme
from source.entities.sprite_bank import retrieve


def main_menu_loop(screen, frame_resolution, game_clock, game_frame_rate):
    gui_manager = UIManager(frame_resolution, main_theme)
    menu_graphics = retrieve('main_menu_graphics')

    start_button = elements.UIButton(
        relative_rect=Rect((frame_resolution[0] / 2 + 150, frame_resolution[1] / 2 + 50),
                           (400, 80)),
        text="Start Simulation",
        object_id="start_sim_button",
        manager=gui_manager)

    settings_button = elements.UIButton(
        relative_rect=Rect((frame_resolution[0] / 2 + 150, frame_resolution[1] / 2 + 130),
                           (400, 80)),
        text="Settings",
        object_id="settings_button",
        manager=gui_manager)

    screen.fill((179, 147, 0))   # This is the initial draw, we don't need to re render the menu graphics later
    screen.blit(menu_graphics, (0, 0))  # This ensures a decent fps

    # Main Game Loop
    while True:

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
                    if e.ui_element == start_button:
                        return 1
                    if e.ui_element == settings_button:
                        pass

            gui_manager.process_events(e)

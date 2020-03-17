"""
Class Name: GuiMaster
Class Purpose: Handles everything UI related.
Notes:
"""
# IMPORTS
from os.path import join

import pygame_gui
from pygame import Rect, USEREVENT

# CLASS BODY

main_theme = join('assets', 'ui_elements', 'gui_theme.json')


class GuiMaster:
    def __init__(self, screen_resolution, entity_master, game_clock):
        self.gui_manager = pygame_gui.UIManager(screen_resolution, main_theme)
        self.entity_master = entity_master
        self.game_clock = game_clock
        self.main_menu_active = False
        self.main_menu_button = pygame_gui.elements.UIButton(relative_rect=
                                                             Rect((screen_resolution[0] - 112,
                                                                   screen_resolution[1] - 112), (110, 110)),
                                                             text='',
                                                             manager=self.gui_manager,
                                                             tool_tip_text="Menu",
                                                             object_id="m_m_b")

        self.menu_rect = Rect(screen_resolution[0] - 400, 0, screen_resolution[0] // 4, screen_resolution[1])
        self.menu_display = None
        self.bee_num = None
        self.flower_num = None
        self.fps = None

    def update(self, time_delta):
        if self.main_menu_active:
            self.update_main_menu()
        self.gui_manager.update(time_delta)

    def draw_ui(self, screen):
        self.gui_manager.draw_ui(screen)

    def process_events(self, event):
        if event.type == USEREVENT:
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == self.main_menu_button:
                    if self.main_menu_active:
                        self.deactivate_main_menu()
                    else:
                        self.activate_main_menu()
        self.gui_manager.process_events(event)

    def activate_main_menu(self):
        self.main_menu_active = True
        self.menu_display = self.build_menu_display()

    def deactivate_main_menu(self):
        self.main_menu_active = False
        self.menu_display.kill()

    def build_menu_display(self):
        number_of_bees = "Number of Bees: " + str(self.entity_master.bee_population)
        number_of_flowers = "Number of Flowers: " + str(self.entity_master.flower_population)
        fps_string = "Frames per Second: " + str(self.game_clock.get_fps())[0:4]

        menu = pygame_gui.core.UIContainer(
            manager=self.gui_manager,
            relative_rect=self.menu_rect
        )
        self.bee_num = pygame_gui.elements.UITextBox(
            html_text=number_of_bees,
            relative_rect=Rect(self.menu_rect[0] + 100, 0, self.menu_rect.width - 100, 40),
            manager=self.gui_manager
        )
        self.flower_num = pygame_gui.elements.UITextBox(
            html_text=number_of_flowers,
            relative_rect=Rect(self.menu_rect[0] + 100, 40, self.menu_rect.width - 100, 40),
            manager=self.gui_manager
        )
        self.fps = pygame_gui.elements.UITextBox(
            html_text=fps_string,
            relative_rect=Rect(self.menu_rect[0] + 100, 80, self.menu_rect.width - 100, 40),
            manager=self.gui_manager
        )

        menu.add_element(self.bee_num)
        menu.add_element(self.flower_num)
        menu.add_element(self.fps)

        return menu

    def update_main_menu(self):
        fps_string = "Frames per Second: " + str(self.game_clock.get_fps())[0:4]
        self.menu_display.remove_element(self.fps)
        self.fps.kill()
        self.fps = pygame_gui.elements.UITextBox(
            html_text=fps_string,
            relative_rect=Rect(self.menu_rect[0] + 100, 80, self.menu_rect.width - 100, 40),
            manager=self.gui_manager
        )
        self.menu_display.add_element(self.fps)

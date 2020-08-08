"""
Class Name: GuiMaster
Class Purpose: Handles everything UI related.
Notes:
"""
# IMPORTS
from os.path import join

from pygame import Rect, USEREVENT, MOUSEBUTTONUP, mouse, Vector2, MOUSEBUTTONDOWN
from pygame_gui import UIManager, elements

# CLASS BODY
main_theme = join('source', 'assets', 'gui_theme.json')


class GuiMaster:
    def __init__(self, screen_resolution, entity_master, game_clock):
        self.gui_manager = UIManager(screen_resolution, main_theme)

        self.entity_master = entity_master
        self.game_clock = game_clock
        self.main_menu_active = False

        self.main_menu_button = elements.UIButton(relative_rect=
                                                  Rect((screen_resolution[0] - 112,
                                                        screen_resolution[1] - 112), (110, 110)),
                                                  text='',
                                                  object_id="button_main_menu",
                                                  manager=self.gui_manager,
                                                  tool_tip_text="Menu")

        self.pause_button = elements.UIButton(relative_rect=
                                              Rect((screen_resolution[0] - 200,
                                                    screen_resolution[1] - 80), (70, 70)),
                                              text="pause",
                                              object_id="sim_button",
                                              manager=self.gui_manager,
                                              tool_tip_text="Pause Sim")

        self.exit_button = elements.UIButton(relative_rect=
                                             Rect((10,
                                                   screen_resolution[1] - 80), (70, 70)),
                                             text="exit",
                                             object_id="sim_button",
                                             manager=self.gui_manager,
                                             tool_tip_text="Exit Sim")
        self.drag_begin = None
        self.info_screen = self.build_info_display(screen_resolution)
        self.info_screen.kill()

    def update(self, time_delta):
        self.update_info_screen()
        self.gui_manager.update(time_delta)

    def draw_ui(self, screen):
        return self.gui_manager.ui_group.draw(screen)

    def process_events(self, event, camera):
        if event.type == MOUSEBUTTONUP:
            if not (event.button == 4 or event.button == 5):
                test_position = mouse.get_pos()
                test_position = test_position[0] + camera.location.x, test_position[1] + camera.location.y
                selected_hive = self.entity_master.get_hive_at(test_position)
                if selected_hive is not None:
                    selected_hive.highlight()
            if event.button == 1:
                drag_end = Vector2(event.pos)
                drag_direction = self.drag_begin - drag_end
                camera.move(drag_direction)

        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                self.drag_begin = Vector2(mouse_x, mouse_y)

            elif event.button == 4:
                camera.zoom_in()
            elif event.button == 5:
                camera.zoom_out()

        elif event.type == USEREVENT:
            if event.user_type == 'ui_button_pressed':
                if event.ui_element == self.main_menu_button:
                    self.deactivate_main_menu() if self.main_menu_active else self.activate_main_menu()
                elif event.ui_element == self.pause_button:
                    self.unpause_sim() if self.entity_master.sim_paused else self.pause_sim()
                elif event.ui_element == self.exit_button:
                    return 0  # Takes us back to the main menu

        self.gui_manager.process_events(event)

    def unpause_sim(self):
        self.entity_master.sim_paused = False

    def pause_sim(self):
        self.entity_master.sim_paused = True

    def activate_main_menu(self):
        self.main_menu_active = True
        self.gui_manager.get_sprite_group().add(self.info_screen)

    def deactivate_main_menu(self):
        self.main_menu_active = False
        self.info_screen.kill()

    def build_info_display(self, res):
        """
        Builds the ui element displaying the current state of the simulation
        :return: Menu render
        """
        number_of_bees = "Number of Bees: " + str(self.entity_master.bee_population)
        number_of_flowers = "Number of Flowers: " + str(self.entity_master.flower_population)
        fps_string = "Frames per Second: " + str(self.game_clock.get_fps())[0:4]

        return elements.UITextBox(
            html_text=number_of_bees + '<br><br>' + number_of_flowers + '<br><br>' + fps_string,
            relative_rect=Rect(res[0] - 201, 0, 200, 120),
            manager=self.gui_manager
        )

    def update_info_screen(self):
        """
        Updates all the parameters that have changed since last time and rebuilds
        :return: void
        """
        number_of_bees = "Number of Bees: " + str(self.entity_master.bee_population)
        number_of_flowers = "Number of Flowers: " + str(self.entity_master.flower_population)
        fps_string = "Frames per Second: " + str(self.game_clock.get_fps())[0:4]
        self.info_screen.html_text = number_of_bees + '<br><br>' + number_of_flowers + '<br><br>' + fps_string
        self.info_screen.rebuild()

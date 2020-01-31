"""
Class Name: Event Master
Class Purpose: Handles logic behind game events
Notes: Class needs reworking, implemented mostly for camera functionality
"""

#  IMPORTS
from sys import exit
import pygame


class EventMaster:

    def __init__(self, camera):
        self.camera = camera

        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.zoom_in = False
        self.zoom_out = False

    def handle_event(self, event, menu_active, entity_master, inspection_target):

        if event.type == pygame.MOUSEBUTTONUP:
            pos = list(pygame.mouse.get_pos())
            if not (menu_active and pos[0] > 1200):
                inspection_target = entity_master.get_hive_at(pos)
            elif menu_active and \
                    1270 <= pos[0] <= 1500 and 540 <= pos[1] <= 580:
                inspection_target.highlight_bees()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.moving_down = False
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.moving_up = False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moving_right = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moving_left = False
            if event.key == pygame.K_EQUALS:
                self.zoom_in = False
            elif event.key == pygame.K_MINUS:
                self.zoom_out = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.moving_down = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.moving_up = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moving_right = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moving_left = True

            if event.key == pygame.K_EQUALS:
                self.zoom_in = True
            elif event.key == pygame.K_MINUS:
                self.zoom_out = True

            if event.key == pygame.K_m and not menu_active:
                menu_active = True
            elif event.key == pygame.K_m and menu_active:
                menu_active = False

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        self.move_camera(self.moving_down, self.moving_up, self.moving_right, self.moving_left)
        self.update_camera_zoom(self.zoom_in, self.zoom_out)

        return inspection_target, menu_active

    def update_camera_zoom(self, z_in, z_out):
        if z_in:
            delta_x = self.camera.size[0] / 10
            delta_y = self.camera.size[1] / 10
            new_camera_size = \
                self.camera.size[0] - delta_x, self.camera.size[1] - delta_y
            if new_camera_size[0] > 400:
                self.camera.size = new_camera_size
        elif z_out:
            delta_x = self.camera.size[0] / 10
            delta_y = self.camera.size[1] / 10
            new_camera_size = \
                self.camera.size[0] + delta_x, self.camera.size[1] + delta_y
            if new_camera_size[0] < 2000:
                self.camera.size = new_camera_size

    def move_camera(self, moving_down, moving_up, moving_right, moving_left):
        if moving_down:
            self.camera.location[1] = self.camera.location[1] + 10
        if moving_up:
            self.camera.location[1] = self.camera.location[1] - 10
        if moving_right:
            self.camera.location[0] = self.camera.location[0] + 10
        if moving_left:
            self.camera.location[0] = self.camera.location[0] - 10

import pygame
import sys


class EventMaster:

    def __init__(self):
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False

    def handle_event(self, event, menu_active, entity_master, inspection_target, camera_location):
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.moving_down = True
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.moving_up = True
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.moving_right = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.moving_left = True

            if event.key == pygame.K_m and not menu_active:
                menu_active = True
            elif event.key == pygame.K_m and menu_active:
                menu_active = False

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        camera_location = \
            self.move_camera(camera_location, self.moving_down, self.moving_up, self.moving_right, self.moving_left)

        return inspection_target, menu_active, camera_location

    def move_camera(self, camera_location, moving_down, moving_up, moving_right, moving_left):
        if moving_down:
            camera_location[1] = camera_location[1] + 10
        if moving_up:
            camera_location[1] = camera_location[1] - 10
        if moving_right:
            camera_location[0] = camera_location[0] + 10
        if moving_left:
            camera_location[0] = camera_location[0] - 10

        return camera_location

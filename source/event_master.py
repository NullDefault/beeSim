import pygame
import sys


def handle_event(event, menu_active, entity_master, inspection_target):
    if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        if not (menu_active and pos[0] > 1200):
            inspection_target = entity_master.get_hive_at(pos)
        elif menu_active and \
                1270 <= pos[0] <= 1500 and 540 <= pos[1] <= 580:
            inspection_target.highlight_bees()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_m and not menu_active:
            menu_active = True
        elif event.key == pygame.K_m and menu_active:
            menu_active = False
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    return inspection_target, menu_active
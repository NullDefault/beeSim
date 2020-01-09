import pygame
from source.entity_master import EntityMaster
from source.menus import menu_render
from source.event_master import EventMaster

########################################################################################################################
# Data Fields
screen_resolution = (1600, 900)
menu_location = (1200, 0)

play_area = (1600, 900)

background = pygame.image.load("assets/grass_background.png")


entity_master = EntityMaster(initial_hives=1,
                             default_bees_per_hive=6,
                             number_of_flower_zones=4,
                             initial_growth_stages=7,
                             play_area_dimensions=play_area)
event_master = EventMaster()

play_music = False

game_icon = pygame.image.load("assets/gameIcon.png")

game_clock = pygame.time.Clock()
game_frame_rate = 24


def main():
########################################################################################################################
# Init Screen
    screen = pygame.display.set_mode(screen_resolution)
    abstract_game_screen = pygame.Surface(play_area)
    camera_location = [0, 0]  # Controls which part of the screen is being rendered
    camera_size = (1600, 900)
    pygame.display.set_icon(game_icon)
    pygame.display.set_caption("beeSim")
# Init Music
    if play_music:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/beeMusic.mp3")
        pygame.mixer.music.play(loops=-1, start=0.0)
# Init Game Vars
    menu_active = False
    inspection_target = None
########################################################################################################################
# Main Game Loop
    while True:

        game_clock.tick(game_frame_rate)

        entities_to_be_rendered = entity_master.get_valid_entities()

        abstract_game_screen.blit(background, (0, 0))
        entities_to_be_rendered.draw(abstract_game_screen)  # TODO: only draw the visible ones

        camera_cropped_render = pygame.Surface(camera_size)
        camera_cropped_render.blit(abstract_game_screen, (0, 0),
                                   (camera_location[0], camera_location[1], camera_size[0], camera_size[1]))

        pygame.transform.scale(camera_cropped_render, screen_resolution, screen)

        if menu_active:
            screen.blit(menu_render(entity_master, game_clock, inspection_target), menu_location)

        pygame.display.flip()

        for event in pygame.event.get():
            inspection_target, menu_active, camera_location = \
                event_master.handle_event(event, menu_active, entity_master, inspection_target, camera_location)
########################################################################################################################


if __name__ == "__main__":
    main()

import pygame
from source import gameBoard
from source.EntityMaster import EntityMaster
from source.menus import menu_render
from source.event_master import handle_event

########################################################################################################################
# Data Fields
screen_size = (1600, 900)
menu_location = (1200, 0)
background = gameBoard.Background((0, 0))  # This is just the background

initial_hives = 3    # These will eventually be tunable parameters you can access from the UI
default_bee_ratio = 10
initial_flower_beds = 20

entity_master = EntityMaster(initial_hives, default_bee_ratio,
                             initial_flower_beds, screen_size)

play_music = False

game_icon = pygame.image.load("assets/gameIcon.png")

game_clock = pygame.time.Clock()
game_frame_rate = 24


def main():
########################################################################################################################
# Init Screen
    screen = pygame.display.set_mode(screen_size)
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

        entities_to_be_rendered = entity_master.get_renderable_entities()

        screen.blit(background.image, background.rect)
        entities_to_be_rendered.draw(screen)

        if menu_active:
            screen.blit(menu_render(entity_master, game_clock, inspection_target), menu_location)

        pygame.display.flip()

        for event in pygame.event.get():
            inspection_target, menu_active = handle_event(event, menu_active, entity_master, inspection_target)
########################################################################################################################


if __name__ == "__main__":
    main()

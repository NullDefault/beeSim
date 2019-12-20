import pygame
import sys
from source import gameBoard
from source import EntityMaster
########################################################################################################################
# Data Fields

screen_size = (1600, 900)
_background = gameBoard.Background((0, 0))  # This is just the background

initialHives = 3     # These will eventually be tunable parameters you can access from the UI
defaultBeeRatio = 10
defaultFlowerNumber = 0

entityMaster = EntityMaster.EntityMaster(initialHives, defaultBeeRatio, defaultFlowerNumber, screen_size)

play_music = False
frame_delay = 14


def main():
########################################################################################################################
# Init Screen
    screen = pygame.display.set_mode(screen_size)
########################################################################################################################
# Init Music
    if play_music:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/beeMusic.mp3")
        pygame.mixer.music.play(loops=-1, start=0.0)
########################################################################################################################
# Main Game Loop
    while True:
        screen.blit(_background.image, _background.rect)

        entities_to_be_rendered = entityMaster.get_renderable_entities()
        entities_to_be_rendered.draw(screen)

        pygame.display.flip()
        pygame.time.delay(frame_delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
########################################################################################################################


if __name__ == "__main__":
    main()

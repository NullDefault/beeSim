import pygame
import sys
from source import gameBoard
from source.EntityMaster import EntityMaster
########################################################################################################################
# Data Fields

screen_size = (1600, 900)
background = gameBoard.Background((0, 0))  # This is just the background

initialHives = 1    # These will eventually be tunable parameters you can access from the UI
defaultBeeRatio = 20
initialFlowerBeds = 20

entityMaster = EntityMaster(initialHives, defaultBeeRatio,
                            initialFlowerBeds, screen_size)

play_music = False

gameIcon = pygame.image.load("assets/gameIcon.png")

gameClock = pygame.time.Clock()
game_frame_rate = 24

fps_location = (10, 10)

pygame.font.init()
gameFont = pygame.font.Font("assets/3Dventure.ttf", 20)


def main():
########################################################################################################################
# Init Screen
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_icon(gameIcon)
    pygame.display.set_caption("beeSim")
# Init Music
    if play_music:
        pygame.mixer.init()
        pygame.mixer.music.load("assets/beeMusic.mp3")
        pygame.mixer.music.play(loops=-1, start=0.0)
########################################################################################################################
# Main Game Loop
    while True:

        gameClock.tick(game_frame_rate)

        entities_to_be_rendered = entityMaster.get_renderable_entities()

        screen.blit(background.image, background.rect)
        entities_to_be_rendered.draw(screen)
        screen.blit(update_fps_display(), fps_location)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                target_bee = entityMaster.handle_bee_press(pos)
                if target_bee is not None:
                    print(target_bee.bee_states.current)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
########################################################################################################################


def update_fps_display():
    fps = gameClock.get_fps()
    fps_display = gameFont.render("FPS: "+str(fps)[0:4], False, [0, 0, 0], None)
    return fps_display


if __name__ == "__main__":
    main()

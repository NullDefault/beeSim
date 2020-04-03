"""
Class Name: Bee Factory Tester
Class Purpose: Tester code for the bee procedural generation, shows a random assembly of generated sprites enlarged
to be more visible
Notes:
"""

from pygame import Surface, display, time, SRCALPHA, transform, event, QUIT
from random import randint
from source.entities.bee_data.bee_components import bee_factory


def main():
    screen = display.set_mode((1500, 800))
    screen.fill([255, 255, 255], (0, 0, 1500, 800))
    clock = time.Clock()

    for y in range(0, 5):
        for x in range(0, 18):
            head = randint(0, 11)
            torso = randint(0, 5)
            wing_u = randint(0, 5)
            wing_d = randint(0, 5)

            sprites = bee_factory.make_bee_sprites((head, torso, wing_u, wing_d))

            wings_u_sprite = Surface((18*4, 18*4), SRCALPHA)
            wings_d_sprite = Surface((18*4, 18*4), SRCALPHA)

            transform.scale(sprites[0], (18*4, 18*4), wings_u_sprite)
            transform.scale(sprites[1], (18*4, 18*4), wings_d_sprite)

            screen.blit(wings_u_sprite, (x * 80 + 20, y * 80))
            screen.blit(wings_d_sprite, (x * 80 + 20, y * 80 + 80 * 5))

    while True:
        clock.tick(60)
        for e in event.get():
            if e.type == QUIT:
                quit()
                exit()
        display.update()


if __name__ == '__main__':
    main()

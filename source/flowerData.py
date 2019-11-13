import pygame


class Flower(pygame.sprite.Sprite):
    def __init__(self, location, flower_type):
        pygame.sprite.Sprite.__init__(self)
        if flower_type == 1:
            self.image = pygame.image.load("assets/Flowers/redFlower.png")
        elif flower_type == 2:
            self.image = pygame.image.load("assets/Flowers/blueFlower.png")
        else:
            self.image = pygame.image.load("assets/Flowers/purpleFlower.png")

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

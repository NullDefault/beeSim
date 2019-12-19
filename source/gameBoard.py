import pygame


class Background(pygame.sprite.Sprite):

    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/grass_background_test.png")
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

